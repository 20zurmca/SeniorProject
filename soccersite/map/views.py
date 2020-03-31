from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.db.models import Count
from .models import RosterMasterData, MatchedHighSchool
from django.core import serializers
import json

# Create your views here.

def index(request):
    colleges  = RosterMasterData.objects.values_list('college', flat=True).distinct().order_by('college')
    leagues   = RosterMasterData.objects.values_list('collegeLeague', flat=True).distinct().order_by('collegeLeague')
    positions = RosterMasterData.objects.values_list('position1', flat=True).distinct().order_by('position1')

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
