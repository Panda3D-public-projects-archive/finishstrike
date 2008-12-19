from django.conf.urls.defaults import *
from anpr.views import *
from django.conf import settings
from anpr.models import Person

# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
#admin.autodiscover()

people_extra_context = {
 'people_length': len(Person.objects.all())
}

urlpatterns = patterns('',
    (r'^$', index),
    (r'^site_media/(.*)$', 'django.views.static.serve', 
                     {'document_root': settings.MEDIA_ROOT}),

    # Example:
    # (r'^anpr/', include('anpr.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/(.*)', admin.site.root),

    #Person url's
    (r'^person/list/?$', 'anpr_project.anpr.views.person_list'),
    (r'^person/create/?$', 'django.views.generic.create_update.create_object',
                    dict({'model': Person, 
                          'template_name': 'person/person_form.html'}, 
                          extra_context=people_extra_context,
                          post_save_redirect="/person/list/") ),

    (r'^person/update/(?P<object_id>\d+)/?$', 
      'django.views.generic.create_update.update_object',
      dict({'model': Person,
            'template_name': 'person/person_form.html'},
            extra_context=people_extra_context)),

    (r'^person/delete/(?P<object_id>\d+)/?$',
      'django.views.generic.create_update.delete_object',
      dict({'model': Person, 
            'template_name': 'person/person_confirm_delete.html'}, 
            extra_context=people_extra_context,
            post_delete_redirect="/person/list/")),

   # XXX - it is not required for now.
   # (r'^person/search/$','anpr_project.anpr.views.search'),

)
