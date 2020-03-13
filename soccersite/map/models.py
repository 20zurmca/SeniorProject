from django.db import models
from django.conf import settings
# Create your models here.

class RosterMasterData(models.Model):
	rosterYear = models.IntegerField()
	playerNumber = models.IntegerField(null = True)
	firstName = models.CharField(max_length = 50)
	lastName = models.CharField(max_length = 50)
	year = models.CharField(max_length = 10)
	position1 = models.CharField(max_length = 20)
	height = models.CharField(max_length = 10, null = True)
	weight = models.IntegerField(null = True)
	homeTown = models.CharField(max_length = 30, null = True)
	stateOrCountry = models.CharField(max_length = 20, null = True)
	highSchool = models.CharField(max_length = 100, null = True)
	alternativeSchool = models.CharField(max_length = 50, null = True)
	college = models.CharField(max_length = 50)
	collegeLeague = models.CharField(max_length = 50)
	bioLink = models.CharField(max_length = 100)
	isStarter = models.CharField(max_length = 1, null = True)
	accolade = models.CharField(max_length = 20, null = True)

class HighSchool(models.Model):
    city            = models.CharField(max_length = 30)
    institution     = models.CharField(max_length = 100)
    stateOrProvince = models.CharField(max_length = 20, null = True)
    country         = models.CharField(max_length = 50)
    latitude        = models.FloatField()
    longitude       = models.FloatField()
    schoolType      = models.CharField(max_length = 20)
