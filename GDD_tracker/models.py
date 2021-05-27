from django.db import models
from django import forms
from django.forms import ModelForm

# Create your models here.

pests = [ 
    ("Armyworm", "Armyworm"),
    ("Cabbage Looper", "Cabbage Looper"),
    ("Corn Earworm", "Corn Earworm"),
    ("San Jose Scale", "San Jose Scale"),
    ("Two Spotted Mite", "Two Spotted Mite")
]

locations = [
    ("Amazonas","Amazonas"),
    ("Bonanza","Bonanza"),
    ("Bouganvilia","Bouganvilia"),
    ("Cengicaña","Cengicaña"),
    ("Costa Brava","Costa Brava"),
    ("El Balsamo","El Balsamo"),
    ("Escuintla Irlanda","Escuintla Irlanda"),
    ("La Giralta","La Giralta"),
    ("Mazatenango San Nico","Mazatenango San Nico"),
    ("Naranjales","Naranjales"),
    ("Petén oficina","Petén oficina"),
    ("Puyumate","Puyumate"),
    ("Retalhuleu Xoluta", "Retalhuleu Xoluta"),
    ("San Antonio del Valle","San Antonio del Valle"),
    ("San Rafael","San Rafael"),
    ("Santa Rosa La candelaria","Santa Rosa La candelaria"),
    ("Tehuantepeq","Tehuantepeq")
]

class Dates(models.Model):

    Date = models.DateTimeField()
    Pest = models.CharField(max_length=20, null=True, blank=True)
    Nearest_location = models.CharField(max_length=40, null=True, blank=True)
    T_min_celsius = models.IntegerField()
    T_max_celsius = models.IntegerField()
    GDD_Today = models.IntegerField()
    GDD_Acumulated = models.IntegerField()

class DateInput(forms.DateInput):
    input_type = 'date'

class Tracker(models.Model):

    Start_date = models.DateTimeField()
    Date = models.DateTimeField(null=True, blank=True)
    Pest = models.CharField(max_length=20, choices= pests)
    warning = models.CharField(max_length=150, null=True, blank=True)
    Nearest_location = models.CharField(max_length=40, choices= locations)

class TrackerForm(forms.ModelForm):

    class Meta:
        model = Tracker
        fields = ["Start_date","Pest", "Nearest_location"]
        widgets = {
            'Start_date': DateInput,
        }
