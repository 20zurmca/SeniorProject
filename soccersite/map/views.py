from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.db.models import Count, Q, F, Func
from .models import GroupedData, RosterData, StarterData, AccoladeData
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
                players = GroupedData.objects.filter(position__overlap=pos)

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
                        players = GroupedData.objects.filter(starter_count__gte=4)
                    else:
                        players = GroupedData.objects.filter(Q(starter_count__gte=4) | Q(starter_count__in=sy[:-1]))
                else:
                    players = GroupedData.objects.filter(starter_count__in=sy)

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
                        players = GroupedData.objects.filter(accolade_count__gte=4)
                    else:
                        players = GroupedData.objects.filter(Q(accolade_count__gte=4) | Q(accolade_count__in=acy[:-1]))
                else:
                    players = GroupedData.objects.filter(accolade_count__in=acy)

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
            save_rosterData(form.cleaned_data['rosterData'])
            save_starterData(form.cleaned_data['starterData'])
            save_accoladeData(form.cleaned_data['accoladeData'])
            form.save()
            return render(request, 'map/upload.html', {'form':form})
    else:
        form = DocumentForm()
    return render(request, 'map/upload.html', {'form':form})



def save_rosterData(filename):
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
        input_data.college_league = record[16]
        input_data.bio_link = record[17]
        input_data.save()

def save_starterData(filename):
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

def save_accoladeData(filename):
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
