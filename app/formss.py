from typing import Type
from django import forms
from django.forms.widgets import NumberInput
from .models import Bodega, Tienda

class BodegaForm(forms.ModelForm):
    address = forms.CharField(label='')

    class Meta:
        model = Bodega
        fields = ['address',]

class TiendaForm(forms.ModelForm):
    address = forms.CharField(label='')

    class Meta:
        model = Tienda
        fields = ['address',]