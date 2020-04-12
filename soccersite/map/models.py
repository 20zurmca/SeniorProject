from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import ArrayField
# Create your models here.

class RosterData(models.Model):
    rosterYear         = models.IntegerField()
    playerNumber       = models.CharField(max_length=10)
    firstName          = models.CharField(max_length=50)
    lastName           = models.CharField(max_length=50)
    year               = models.CharField(max_length=10)
    position1          = models.CharField(max_length=20)
    position2          = models.CharField(max_length=20)
    position3          = models.CharField(max_length=10)
    height             = models.CharField(max_length=10)
    weight             = models.IntegerField()
    homeTown           = models.CharField(max_length=30)
    stateOrCountry     = models.CharField(max_length=20)
    highSchool         = models.CharField(max_length=100)
    alternativeSchool  = models.CharField(max_length=50)
    college            = models.CharField(max_length=50)
    collegeLeague      = models.CharField(max_length=50)
    bioLink            = models.CharField(max_length=100)

class StarterData(models.Model):
    rosterYear      = models.IntegerField();
    number          = models.IntegerField();
    firstName       = models.CharField(max_length=50)
    lastName        = models.CharField(max_length=50)
    potentialStarts = models.IntegerField()
    GP              = models.IntegerField()
    GS              = models.IntegerField()
    isStarter       = models.CharField(max_length=1)
    college         = models.CharField(max_length=50)

class AccoladeData(models.Model):
    rosterYear = models.IntegerField()
    firstName  = models.CharField(max_length=50)
    lastName   = models.CharField(max_length=50)
    accolade   = models.CharField(max_length=20)
    college    = models.CharField(max_length=50)

class GroupedData(models.Model):
    firstName                 = models.CharField(max_length=50)
    lastName                  = models.CharField(max_length=50)
    homeTown                  = models.CharField(max_length=30)
    stateOrCountry            = models.CharField(max_length=20)
    highSchool                = models.CharField(max_length=100)
    alternativeSchool         = models.CharField(max_length=50)
    college                   = models.CharField(max_length=50)
    collegeLeague             = models.CharField(max_length=50)
    schoolType                = models.CharField(max_length=13, null=True)
    yearsStarter              = models.IntegerField()
    yearsAllConference        = models.IntegerField()
    latitude                  = models.FloatField()
    longitude                 = models.FloatField()
    highSchoolCity            = models.TextField(null=True)
    highSchoolSateOrProvince  = models.TextField(null=True)
    highSchoolCountry         = models.TextField(null=True)
    yearsOnRoster             = ArrayField(models.IntegerField())
    yearsPlayed               = ArrayField(models.CharField(max_length=50))
    positions                 = ArrayField(models.CharField(max_length=50))
    heights                   = ArrayField(models.CharField(max_length=5))
    weights                   = ArrayField(models.IntegerField())
    bioLinks                  = ArrayField(models.CharField(max_length=100))

#try for uploading csv
class Documents(models.Model):
    description = models.CharField(max_length=255, blank=True)
    rosterData = models.FileField(upload_to='documents/')
    starterData = models.FileField(upload_to='documents/')
    accolateData = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
