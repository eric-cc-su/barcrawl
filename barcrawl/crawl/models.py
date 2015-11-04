from django.db import models

# Create your models here.
class City(models.Model):
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    date = models.DateField(auto_now=True)

class Bar(models.Model):
    city = models.ForeignKey('City')
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    lat = models.FloatField(default=0.0)
    lng = models.FloatField(default=0.0)

class Distance(models.Model):
    start = models.ForeignKey('City', related_name="start")
    end = models.ForeignKey('City', related_name="end")
    distance = models.PositiveIntegerField()