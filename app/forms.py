from typing import Type
from django import forms
from django.forms.widgets import NumberInput
from .models import Search


class SearchForm(forms.ModelForm):
    lat = forms.FloatField(label="", widget=forms.TextInput(attrs={'placeholder': 'latitud'}))
    lng = forms.FloatField(label="", widget=forms.TextInput(attrs={'placeholder': 'longitud'}))
    address = forms.CharField(label='')

    class Meta:
        model = Search
        fields = ['lat', 'lng', 'address',]
