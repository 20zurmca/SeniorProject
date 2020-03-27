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

    #this part is buggy, not working correctly with view. Thus, Xingwen commented it out
    """
    def __str__(self):
        val = str(' '.join([rosterYear, playerNumber, firstName, lastName,
		                    position1, height, weight, homeTown, stateOrCountry,
							highSchool, alternativeSchool, college, collegeLeague,
							bioLink, isStarter, accolade]))
        return val
    """

class HighSchool(models.Model):
    city            = models.CharField(max_length = 30)
    institution     = models.CharField(max_length = 100)
    stateOrProvince = models.CharField(max_length = 20, null = True)
    country         = models.CharField(max_length = 50)
    latitude        = models.FloatField()
    longitude       = models.FloatField()
    schoolType      = models.CharField(max_length = 20)

    def __str__(self):
        val = str(' '.join([city, institution, stateOrProvince, country,
		                    latitude, longitude, schoolType]))
        return val

class BoardingSchool(models.Model):
    name      = models.CharField(max_length = 100)
    state     = models.CharField(max_length = 2)
    latitude  = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        val = str(' '.join([name, address, state, latitude, longitude]))
        return val
