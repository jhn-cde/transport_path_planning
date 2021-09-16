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
class PolygonLayer(models.Model):
    geom = PolygonField()

class AlmacenPoint(models.Model):
    name = models.CharField(max_length=200, null=True)
    markermodel = models.CharField(max_length=20, null=True)
    geom = PointField()

class TiendaPoint(models.Model):
    name = models.CharField(max_length=200, null=True)
    markermodel = models.CharField(max_length=20, null=True)
    geom = PointField()