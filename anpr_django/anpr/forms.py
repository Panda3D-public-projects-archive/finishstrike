from anpr_django.anpr.models import *
from django.forms import *

class PersonForm(ModelForm):
    class Meta:
        model = Person
