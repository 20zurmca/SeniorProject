from django.contrib import admin
from .models import RosterMasterData, HighSchool, MatchedHighSchool

# Register your models here.
admin.site.register(RosterMasterData)
admin.site.register(HighSchool)

"""
@admin.register(MatchedHighSchool)
class MHSAdmin(admin.ModelAdmin):
    def MHS_actions(self, obj):
"""        
