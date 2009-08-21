from django.conf.urls.defaults import *
from anpr.views import *
from django.conf import settings
from anpr.models import Person, Car
from anpr.forms import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

extra_context = {
 'people_length': len(Person.objects.all()),
 'car_length': len(Car.objects.all())
}

urlpatterns = patterns('',
    (r'^$', index),
    (r'^search/?$', search),
    (r'^report/?$', report),

    (r'^site_media/(.*)$', 'django.views.static.serve', 
                     {'document_root': settings.MEDIA_ROOT}),

    # Example:list_detail.object_list
#     (r'^anpr/', include('anpr.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
     (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/(.*)', admin.site.root),

    #Person url's
    (r'^person/list/?$', 'django.views.generic.list_detail.object_list',
      dict({'queryset': Person.objects.all(),
            'template_object_name': 'person',
            'paginate_by': 10,
            'template_name': 'person/person_list.html'},
            extra_context=extra_context)),

    (r'^person/view/(?P<object_id>\d+)/?$', 
                           'django.views.generic.list_detail.object_detail',
      dict({'queryset': Person.objects.all(),
            'template_object_name': 'person',
            'template_name': 'person/person_view.html'},
            extra_context=extra_context)),

    (r'^person/create/?$', 'django.views.generic.create_update.create_object',
      dict({'model': Person, 
            'template_name': 'person/person_form.html'}, 
            extra_context=extra_context,
            post_save_redirect="/person/list/") ),

    (r'^person/update/(?P<object_id>\d+)/?$', 
      'django.views.generic.create_update.update_object',
      dict({'model': Person,
            'template_name': 'person/person_form.html'},
            extra_context=extra_context,
            post_save_redirect="/person/view/%(id)s")),

    (r'^person/delete/(?P<object_id>\d+)/?$',
                        'django.views.generic.create_update.delete_object',
      dict({'model': Person, 
            'template_object_name': 'person',
            'template_name': 'person/person_confirm_delete.html'}, 
            extra_context=extra_context,
            post_delete_redirect="/person/list/")),

    # XXX - it is not required for now.
    # (r'^person/search/$','anpr_django.anpr.views.search'),

    # Car url's
    (r'^car/create/?$','django.views.generic.create_update.create_object',
      dict({'model': Car,
            'template_name': 'car/car_form.html'},
            extra_context=extra_context,
            post_save_redirect='/car/list/')),
    
    (r'^car/update/(?P<object_id>\d+)/?$', 
                        'django.views.generic.create_update.update_object',
      dict({'model': Car,
            'template_name': 'car/car_form.html'},
            extra_context=extra_context,
            post_save_redirect="/car/view/%(id)s")),

    (r'^car/delete/(?P<object_id>\d+)/?$',
                       'django.views.generic.create_update.delete_object',
      dict({'model':Car,
            'template_name': 'car/car_confirm_delete.html'},
            extra_context=extra_context,
            post_delete_redirect='car/list/')),

    (r'^car/list/?$', 'django.views.generic.list_detail.object_list',
      dict({'queryset': Car.objects.all(),
           'template_object_name': 'car',
           'paginate_by': 10,
    	     'template_name': 'car/car_list.html',},
    	    extra_context=extra_context)),

    (r'^car/view/(?P<object_id>\d+)/?$', 
                        'django.views.generic.list_detail.object_detail',
      dict({'queryset': Car.objects.all(),
            'template_object_name': 'car',
            'template_name': 'car/car_view.html'},
            extra_context=extra_context)),

    
)
