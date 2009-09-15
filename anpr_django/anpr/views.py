# Create your views here.
from django.http import HttpResponse, Http404
from django.template import Context
from django.template.loader import get_template
from django.contrib.auth.models import User
from django.template import Context
from django.shortcuts import render_to_response
from django.template import RequestContext
from anpr_django.anpr.models import Person, Car
from anpr_django.anpr.forms import PersonForm, UploadCarImageForm
from anpr_django.lib import anpr
import StringIO
from PIL import Image
import os
import commands

SAVE_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)),"../templates/car_images/")

def index(request):
  context_instance = RequestContext(request)
  context_instance['people_length'] =  len(Person.objects.all())
  context_instance['car_length'] = len(Car.objects.all())
  return render_to_response('index.html', locals(), context_instance)

def car_list(request):
  cars = Car.objects.all()
  return render_to_response('car/car_list.html', \
           {'cars':cars, 'cars_length':len(cars)},\
           context_instance=RequestContext(request))

def search(request):
  context_instance = RequestContext(request)
  context_instance['people_length'] =  len(Person.objects.all())
  context_instance['car_length'] = len(Car.objects.all())

  if request.method == 'POST':
    form = UploadCarImageForm(request.POST, request.FILES)
    if form.is_valid():
      print request
      return render_to_response('image.html', locals(), context_instance)
  else:
    form = UploadCarImageForm()
  return render_to_response('search.html', locals(), context_instance)

def report(request):
  image_name_list = [ i for i in os.listdir(SAVE_PATH) if i.endswith('.jpg')]
  for image_name in image_name_list:
    file_path = os.path.join(SAVE_PATH, image_name)
    print 'REMOVING %s' % file_path
    os.remove(file_path)
  car = None
  context_instance = RequestContext(request)
  context_instance['people_length'] =  len(Person.objects.all())
  context_instance['car_length'] = len(Car.objects.all())
  car_image = request.FILES['car_image']
  file_name = str(car_image)
  car_image_stringio = StringIO.StringIO(car_image.read())  
  car_image = Image.open(car_image_stringio)
  car_image.save(os.path.join(SAVE_PATH, file_name))

  anpr.SAVE = SAVE_PATH
  plate_text = anpr.main(car_image)
  car_query_set = Car.objects.all().filter(plate=plate_text)
  if len(car_query_set):
    car = car_query_set[0]

  image_dict = {'STEP01': [],
                'STEP02': [],
                'STEP03': [],
                'STEP04': [],
                'STEP05': []}

  for k in image_dict.keys():
    image_dict[k] = [image_name for image_name in image_name_list if image_name.startswith(k)]
  print image_dict    
  return render_to_response('report.html', 
                            {'car': car, 'image': file_name,
                             'image_dict' : image_dict}, context_instance)
 
