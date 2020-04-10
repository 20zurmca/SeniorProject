from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import ArrayField
# Create your models here.

class RosterData(models.Model):
    rosterYear         = models.IntegerField(null=True)
    playerNumber       = models.CharField(max_length=10, null=True)
    firstName          = models.CharField(max_length=50, null=True)
    lastName           = models.CharField(max_length=50, null=True)
    year               = models.CharField(max_length=10, null=True)
    position1          = models.CharField(max_length=20, null=True)
    position2          = models.CharField(max_length=20, null=True)
    position3          = models.CharField(max_length=10, null=True)
    height             = models.CharField(max_length=10, null=True)
    weight             = models.IntegerField(null=True)
    homeTown           = models.CharField(max_length=30, null=True)
    stateOrCountry     = models.CharField(max_length=20, null=True)
    highSchool         = models.CharField(max_length=100, null=True)
    alternativeSchool  = models.CharField(max_length=50, null=True)
    college            = models.CharField(max_length=50, null=True)
    collegeLeague      = models.CharField(max_length=50, null=True)
    bioLink            = models.CharField(max_length=100, null=True)

class StarterData(models.Model):
    rosterYear      = models.IntegerField(null=True);
    number          = models.IntegerField(null=True);
    firstName       = models.CharField(max_length=50, null=True)
    lastName        = models.CharField(max_length=50, null=True)
    potentialStarts = models.IntegerField(null=True)
    GP              = models.IntegerField(null=True)
    GS              = models.IntegerField(null=True)
    isStarter       = models.CharField(max_length=1, null=True)
    college         = models.CharField(max_length=50, null=True)

class AccoladeData(models.Model):
    rosterYear = models.IntegerField(null=True)
    firstName  = models.CharField(max_length=50, null=True)
    lastName   = models.CharField(max_length=50, null=True)
    accolade   = models.CharField(max_length=20, null=True)
    college    = models.CharField(max_length=50, null=True)

class GroupedData(models.Model):
    firstName                 = models.CharField(max_length=50, null=True)
    lastName                  = models.CharField(max_length=50, null=True)
    homeTown                  = models.CharField(max_length=30, null=True)
    stateOrCountry            = models.CharField(max_length=20, null=True)
    highSchool                = models.CharField(max_length=100, null=True)
    alternativeSchool         = models.CharField(max_length=50, null=True)
    college                   = models.CharField(max_length=50, null=True)
    collegeLeague             = models.CharField(max_length=50, null=True)
    highSchoolCity            = models.TextField(null=True)
    highSchoolSateOrProvince  = models.TextField(null=True)
    highSchoolCountry         = models.TextField(null=True)
    schoolType                = models.CharField(max_length=13, null=True)
    yearsStarter              = models.IntegerField(null=True)
    yearsAllConference        = models.IntegerField(null=True)
    latitude                  = models.FloatField(null=True)
    longitude                 = models.FloatField(null=True)
    yearsOnRoster             = ArrayField(models.IntegerField(null=True))
    yearsPlayed               = ArrayField(models.CharField(max_length=50, null=True))
    positions                 = ArrayField(models.CharField(max_length=50, null=True))
    heights                   = ArrayField(models.CharField(max_length=5, null=True))
    weights                   = ArrayField(models.IntegerField(null=True))
    bioLinks                  = ArrayField(models.CharField(max_length=100, null=True))

#try for uploading csv
class Documents(models.Model):
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
