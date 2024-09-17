# models.py in map_visualization app
from django.db import models

class CrimeData(models.Model):
    state_ut = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    year = models.IntegerField()
    rape = models.IntegerField()
    kidnapping_and_abduction = models.IntegerField()
    dowry_deaths = models.IntegerField()
    assault_on_women = models.IntegerField()
    insult_to_modesty = models.IntegerField()
    cruelty_by_husband = models.IntegerField()
    importation_of_girls = models.IntegerField()
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return f"{self.district}, {self.state_ut}"