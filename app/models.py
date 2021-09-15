from ctypes import addressof
from django.db import models
from djgeojson.fields import PolygonField, PointField
# Create your models here.


"""class Search(models.Model):
    address = models.CharField(max_length=200, null=True)
    date = models.DateTimeField(auto_now_add=True)
    lat = models.FloatField(null=True)
    lng = models.FloatField(null=True)

    def __str__(self):
        return self.address
"""
class Address(models.Model):
    geom = PointField()

class PolygonLayer(models.Model):
    geom = PolygonField()
    
class Bodega(models.Model):
    address = models.CharField(max_length=200, null=True)
    lat = models.FloatField(null=True)
    lng = models.FloatField(null=True)
    def __str__(self):
        return self.address + '()' + str(self.lat) + '()' + str(self.lng)

class Tienda(models.Model):
    address = models.CharField(max_length=200, null=True)
    zone = models.CharField(max_length=200, null=True)
    lat = models.FloatField(null=True)
    lng = models.FloatField(null=True)
    def __str__(self):
        return self.address + '()' + str(self.lat) + '()' + str(self.lng)