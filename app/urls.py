from django.urls import path

from . import views

app_name = 'app'
urlpatterns = [
    path('', views.index, name='index'),
    path('almacenes/', views.almacenes, name='almacenes'),
    path('tiendas/', views.tiendas, name='tiendas'),
    path('resultado/', views.resultado, name='resultado'),
    path('delalmacenes/', views.delalmacenes, name='delalmacenes'),
    path('deltiendas/', views.deltiendas, name='deltiendas'),
]