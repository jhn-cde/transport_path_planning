from django.shortcuts import render, redirect
from django.http import HttpResponse
from numpy import add
from .models import Search
from .forms import SearchForm
import folium
import geocoder

# Create your views here.

def index(request):
    return render(request, "app/index.html")

def bodegas(request):
    # Create Map Object
    m = folium.Map(location=[-13.5299334,-71.9742687], zoom_start=13)

    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('./')
    else:
        form = SearchForm()
    address = Search.objects.all().last()
    if(address != None):
        location = geocoder.osm(address)
        lat = location.lat
        lng = location.lng
        country = location.country
        if lat == None or lng == None:
            address.delete()
            return HttpResponse('You address input is invalid')
        folium.Marker([lat, lng], tooltip='Click for more',
                  popup=country).add_to(m)
    
    # Get HTML Representation of Map Object
    m = m._repr_html_()
    context = {
        'm': m,
        'form': form,
    }
    return render(request, 'bodegas/index.html', context)
