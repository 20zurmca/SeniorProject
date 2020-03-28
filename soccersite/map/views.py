from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from .models import RosterMasterData, MatchedHighSchool
from django.core import serializers
import json

# Create your views here.

def index(request):
    colleges  = RosterMasterData.objects.values_list('college', flat=True).distinct().order_by('college')
    leagues   = RosterMasterData.objects.values_list('collegeLeague', flat=True).distinct().order_by('collegeLeague')
    positions = RosterMasterData.objects.values_list('position1', flat=True).distinct().order_by('position1')

    #everything
    players =  MatchedHighSchool.objects.all()
    jsData  =  serializers.serialize("json", players)

    if(request.method == 'POST'):
        payload = json.loads(request.POST.get('json_data'))
        print(payload['collegeLeagues'])

    context = {'API_KEY': settings.GOOGLE_MAPS_API_KEY,
               'colleges': colleges,
               'leagues': leagues,
               'positions': positions,
               'players': players,
               'jsData' : jsData
               }

    return render(request, 'map/index.html', context)

def about(request):
    return render(request, 'map/about.html')
