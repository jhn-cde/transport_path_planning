from django.contrib import admin
from .models import AlmacenPoint, TiendaPoint, PolygonLayer

# Register your models here.
admin.site.register(PolygonLayer)
admin.site.register(AlmacenPoint)
admin.site.register(TiendaPoint)
