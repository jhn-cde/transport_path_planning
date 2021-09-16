from django.shortcuts import render, redirect
from django.conf import settings
from djgeojson.serializers import Serializer as GeoJSONSerializer
import json

from .models import Almacen, AlmacenPoint, Tienda, TiendaPoint, PolygonLayer
from .mixins import getlatlng, guardarObjeto, getDictCoords
from .utils.voronoi import DiagramaVoronoi
from .utils.DistanciaMinima import MinDistancia

# views
def index(request):
    return render(request, "app/index.html")

def tiendas(request):
    # verificar si formulario fue completado
    if request.method == 'POST':
        address = request.POST['google_address']
        # obtener latlng
        latlng = getlatlng(address, settings.GOOGLE_API_KEY)
        # añadir nombre
        if (latlng["address"] == ""):
            latlng["address"] = "Tienda " + str(len(Tienda.objects.all()))
        # guardar punto            
        tiendaPunto = TiendaPoint()
        guardarObjeto(tiendaPunto, latlng, "Tienda")
        # volver a cargar página
        return redirect('./')
    
    # obtener direcciones serializadas
    tieSer = GeoJSONSerializer().serialize(TiendaPoint.objects.all(), use_natural_keys=False, with_modelname=False)
    
    context = {
        "google_api_key": settings.GOOGLE_API_KEY,
        "tieSer": tieSer
    }
    return render(request, 'app/tiendas.html', context)

def deltiendas(request):
    Tienda.objects.all().delete()
    return tiendas(request)

def almacenes(request):
    # verificar si formulario fue completado
    if request.method == 'POST':
        address = request.POST['google_address']
        # obtener latlng
        latlng = getlatlng(address, settings.GOOGLE_API_KEY)
        # añadir nombre
        if (latlng["address"] == ""):
            latlng["address"] = "Almacen " + str(len(Almacen.objects.all()))
        # guardar punto
        almacenPunto = AlmacenPoint()
        guardarObjeto(almacenPunto, latlng, "Almacen")
        # volver a cargar página
        return redirect('./')
    
    # obtener direcciones serializadas
    almSer = GeoJSONSerializer().serialize(AlmacenPoint.objects.all(), use_natural_keys=False, with_modelname=False)
    
    context = {
        "google_api_key": settings.GOOGLE_API_KEY,
        "almSer": almSer
    }
    return render(request, 'app/almacenes.html', context)

def delalmacenes(request):
    Almacen.objects.all().delete()
    return almacenes(request)

def resultado(request):
    # obtener modelos serializados
    ser = GeoJSONSerializer().serialize(PolygonLayer.objects.all(), use_natural_keys=False, with_modelname=False)
    almSer = GeoJSONSerializer().serialize(AlmacenPoint.objects.all(), use_natural_keys=False, with_modelname=False)
    tieSer = GeoJSONSerializer().serialize(TiendaPoint.objects.all(), use_natural_keys=False, with_modelname=False)

    # preparar datos para voronoi
    d_almSer = getDictCoords(json.loads(almSer))
    d_tieSer = getDictCoords(json.loads(tieSer))

    # crear Diagramas de Voronoi
    print("* Generando diagramas de voronoi ...")
    diagramas_voronoi = DiagramaVoronoi(d_almSer)
    print("* Diagramas de Voronoi Generados")

    # Eliminar poligonos anteriores
    PolygonLayer.objects.all().delete()

    # generar nuevos poligonos
    print("\n* Generando poligonos - regiones")
    regiones = diagramas_voronoi.regiones()
    for v in regiones:
        pol = PolygonLayer()
        pol.geom = v
        pol.save()
    print("* Poligonos generados")

    print("\n* Generando rutas optimas")
    # Generar rutas
    d_rutas = {}
    for alm in diagramas_voronoi.region_pts.keys():
        # separar tiendas por regiones
        tiendas_por_region = diagramas_voronoi.puntos_por_region(d_tieSer, alm)
        nombre = tiendas_por_region[0]
        d_ruta = {"nombre": nombre, "coordenadas": [d_almSer[nombre]]}
        for i in range(1, len(tiendas_por_region)):
            nombre = tiendas_por_region[i]
            d_ruta['coordenadas'] += [d_tieSer[nombre]]

        # obtener rutas ordenadas
        mindist = MinDistancia(d_ruta)
        camino_minimo = mindist.CaminoMinimo() 
        print(camino_minimo)

        # generar dicionario de rutas
        d_rutas[camino_minimo['nombre']] = camino_minimo['coordenadas']
    print("* Rutas optimas generadas")

    # serializar rutas
    rutasSer = str(d_rutas).replace("'", '"')

    context = {
        "google_api_key": settings.GOOGLE_API_KEY,
        "ser": ser,
        "almSer": almSer,
        "tieSer": tieSer,
        "rutasSer": rutasSer
    }
    return render(request, "app/resultado.html", context)