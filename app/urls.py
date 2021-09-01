from django.urls import path

from . import views

app_name = 'app'
urlpatterns = [
    #path('', views.index, name='index'),
    path('', views.bodegas, name='bodegas'),
    path('tiendas/', views.tiendas, name='tiendas'),
]