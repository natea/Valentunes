from django.conf.urls.defaults import *

urlpatterns = patterns('django.views.generic.simple',
    (r'^about/$', 'direct_to_template', {'template': 'about.html'}),
    )
    
urlpatterns += patterns('valentunes.views',
    url('choose/(?P<cardid>[\d\w]+)/$', 'choose', name='choose'),
    url('$', 'index', name='main_index'),
    )

