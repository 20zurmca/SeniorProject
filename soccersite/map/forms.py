from django import forms
from .models import Documents
#import csv
class DocumentForm(forms.ModelForm):
    class Meta:
        model = Documents
        fields = ('description', 'rosterData', 'starterData','accoladeData', )
