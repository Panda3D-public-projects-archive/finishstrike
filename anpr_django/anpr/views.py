# Create your views here.
from django.http import HttpResponse, Http404
from django.template import Context
from django.template.loader import get_template
from django.contrib.auth.models import User
from django.template import Context
from django.shortcuts import render_to_response
from django.template import RequestContext
from anpr_project.anpr.models import *
from anpr_project.anpr.forms import *

def index(request):
  return render_to_response('index.html', locals(),
                        context_instance=RequestContext(request))


def person_new(request):
    import pdb; pdb.set_trace()
    form = PersonForm()
    return render_to_response('person/form.html',{'form':form,'as_p':form.as_p},
                             context_instance=RequestContext(request))
    


def person_list(request):
    people = Person.objects.all()
    return render_to_response('person/list.html',{
        'people':people
    },
    context_instance=RequestContext(request)
    )
    

def person_add(request):
    if request.method == 'POST':
        personForm = PersonForm(request.POST)
        if personForm.is_valid():
            personForm.save()
            msg = 'Ok'
        else:
            msg = 'Error on registration.'

        return render_to_response('person/form.html',{'personForm':personform,
                                     'msg':msg})
    else:
         return HttpResponse("Form was not submitted.")

