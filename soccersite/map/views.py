"""
views.py provides the backend application logic such as database accesses
and data transformations
"""

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.db.models import Count, Q, F, Func
from .models import GroupedData, RosterData, StarterData, AccoladeData, Documents, BackUp, HighSchoolMatchMaster, HighSchoolData
from django.core import serializers
import json
from .forms import DocumentForm
from django.contrib.admin.views.decorators import staff_member_required
import csv
import codecs
import subprocess
from random import randint

"""
 _random_with_N_digits returns a random number of length n
 input: n::int
 return: int
"""
def _random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

"""
index(request) is the view for the homepage
"""
def index(request):
    colleges  = GroupedData.objects.values_list('college', flat=True).distinct().order_by('college')
    leagues   = GroupedData.objects.values_list('college_league', flat=True).distinct().order_by('college_league')
    positions = GroupedData.objects.annotate(arr_els=Func(F('position'), function='unnest')).values_list('arr_els', flat=True).distinct()
    currentBackUpVersion = BackUp.objects.filter(isCurrent=True).first()
    context = {'API_KEY': settings.GOOGLE_MAPS_API_KEY,
               'colleges': colleges,
               'leagues': leagues,
               'positions': positions,
               'currentBackUp': currentBackUpVersion
               }

    if(request.method == 'POST'):
        payload = json.loads(request.POST.get('json_data'))
        c = payload['colleges'] #list of colleges user specified from drop down
        pos = payload['positions'] #list of positions user specified from positions drop down
        sy = payload['starterYears'] #list of starterYears specified from positions drop down
        acy = payload['allConferenceYears'] #list of allConferenceYears positioned in drop down

        starterYearFourOrMore = '4+' in sy #user selected '4+' in years starter dropdown
        allConferenceYearsFourOrMore = '4+' in acy #user selected '4+' in all conference years dropdown

        multiplePlayersPerSchool = False
        if(payload['multipleHS'] == 'selected'):
            multiplePlayersPerSchool = True #user selected checkbox for filtering high schools with more than one player per school

        players = None #this will be the returned data for query

        #if nothing is selected, default to search all
        if((len(c) == 0) and (len(pos) == 0) and (len(sy) == 0) and (len(acy) == 0)):
            c = colleges; #since c is all colleges, all data will be returned in the subsequent code

        if(len(c) > 0): #if a college is selected
            players = GroupedData.objects.filter(college__in=c)

        if(len(pos) > 0): #if a position is selected
            if(players): #if there was a college selected, filter existing players
                players = players.filter(position__overlap=pos)
            else:
                players = GroupedData.objects.filter(position__overlap=pos)

        if(len(sy) > 0): #if a starter year was selected
            if(players): #if there was a college selected or a position selected
                if(starterYearFourOrMore):
                    if(len(sy) == 1): #if only 4+ was selected
                        players = players.filter(starter_count__gte=4)
                    else: #if other things including 4+ was selected
                        players = players.filter(Q(starter_count__gte=4) | Q(starter_count__in=sy[:-1]))
                else:
                    players = players.filter(starter_count__in=sy)

            else: #if there weren't any players filtered yet
                if(starterYearFourOrMore):
                    if(len(sy) == 1):
                        players = GroupedData.objects.filter(starter_count__gte=4)
                    else:
                        players = GroupedData.objects.filter(Q(starter_count__gte=4) | Q(starter_count__in=sy[:-1])) #slicing up to '4+'
                else:
                    players = GroupedData.objects.filter(starter_count__in=sy)

        if(len(acy) > 0): #same logic as starter years
            if(players):
                if(allConferenceYearsFourOrMore):
                    if(len(acy) == 1):
                        players = players.filter(accolade_count__gte=4)
                    else:
                        players = players.filter(Q(accolade_count__gte=4) | Q(accolade_count__in=acy[:-1]))
                else:
                    players = players.filter(accolade_count__in=acy)

            else:
                if(allConferenceYearsFourOrMore):
                    if(len(acy) == 1):
                        players = GroupedData.objects.filter(accolade_count__gte=4)
                    else:
                        players = GroupedData.objects.filter(Q(accolade_count__gte=4) | Q(accolade_count__in=acy[:-1]))
                else:
                    players = GroupedData.objects.filter(accolade_count__in=acy)

        if(multiplePlayersPerSchool):
            #getting all duplicate high school names in the same city
            dupeHS = players.values('high_school', 'highschoolcity') \
                       .annotate(hs_cnt=Count('high_school'), city_cnt=Count('highschoolcity')) \
                       .order_by() \
                       .filter(Q(hs_cnt__gt=1) & Q(city_cnt__gt=1))

            #filtering players further
            players = players.filter(high_school__in=[item['high_school'] for item in dupeHS])

        data  =  {'players': list(players.values())} #payload to return
        return JsonResponse(data)

    return render(request, 'map/index.html', context)

"""
about(request) is the view for the about page
"""
def about(request):
    return render(request, 'map/about.html')

"""
manualupload(request) is the view for the manual upload page
"""
def manualupload(request):
    positions = GroupedData.objects.annotate(arr_els=Func(F('position'), function='unnest')).values_list('arr_els', flat=True).distinct()
    colleges  = GroupedData.objects.values_list('college', flat=True).distinct().order_by('college')
    leagues   = GroupedData.objects.values_list('college_league', flat=True).distinct().order_by('college_league')

    context = {'positions':positions,
               'colleges': colleges,
               'leagues': leagues}
    if(request.method=='POST'):
        payload = json.loads(request.POST.get('json_data'))
        mostRecentId = HighSchoolMatchMaster.objects.values_list('id', flat=True).order_by('id').latest('id')
        record = HighSchoolMatchMaster(mostRecentId + 1,
                                       payload['rosterYear'],
                                       payload['playerNumber'],
                                       payload['firstName'],
                                       payload['lastName'],
                                       payload['classYear'],
                                       payload['position'],
                                       payload['height'],
                                       payload['weight'],
                                       payload['homeTown'],
                                       payload['stateOrCountry'],
                                       payload['highSchool'],
                                       payload['alternativeSchool'],
                                       payload['college'],
                                       payload['collegeLeague'],
                                       payload['bioLink'],
                                       payload['isStarter'],
                                       payload['accolade'],
                                       payload['highSchoolCity'],
                                       payload['highSchool'],
                                       payload['highSchoolStateOrProvince'],
                                       payload['highSchoolCountry'],
                                       payload['highSchoolLatitude'],
                                       payload['highSchoolLongitude'],
                                       payload['schoolType'])
        record.save()
        #insert into document table to trigger the trigger and group the inserted players
        doc = Documents(description="Manual Upload" + str(_random_with_N_digits(3)),
                       rosterData=None,
                       starterData=None,
                       accoladeData=None,
                       manual_upload=True)
        doc.save()
        return JsonResponse({"success":"true"})
    return render(request, 'map/manualupload.html', context)

"""
upload_file(request) is the view for the upload page
"""
@staff_member_required
def upload_file(request):
    if(request.method == 'POST'):
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            a = save_rosterData(form.cleaned_data['rosterData'])
            b = save_starterData(form.cleaned_data['starterData'])
            c = save_accoladeData(form.cleaned_data['accoladeData'])
            form.save()
            #writing backup file. Output will go to ./fixtures directory as a .json file
            fn = "dumpfile" + str(_random_with_N_digits(10)) + ".json"
            json_dump = subprocess.run(["python", "manage.py", "dumpdata", "-o", "map/fixtures/" + fn, \
                                        "--exclude=admin", "--exclude=auth", "--exclude=contenttypes", \
                                        "--exclude=sessions", "--exclude=messages", "--exclude=staticfiles", \
                                        "--exclude=map.Documents", "--exclude=map.BackUp", "--exclude=map.HighSchoolData"])

            #reassigning the current data version as the most recently uploaded dump
            old_version = BackUp.objects.filter(isCurrent=True).first() #old version will be the current version
            old_version.isCurrent = False
            old_version.isLoaded = False
            old_version.save(update_fields=['isCurrent', 'isLoaded'])

            new_version = BackUp(description = form.cleaned_data['description'], file=fn, isCurrent=True, isLoaded=True)
            new_version.save()

            if(a and b and c):
                context = {'form': form, 'uploaded': True}
            else:
                context = {'form': form, 'uploaded': False} #error handling case
            return render(request, 'map/upload.html', context)
    else:
        form = DocumentForm()
    return render(request, 'map/upload.html', {'form':form})

"""
 restore(request) is the view for the restore page
"""
@staff_member_required
def restore(request):
    versions = reversed(BackUp.objects.all().values('description', 'uploaded_at'))
    if(request.method=='POST'):
        if(request.POST.get('json_data')):
            payload = json.loads(request.POST.get('json_data'))
            #acquire old description and reassign isCurrent and isLoaded to false
            description = payload['version']
            old_version = BackUp.objects.filter(isCurrent=True).first()
            descpt = old_version.description
            fn = old_version.file
            old_version.delete()
            old_version_temp = BackUp(description=descpt, file=fn, isCurrent=False, isLoaded=False)
            old_version_temp.save()

            #update new_version which is the version selected
            new_version = BackUp.objects.filter(description=description).first()
            new_version.isCurrent = True
            new_version.isLoaded = False
            new_version.save(update_fields=['isCurrent', 'isLoaded'])

            #run respotre process
            backUpFile  = "map/fixtures/" + BackUp.objects.filter(description=description).get().filename()
            RosterData.objects.all().delete()
            StarterData.objects.all().delete()
            AccoladeData.objects.all().delete()
            GroupedData.objects.all().delete()
            HighSchoolMatchMaster.objects.all().delete()
            p = subprocess.Popen(["python", "manage.py", "loaddata", backUpFile])

            currentBackUpVersion = BackUp.objects.filter(isCurrent=True).first()
            return render(request, 'map/restore.html', {'versions': versions,
                                                        'currentBackUp': currentBackUpVersion})

    #acquire currentBackup to render upon refreshing the page
    new_version = BackUp.objects.filter(isCurrent=True).first()
    if(HighSchoolMatchMaster.objects.all().exists()): #if finished loading
        try: #try catch to avoid duplicate description error
            new_version.isLoaded = True
            new_version.save(update_fields=['isLoaded'])
        except:
            pass

    currentBackUpVersion = BackUp.objects.filter(isCurrent=True).first()
    return render(request, 'map/restore.html', {'versions': versions,
                                                'currentBackUp': currentBackUpVersion})


"""
save_rosterData(filename) saves an uploaded rosterdata.csv upload to the database
"""
def save_rosterData(filename):
    try:
        records = csv.reader(codecs.iterdecode(filename,'utf-8'))
        next(records)
        for record in records:
            input_data = RosterData()
            input_data.roster_year = record[1]
            if record[2] == '':
                input_data.player_number = 0
            else:
                input_data.player_number = record[2]
            input_data.first_name = record[3]
            input_data.last_name = record[4]
            input_data.year = record[5]
            input_data.position1 = record[6]
            input_data.position2 = record[7]
            input_data.position3 = record[8]
            input_data.height = record[9]
            if record[10] == '':
                input_data.weight = 0
            else:
                input_data.weight = record[10]
            input_data.home_town = record[11]
            input_data.state_or_country = record[12]
            input_data.high_school = record[13]
            input_data.alternative_school = record[14]
            input_data.college = record[15]
            input_data.college_league = record[16].upper()
            input_data.bio_link = record[17]
            input_data.save()
    except:
        return False
    else:
        return True

"""
save_starterData(filename) saves an uploaded starterdata.csv file to the database
"""
def save_starterData(filename):
    try:
        records = csv.reader(codecs.iterdecode(filename,'utf-8'))
        next(records)
        for record in records:
            input_data = StarterData()
            input_data.roster_year = record[1]
            input_data.number = record[2]
            input_data.first_name = record[3]
            input_data.last_name = record[4]
            input_data.potential_starts = record[5]
            if record[6] == '':
                input_data.gp = 0
            else:
                input_data.gp = record[6]
            if record[7] == '':
                input_data.gs = 0
            else:
                input_data.gs = record[7]
            input_data.is_starter = record[8]
            input_data.college = record[9]
            input_data.save()
    except:
        return False
    else:
        return True

"""
save_accoladeData(filename) saves an uploaded accolade.csv file to the database
"""
def save_accoladeData(filename):
    try:
        records = csv.reader(codecs.iterdecode(filename,'utf-8'))
        next(records)
        for record in records:
            input_data = AccoladeData()
            input_data.roster_year = record[1]
            input_data.first_name = record[2]
            input_data.last_name = record[3]
            input_data.accolade = record[4]
            input_data.college = record[5]
            input_data.save()
    except:
        return False
    else:
        return True
