from django.shortcuts import render, redirect
from django.http import HttpResponse
from numpy import add
from .models import Bodega, Tienda
from .forms import BodegaForm, TiendaForm
import folium
import geocoder

# Create your views here.

def index(request):
    return render(request, "app/index.html")

def tiendas(request):
    return render(request, "tiendas/index.html")

def bodegas(request):
    # Create Map Object
    m = folium.Map(location=[-13.5252062,-71.9686264], zoom_start=13)

    # verificar si formulario fue completado
    if request.method == 'POST':
        form = BodegaForm(request.POST)
        # verficar validez de datos
        if form.is_valid():
            form.save()
            return redirect('./')
    #
    else:
        form = BodegaForm()
    # obtener direcciones
    address_set = Bodega.objects.all()
    for address in address_set:
        #if(address != None):
        location = geocoder.osm(address)
        lat = location.lat
        lng = location.lng
        name = address.address
        if lat == None or lng == None:
            address.delete()
            return HttpResponse('You address input is invalid')
        folium.Marker([lat, lng], tooltip='Click for more',
                  popup=name).add_to(m)
    
    # Get HTML Representation of Map Object
    m = m._repr_html_()
    context = {
        'm': m,
        'form': form,
        'lat': lat,
        'lng': lng,
    }
    return render(request, 'bodegas/index.html', context)
