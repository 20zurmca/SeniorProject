from django.contrib import admin
from .models import RosterData, StarterData, AccoladeData, GroupedData, Documents, HighSchoolData, HighSchoolMatchMaster

# Register your models here.
admin.site.register(RosterData)
admin.site.register(StarterData)
admin.site.register(AccoladeData)
admin.site.register(GroupedData)
admin.site.register(Documents)
admin.site.register(HighSchoolData)
admin.site.register(HighSchoolMatchMaster)
