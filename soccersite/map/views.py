from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.db.models import Count
from .models import RosterMasterData, MatchedHighSchool
from django.core import serializers
import json
from .forms import MHSForm, DocumentForm
from django.contrib.admin.views.decorators import staff_member_required
import csv
import codecs

# Create your views here.

def index(request):
    colleges  = RosterMasterData.objects.values_list('college', flat=True).distinct().order_by('college')
    leagues   = RosterMasterData.objects.values_list('collegeLeague', flat=True).distinct().order_by('collegeLeague')
    positions = RosterMasterData.objects.values_list('position1', flat=True).distinct().order_by('position1')

    print(colleges)
    context = {'API_KEY': settings.GOOGLE_MAPS_API_KEY,
               'colleges': colleges,
               'leagues': leagues,
               'positions': positions,
               }

    if(request.method == 'POST'): #form.js will check for at least one college selected before submission
        payload = json.loads(request.POST.get('json_data'))
        c = payload['colleges'] #list of colleges user specified from drop down
        pos = payload['positions'] #list of positions user specified from positions drop down
        sy = payload['starterYears'] # TODO: implement queries for this
        acy = payload['allConferenceYears'] # TODO: implement queries for this
        players =  MatchedHighSchool.objects.filter(college__in=c) \
                                                 .annotate(num_colleges=Count('college')) \
                                                 .filter(num_colleges=len(c)).values()


        data  =  {'players': list(players)}
        return JsonResponse(data)

    return render(request, 'map/index.html', context)

def about(request):
    return render(request, 'map/about.html')



@staff_member_required
def upload_file(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            #print("form.document: ", form.cleaned_data['document'])
            form.save()
            save_data( form.cleaned_data['document'])
            return render(request, 'map/myadmin.html', {'form':form})
    else:
        form = DocumentForm()
    return render(request, 'map/myadmin.html', {'form':form})



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
