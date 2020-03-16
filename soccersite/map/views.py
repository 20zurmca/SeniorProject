from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from .models import RosterMasterData
from .forms import FilterForm

# Create your views here.

def index(request):
    colleges  = RosterMasterData.objects.values_list('college', flat=True).distinct().order_by('college')
    leagues   = RosterMasterData.objects.values_list('collegeLeague', flat=True).distinct().order_by('collegeLeague')
    positions = RosterMasterData.objects.values_list('position1', flat=True).distinct().order_by('position1')

    if request.method == 'POST':
        form  = FilterForm(request.POST)
        if(form.is_valid()):
            print(form.cleaned_data.get("collegeLeague"))
    else:
        form = FilterForm()

    context = {'API_KEY': settings.GOOGLE_MAPS_API_KEY,
               'colleges': colleges,
               'leagues': leagues,
               'positions': positions,
               'form': form }

    return render(request, 'map/index.html', context)
