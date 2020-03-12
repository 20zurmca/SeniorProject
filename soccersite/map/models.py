from django.db import models
from django.conf import settings
# Create your models here.

class RosterMasterData(models.Model):
	rosterYear = models.IntegerField()
	playerNumber = models.IntegerField()
	firstName = models.CharField(maxlength = 50)
	lastName = models.CharField(maxlength = 50)
	year = models.CharField(maxlength = 10)
	position1 = models.CharField(maxlength = 20)
	height = models.CharField(maxlength = 10)
	weight = models.IntegerField()
	homeTown = models.CharField(maxlength = 30)
	stateOrCountry = models.CharField(maxlength = 20)
	highSchool = models.CharField(maxlength = 100)
	alternativeSchool = models.CharField(maxlength = 50)
	college = models.CharField(maxlength = 50)
	collegeLeague = models.CharField(maxlength = 50)
	bioLink = models.CharField(maxlength = 100)
	isStarter = models.CharField(maxlength = 1)
	accolade = models.CharField(maxlength = 20)

class HighSchool(models.Model):
    city            = models.CharField(max_length = 30)
    instiution      = models.CharField(max_length = 100)
    stateOrProvince = models.CharField(max_length = 20)
    country         = models.CharField(max_length = 50)
    latitude        = models.DecimalField(max_digits = 10)
    longitude       = models.DecimalField(max_digits = 10)
    schoolType      = models.CharField(max_length = 20)
