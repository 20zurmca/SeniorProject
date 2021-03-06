from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about', views.about, name='about'),
    path('upload', views.upload_file, name='upload_file'),
    path('restore', views.restore, name='restore_db'),
    path('manualupload', views.manualupload, name='manualupload')
]
