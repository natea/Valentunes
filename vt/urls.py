from django.conf.urls.defaults import *
from piston.resource import Resource
#from vt.api.handlers import CardHandler
#card_handler = Resource(CardHandler)
# from vt.api.handlers import TaskHandler

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from vt.valentunes.api import CardResource, TrackResource

card_resource = CardResource()
track_resource = TrackResource()

urlpatterns = patterns('',
    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    (r'^api/', include(card_resource.urls)),
    (r'^api/', include(track_resource.urls)),    
    # (r'^api/$', card_handler),
    # (r'^api/(?P<object_id>\d+)/$', card_handler),
)
