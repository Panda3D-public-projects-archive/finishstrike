# Create your views here.
from django.http import HttpResponse, Http404
from django.template import Context
from django.template.loader import get_template
from django.contrib.auth.models import User
from django.template import Context
from django.shortcuts import render_to_response
from django.template import RequestContext
from anpr_project.anpr.models import Person
from anpr_project.anpr.forms import PersonForm

def index(request):
  context_instance=RequestContext(request)
  context_instance['people_length'] =  len(Person.objects.all())
  return render_to_response('index.html', locals(), context_instance)

