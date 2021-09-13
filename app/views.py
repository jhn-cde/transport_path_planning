from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from numpy import add
from .models import Bodega, Tienda
from urllib.parse import urlencode
from .mixins import Directions, Markers
from .utils.voronoi import DiagramaVoronoi
from .utils.DistanciaMinima import MinDistancia
import requests

from .mixins import Directions
# Create your views here.

def index(request):
    return render(request, "app/index.html")

def tiendas(request):
    # verificar si formulario fue completado
    if request.method == 'POST':
        address = request.POST['google_address']
        latlng = getlatlng(address, settings.GOOGLE_API_KEY)
        miAlamacen = Tienda()
        miAlamacen.address = address
        miAlamacen.lat = latlng['lat']
        miAlamacen.lng = latlng['lng']
        miAlamacen.save()
        return redirect('./')
    
    # obtener direcciones
    address_list = Markers(Tienda.objects.all())
    context = {
        'address_list': address_list,
        "google_api_key": settings.GOOGLE_API_KEY,
    }
    return render(request, 'app/tiendas.html', context)
    
def bodegas(request):
    # verificar si formulario fue completado
    if request.method == 'POST':
        address = request.POST['google_address']
        latlng = getlatlng(address, settings.GOOGLE_API_KEY)
        miAlamacen = Bodega()
        miAlamacen.address = address
        miAlamacen.lat = latlng['lat']
        miAlamacen.lng = latlng['lng']
        miAlamacen.save()
        return redirect('./')
    
    # obtener direcciones
    address_list = Markers(Bodega.objects.all())
    context = {
        'address_list': address_list,
        "google_api_key": settings.GOOGLE_API_KEY,
    }
    return render(request, 'app/bodegas.html', context)

def resultado(request):
    d_almacenes = dict()
    for bodega in Bodega.objects.all():
        d_almacenes[bodega.address] = [bodega.lng, bodega.lat]
    if(len(d_almacenes) < 3):
        return bodegas(request)

    d_tiendas = dict()
    for tienda in Tienda.objects.all():
        d_tiendas[tienda.address] = [tienda.lng, tienda.lat]
    if(len(d_tiendas) == 0):
        return tiendas(request)

    diagramas_voronoi = DiagramaVoronoi(d_almacenes)
    #print(d_almacenes)
    rutas = []
    for alm in diagramas_voronoi.region_pts.keys():
        tiendas_por_region = diagramas_voronoi.puntos_por_region(d_tiendas, alm)
        ruta = [tiendas_por_region[0].replace(", ", "@")]
        ruta += [tiendas_por_region[i].replace(", ", "@") for i in range(1, len(tiendas_por_region))]
        rutas.append('()'.join(ruta))
    
    context = {
        'rutas_list': rutas,
        "google_api_key": settings.GOOGLE_API_KEY,
    }
    return render(request, "app/resultado.html", context)


def getlatlng(address, GOOGLE_API_KEY):
    data_type = 'json'
    endpoint = f"https://maps.googleapis.com/maps/api/place/findplacefromtext/{data_type}"
    params = {"input":address.replace(', ', ',+'),
        "inputtype":"textquery", "fields":"formatted_address,name,rating,opening_hours,geometry",
        "key":GOOGLE_API_KEY}
    url_params = urlencode(params)

    url = f"{endpoint}?{url_params}"

    payload={}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    if response.status_code not in range(200, 299):
        return {}
    return(response.json()['candidates'][0]["geometry"]['location'])