from django import forms
from .models import Documents
#import csv
class DocumentForm(forms.ModelForm):
    class Meta:
        model = Documents
        fields = ('description', 'document', )



class MHSForm(forms.Form):
    """
    class Meta:
        model = MatchedHighSchool
        fields = '__all__'
    """
    myfile = forms.FileField()

    """
    def save(self):
        records = csv.reader(self.cleaned_data["myfile"])
        #print("records: ", records)
        for line in records:
            input_data = MatchedHighSchool()
            input_data.rosterYear = self.cleaned_data['roster_year']
            #print("rosteryear: ", self.cleaned_data['roster_year'])
            input_data.playerNumber = self.cleaned_data['roster_data.player_Number']
            input_data.firstName = self.cleaned_data['first_name']
            input_data.lastName = self.cleaned_data['last_name']
            input_data.year = self.cleaned_data['year']
            input_data.position1 = self.cleaned_data['position1']
            input_data.height = self.cleaned_data['height']
            input_data.weight = self.cleaned_data['weight']
            input_data.homeTown = self.cleaned_data['home_town']
            input_data.stateOrCountry = self.cleaned_data['state_or_country']
            input_data.highSchool = self.cleaned_data['high_school']
            input_data.alternativeSchool = self.cleaned_data['alternative_school']
            input_data.college = self.cleaned_data['college']
            input_data.collegeLeague = self.cleaned_data['college_league']
            input_data.bioLink = self.cleaned_data['bio_link']
            input_data.isStarter = self.cleaned_data['is_starter']
            input_data.accolade = self.cleaned_data['accolade']
            input_data.matchedCity = self.cleaned_data['city']
            input_data.matchedInstitution = self.cleaned_data['institution']
            input_data.matchedStateProvince = self.cleaned_data['State/Province']
            input_data.matchedCountry = self.cleaned_data['country']
            input_data.latitude = self.cleaned_data['latitude']
            input_data.longitude = self.cleaned_data['longitude']
            input_data.schoolType = self.cleaned_data['Public/Private/International']
            input_data.save()
            """
