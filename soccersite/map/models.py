from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import ArrayField
import os
# Create your models here.

class RosterData(models.Model):
    roster_year         = models.IntegerField(null=True)
    player_number       = models.CharField(max_length=10, null=True)
    first_name          = models.CharField(max_length=50, null=True)
    last_name           = models.CharField(max_length=50, null=True)
    year                = models.CharField(max_length=10, null=True)
    position1           = models.CharField(max_length=20, null=True)
    position2           = models.CharField(max_length=20, null=True)
    position3           = models.CharField(max_length=10, null=True)
    height              = models.CharField(max_length=10, null=True)
    weight              = models.IntegerField(null=True)
    home_town           = models.CharField(max_length=30, null=True)
    state_or_country    = models.CharField(max_length=20, null=True)
    high_school         = models.CharField(max_length=100, null=True)
    alternative_school  = models.CharField(max_length=50, null=True)
    college             = models.CharField(max_length=50, null=True)
    college_league      = models.CharField(max_length=50, null=True)
    bio_link            = models.CharField(max_length=100, null=True)

class StarterData(models.Model):
    roster_year      = models.IntegerField(null=True);
    number           = models.IntegerField(null=True);
    first_name       = models.CharField(max_length=50, null=True)
    last_name        = models.CharField(max_length=50, null=True)
    potential_starts = models.IntegerField(null=True)
    gp               = models.IntegerField(null=True)
    gs               = models.IntegerField(null=True)
    is_starter       = models.CharField(max_length=1, null=True)
    college          = models.CharField(max_length=50, null=True)

class AccoladeData(models.Model):
    roster_year = models.IntegerField(null=True)
    first_name  = models.CharField(max_length=50, null=True)
    last_name   = models.CharField(max_length=50, null=True)
    accolade    = models.CharField(max_length=20, null=True)
    college     = models.CharField(max_length=50, null=True)

class HighSchoolData(models.Model):
    city            = models.CharField(max_length=50, null=True)
    institution     = models.CharField(max_length=100, null=True)
    stateorprovince = models.CharField(max_length=20, null=True)
    country         = models.CharField(max_length=50, null=True)
    latitude        = models.FloatField(null=True)
    longitude       = models.FloatField(null=True)
    school_type     = models.CharField(max_length=20, null=True)

class GroupedData(models.Model):
    first_name                   = models.CharField(max_length=50, null=True)
    last_name                    = models.CharField(max_length=50, null=True)
    home_town                    = models.CharField(max_length=30, null=True)
    state_or_country             = models.CharField(max_length=20, null=True)
    high_school                  = models.CharField(max_length=100, null=True)
    alternative_school           = models.CharField(max_length=50, null=True)
    college                      = models.CharField(max_length=50, null=True)
    college_league               = models.CharField(max_length=50, null=True)
    highschoolcity               = models.TextField(null=True)
    highschoolstateorprovince    = models.TextField(null=True)
    highschoolcountry            = models.TextField(null=True)
    school_type                  = models.CharField(max_length=13, null=True)
    starter_count                = models.IntegerField(null=True)
    accolade_count               = models.IntegerField(null=True)
    latitude                     = models.FloatField(null=True)
    longitude                    = models.FloatField(null=True)
    roster_year                  = ArrayField(models.IntegerField(null=True))
    year                         = ArrayField(models.CharField(max_length=50, null=True))
    position                     = ArrayField(models.CharField(max_length=50, null=True))
    heights                      = ArrayField(models.CharField(max_length=5, null=True))
    weights                      = ArrayField(models.IntegerField(null=True))
    bio_link                     = ArrayField(models.CharField(max_length=100, null=True))

class HighSchoolMatchMaster(models.Model):
    roster_year        = models.IntegerField(null=True)
    player_number      = models.CharField(max_length=10, null=True)
    first_name         = models.CharField(max_length=50, null=True)
    last_name          = models.CharField(max_length=50, null=True)
    year               = models.CharField(max_length=10, null=True)
    position1          = models.CharField(max_length=20, null=True)
    height             = models.CharField(max_length=10, null=True)
    weight             = models.IntegerField(null=True)
    home_town          = models.CharField(max_length=30, null=True)
    state_or_country   = models.CharField(max_length=20, null=True)
    high_school        = models.CharField(max_length=100, null=True)
    alternative_school = models.CharField(max_length=50, null=True)
    college            = models.CharField(max_length=50, null=True)
    college_league     = models.CharField(max_length=50, null=True)
    bio_link           = models.CharField(max_length=100, null=True)
    is_starter         = models.CharField(max_length=1, null=True)
    accolade           = models.CharField(max_length=20, null=True, blank=True)
    city               = models.CharField(max_length=30, null=True)
    institution        = models.CharField(max_length=100, null=True)
    stateorprovince    = models.CharField(max_length=20, null=True)
    country            = models.CharField(max_length=50, null=True)
    latitude           = models.FloatField(null=True)
    longitude          = models.FloatField(null=True)
    school_type        = models.CharField(max_length=20, null=True)

class Documents(models.Model):
    description   = models.CharField(unique=True, max_length=255)
    rosterData    = models.FileField(upload_to='documents/', null=True)
    starterData   = models.FileField(upload_to='documents/', null=True)
    accoladeData  = models.FileField(upload_to='documents/', null=True)
    uploaded_at   = models.DateTimeField(auto_now_add=True)
    manual_upload = models.BooleanField(default=False, blank=True)


class BackUp(models.Model):
    description = models.CharField(unique=True, max_length=255)
    file        = models.FileField()
    uploaded_at = models.DateTimeField(auto_now_add=True)
    isCurrent   = models.BooleanField(default=False)
    isLoaded    = models.BooleanField(default=False)

    def filename(self):
        return os.path.basename(self.file.name)
