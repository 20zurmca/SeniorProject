from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
GOOGLE_API_KEY = 'AIzaSyAH_r-WUtEbvF6_HAxLk9n5FF_6zJWImE4'

def index(request):
    context = {'API_KEY': GOOGLE_API_KEY}
    return render(request, 'map/index.html', context)
