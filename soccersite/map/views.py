from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.db.models import Count, Q, F, Func
from .models import GroupedData
from django.core import serializers
import json
from .forms import MHSForm, DocumentForm
from django.contrib.admin.views.decorators import staff_member_required
import csv
import codecs

def index(request):
    colleges  = GroupedData.objects.values_list('college', flat=True).distinct().order_by('college')
    leagues   = GroupedData.objects.values_list('college_league', flat=True).distinct().order_by('college_league')
    positions = GroupedData.objects.annotate(arr_els=Func(F('position'), function='unnest')).values_list('arr_els', flat=True).distinct()
    context = {'API_KEY': settings.GOOGLE_MAPS_API_KEY,
               'colleges': colleges,
               'leagues': leagues,
               'positions': positions,
               }

    if(request.method == 'POST'): #form.js will check for at least one college selected before submission
        payload = json.loads(request.POST.get('json_data'))
        c = payload['colleges'] #list of colleges user specified from drop down
        pos = payload['positions'] #list of positions user specified from positions drop down
        sy = payload['starterYears'] #list of starterYears specified from positions drop down
        acy = payload['allConferenceYears'] #list of allConferenceYears positioned in drop down

        starterYearFourOrMore = '4+' in sy
        allConferenceYearsFourOrMore = '4+' in acy

        players = None

        if(len(c) > 0):
            players = GroupedData.objects.filter(college__in=c)

        if(len(pos) > 0):
            if(players):
                players = players.filter(position__overlap=pos)
            else:
                players = GroupedData.objects.filter(position_overlap=pos)

        if(len(sy) > 0):
            if(players):
                if(starterYearFourOrMore):
                    if(len(sy) == 1):
                        players = players.filter(starter_count__gte=4)
                    else:
                        players = players.filter(Q(starter_count__gte=4) | Q(starter_count__in=sy[:-1]))
                else:
                    players = players.filter(starter_count__in=sy)

            else:
                if(starterYearFourOrMore):
                    if(len(sy) == 1):
                        players = GroupedData.filter(starter_count__gte=4)
                    else:
                        players = GroupedData.filter(Q(starter_count__gte=4) | Q(starter_count__in=sy[:-1]))
                else:
                    players = GroupedData.filter(starter_count__in=sy)

        if(len(acy) > 0):
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
                        players = GroupedData.filter(accolade_count__gte=4)
                    else:
                        players = GroupedData.filter(Q(accolade_count__gte=4) | Q(accolade_count__in=acy[:-1]))
                else:
                    players = GroupedData.filter(accolade_count__in=acy)

        data  =  {'players': list(players.values())}
        return JsonResponse(data)

    return render(request, 'map/index.html', context)

def about(request):
    return render(request, 'map/about.html')



@staff_member_required
def upload_file(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            save_data(form.cleaned_data['document'])
            form.save()
            return render(request, 'map/upload.html', {'form':form})
    else:
        form = DocumentForm()
    return render(request, 'map/upload.html', {'form':form})



def save_data(filename):
    records = csv.reader(codecs.iterdecode(filename,'utf-8'))
    next(records)
    for record in records:
        input_data = MatchedHighSchool()
        input_data.rosterYear = record[1]
        if record[2] == '':
            input_data.playerNumber = 0
        else:
            input_data.playerNumber = record[2]
        input_data.firstName = record[3]
        input_data.lastName = record[4]
        input_data.year = record[5]
        input_data.position1 = record[6]
        input_data.height = record[7]
        if record[8] == '':
            input_data.weight = 0
        else:
            input_data.weight = record[8]
        input_data.homeTown = record[9]
        input_data.stateOrCountry = record[10]
        input_data.highSchool = record[11]
        input_data.alternativeSchool = record[12]
        input_data.college = record[13]
        input_data.collegeLeague = record[14]
        input_data.bioLink = record[15]
        input_data.isStarter = record[16]
        input_data.accolade = record[17]
        input_data.matchedCity = record[18]
        input_data.matchedInstitution = record[19]
        input_data.matchedStateProvince = record[20]
        input_data.matchedCountry = record[21]
        input_data.latitude = record[22]
        input_data.longitude = record[23]
        input_data.schoolType = record[24]
        input_data.save()
