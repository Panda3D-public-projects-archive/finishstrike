from django.conf.urls.defaults import *
from anpr.views import *
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', index),
    (r'^site_media/(.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),

    # Example:
    # (r'^anpr/', include('anpr.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/(.*)', admin.site.root),

    #Person url's
    (r'^person/list/$','anpr_project.anpr.views.person_list'),
    (r'^person/add/$','anpr_project.anpr.views.person_add'),
    (r'^person/new/$','anpr_project.anpr.views.person_new'),
   
   # (r'^person/delete/$','anpr_project.anpr.views.delete'),
   # (r'^person/edit/$','anpr_project.anpr.views.edit'),
   # (r'^person/update/$','anpr_project.anpr.views.update'),
   # (r'^person/search/$','anpr_project.anpr.views.search'),

    




)
