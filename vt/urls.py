from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

# as described in http://readthedocs.org/docs/django-tastypie/en/latest/api.html#quick-start
from tastypie.api import Api
from vt.valentunes.api import CardResource, TrackResource

card_resource = CardResource()
track_resource = TrackResource()

urlpatterns = patterns('',
    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^api/', include(card_resource.urls)),
    (r'^api/', include(track_resource.urls)),
    # as described in http://django-registration.readthedocs.org/en/latest/quickstart.html#setting-up-urls
    (r'^accounts/', include('registration.backends.default.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'static'}),
    (r'^v/', include('valentunes.urls')),        
    (r'', include('valentunes.urls')),
    # (r'^$', direct_to_template,
    #         { 'template': 'index.html' }, 'index'),
    #)
)
