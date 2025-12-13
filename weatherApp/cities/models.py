from django.db import models

# Create your models here.
class City(models.Model):
    cityName = models.CharField(max_length=255)