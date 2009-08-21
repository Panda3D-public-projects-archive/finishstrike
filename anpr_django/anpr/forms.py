from anpr_django.anpr.models import *
from django import forms

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person

class CarForm(forms.ModelForm):
    class Meta:
        model = Car

class UploadCarImageForm(forms.Form):
    car_image = forms.ImageField()

