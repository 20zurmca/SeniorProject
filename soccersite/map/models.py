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




