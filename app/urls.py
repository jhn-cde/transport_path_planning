from django.urls import path

from . import views

app_name = 'app'
urlpatterns = [
    path('', views.index, name='index'),
    path('almacenes/', views.almacenes, name='almacenes'),
    path('delalmacenes/', views.delalmacenes, name='delalmacenes'),
    path('tiendas/', views.tiendas, name='tiendas'),
    path('deltiendas/', views.deltiendas, name='deltiendas'),
    path('resultado/', views.resultado, name='resultado'),
    path('delresultado/', views.delresultado, name='delresultado'),
]