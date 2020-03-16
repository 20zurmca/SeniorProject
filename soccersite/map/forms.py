from django import forms
from .models import RosterMasterData

colleges  = RosterMasterData.objects.values_list('college', flat=True).distinct().order_by('college')
leagues   = RosterMasterData.objects.values_list('collegeLeague', flat=True).distinct().order_by('collegeLeague')
positions = RosterMasterData.objects.values_list('position1', flat=True).distinct().order_by('position1')

LEAGUE_CHOICES   = ()
COLLEGE_CHOICES  = ()
POSITION_CHOICES = ()

for i in range(len(leagues)):
    LEAGUE_CHOICES += (i+1, leagues[i])

for i in range(len(colleges)):
    COLLEGE_CHOICES += (i+1, colleges[i])

for i in range(len(positions)):
    POSITION_CHOICES += (i+1, positions[i])

STARTER_CHOICES        = (("1", "0"), ("2", "1"), ("3", "2"), ("4", "3"), ("5", "4+"))
ALL_CONFERENCE_CHOICES = STARTER_CHOICES
print(LEAGUE_CHOICES)
class FilterForm(forms.Form):
    collegeLeague      = forms.MultipleChoiceField(required=False, label="collegeLeague", choices=LEAGUE_CHOICES)
    college            = forms.MultipleChoiceField(required=False, label="college", choices=COLLEGE_CHOICES)
    position           = forms.MultipleChoiceField(required=False, label="position", choices=POSITION_CHOICES)
    starterYears       = forms.MultipleChoiceField(required=False, label="starterYears", choices=STARTER_CHOICES)
    allConferenceYears = forms.MultipleChoiceField(required=False, label="allConferenceYears", choices=ALL_CONFERENCE_CHOICES)
