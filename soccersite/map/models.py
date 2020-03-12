from django.db import models

# Create your models here.
class HighSchool(models.Model):
    city           = models.CharField(max_length = 30)
    instiution     = models.CharField(max_length = 100)
    state_province = models.CharField(max_length = 20)
    country        = models.CharField(max_length = 50)
    latitude       = models.DecimalField(max_digits = 10)
    longitude      = models.DecimalField(max_digits = 10)
    type           = models.CharField(max_length = 20)
