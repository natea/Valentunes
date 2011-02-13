from django.conf.urls.defaults import *
from piston.resource import Resource
from vt.api.handlers import CardHandler
# from vt.api.handlers import TaskHandler

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

card_handler = Resource(CardHandler)

urlpatterns = patterns('',
    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    (r'^api/$', card_handler),
    (r'^api/(?P<object_id>\d+)/$', card_handler),
    #TODO: this is insecure must fix before production
    (r'css/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': './css'}),
    (r'fonts/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': './fonts'}),
    (r'imgs/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': './imgs'}),
    (r'button/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': './button'}),
    (r'^v/', include('valentunes.urls')),        
    (r'^', include('valentunes.urls')),
)
