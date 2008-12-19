# Create your views here.
from django.http import HttpResponse, Http404
from django.template import Context
from django.template.loader import get_template
from django.contrib.auth.models import User
from django.template import Context
from django.shortcuts import render_to_response
from django.template import RequestContext
from anpr_project.anpr.models import Person, Car
from anpr_project.anpr.forms import PersonForm

def index(request):
  context_instance=RequestContext(request)
  context_instance['people_length'] =  len(Person.objects.all())
  context_instance['car_length'] = len(Car.objects.all())
  return render_to_response('index.html', locals(), context_instance)

def car_list(request):
    cars = Car.objects.all()
    return render_to_response('car/car_list.html', \
           {'cars':cars, 'cars_length':len(cars)},\
           context_instance=RequestContext(request))


