from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings

# Create your views here.

def index(request):
    context = {'API_KEY': settings.GOOGLE_MAPS_API_KEY}
    return render(request, 'map/index.html', context)
