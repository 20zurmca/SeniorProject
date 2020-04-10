from django.contrib import admin
from .models import RosterData, StarterData, AccoladeData, GroupedData, Documents

# Register your models here.
admin.site.register(RosterData)
admin.site.register(StarterData)
admin.site.register(AccoladeData)
admin.site.register(GroupedData)
admin.site.register(Documents)
