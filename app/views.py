from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from numpy import add
from numpy.lib.shape_base import split
from .models import Bodega, Tienda, PolygonLayer, Address
from urllib.parse import urlencode
from .mixins import Directions, Markers
from .utils.voronoi import DiagramaVoronoi
from .utils.DistanciaMinima import MinDistancia
import requests
from djgeojson.serializers import Serializer as GeoJSONSerializer

from .mixins import Directions
# Create your views here.

def index(request):
    return render(request, "app/index.html")

def tiendas(request):
    # verificar si formulario fue completado
    if request.method == 'POST':
        address = request.POST['google_address']
        latlng = getlatlng(address, settings.GOOGLE_API_KEY)
        miTienda = Tienda()
        guardarObjeto(miTienda, latlng)
        return redirect('./')
    
    # obtener direcciones
    address_list = Markers(Tienda.objects.all())
    context = {
        'address_list': address_list,
        "google_api_key": settings.GOOGLE_API_KEY,
    }
    return render(request, 'app/tiendas.html', context)

def deltiendas(request):
    Tienda.objects.all().delete()
    return tiendas(request)

def almacenes(request):
    # verificar si formulario fue completado
    if request.method == 'POST':
        address = request.POST['google_address']
        latlng = getlatlng(address, settings.GOOGLE_API_KEY)
        miAlamacen = Bodega()
        guardarObjeto(miAlamacen, latlng)
        return redirect('./')
    
    # obtener direcciones
    address_list = Markers(Bodega.objects.all())
    context = {
        'address_list': address_list,
        "google_api_key": settings.GOOGLE_API_KEY,
    }
    return render(request, 'app/almacenes.html', context)

def delalmacenes(request):
    Bodega.objects.all().delete()
    return almacenes(request)

def resultado(request):
    d_almacenes = dict()
    for bodega in Bodega.objects.all():
        d_almacenes[bodega.address] = [bodega.lng, bodega.lat]
    if(len(d_almacenes) < 3):
        return almacenes(request)

    d_tiendas = dict()
    for tienda in Tienda.objects.all():
        d_tiendas[tienda.address] = [tienda.lng, tienda.lat]
    if(len(d_tiendas) == 0):
        return tiendas(request)

    diagramas_voronoi = DiagramaVoronoi(d_almacenes)
    regiones = diagramas_voronoi.regiones()
    PolygonLayer.objects.all().delete()
    for v in regiones:
        pol = PolygonLayer()
        pol.geom = v
        pol.save()
    #ser = GeoJSONSerializer().serialize('geojson', PolygonLayer.objects.all()[0], geometry_field='Polygon')

    ser = GeoJSONSerializer().serialize(PolygonLayer.objects.all(), use_natural_keys=False, with_modelname=False)

    rutas = []
    for alm in diagramas_voronoi.region_pts.keys():
        tiendas_por_region = diagramas_voronoi.puntos_por_region(d_tiendas, alm)
        ruta = [tiendas_por_region[0].replace(", ", "@")]
        ruta += [tiendas_por_region[i].replace(", ", "@") for i in range(1, len(tiendas_por_region))]
        rutas.append('()'.join(ruta))

    almacenes_list = Markers(Bodega.objects.all())
    tiendas_list = Markers(Tienda.objects.all())
    context = {
        'rutas_list': rutas,
        "google_api_key": settings.GOOGLE_API_KEY,
        "ser": ser,
        "tiendas_list": tiendas_list,
        "almacenes_list": almacenes_list
    }
    return render(request, "app/resultado.html", context)


def getlatlng(address, GOOGLE_API_KEY):
    tmp = address.split(",")
    try:
        lat = float(tmp[0])
        lng = float(tmp[1])
        ln = len(Bodega.objects.all())
        return {"address": "Almacen " + str(ln),"lat":lat, "lng":lng}
    except Exception:
        try:
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
            d = (response.json()['candidates'][0]["geometry"]['location'])
            d['address'] = address
            return d
        except (Exception):
            print("No se pudo obtener latlng", Exception)
            return {}

def guardarObjeto(objeto, latlng):
    try:
        objeto.address = latlng['address']
        objeto.lat = latlng['lat']
        objeto.lng = latlng['lng']
        objeto.save()
    except Exception:
        print("No se pudo guardar el objeto", Exception)
    
    