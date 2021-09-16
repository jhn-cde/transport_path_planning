from django.contrib import admin
from .models import Almacen, AlmacenPoint, Tienda, TiendaPoint, PolygonLayer

# Register your models here.
admin.site.register(Almacen)
admin.site.register(Tienda)
admin.site.register(PolygonLayer)
admin.site.register(AlmacenPoint)
admin.site.register(TiendaPoint)
