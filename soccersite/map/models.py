from django.db import models
from django.conf import settings
# Create your models here.

class RosterMasterData(models.Model):
	rosterYear = models.IntegerField()
	playerNumber = models.IntegerField()
	firstName = models.CharField(max_length = 50)
	lastName = models.CharField(max_length = 50)
	year = models.CharField(max_length = 10)
	position1 = models.CharField(max_length = 20)
	height = models.CharField(max_length = 10)
	weight = models.IntegerField()
	homeTown = models.CharField(max_length = 30)
	stateOrCountry = models.CharField(max_length = 20)
	highSchool = models.CharField(max_length = 100)
	alternativeSchool = models.CharField(max_length = 50)
	college = models.CharField(max_length = 50)
	collegeLeague = models.CharField(max_length = 50)
	bioLink = models.CharField(max_length = 100)
	isStarter = models.CharField(max_length = 1)
	accolade = models.CharField(max_length = 20)

class HighSchool(models.Model):
    city            = models.CharField(max_length = 30)
    instiution      = models.CharField(max_length = 100)
    stateOrProvince = models.CharField(max_length = 20)
    country         = models.CharField(max_length = 50)
    latitude        = models.DecimalField(max_digits = 10)
    longitude       = models.DecimalField(max_digits = 10)
    schoolType      = models.CharField(max_length = 20)
