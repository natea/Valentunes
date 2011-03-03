from django.conf.urls.defaults import *

urlpatterns = patterns('django.views.generic.simple',
    (r'^about/$', 'direct_to_template', {'template': 'about.html'}),
    )
    
urlpatterns += patterns('valentunes.views',
    url('choose/(?P<cardid>[\d\w]+)/$', 'choose', name='choose'),
    url('playlist/(?P<cardid>[\d\w]+)/$', 'playlist', name='playlist'),
    url('gift/(?P<cardid>[\d\w]+)/$', 'gift', name='gift'),
    url('$', 'index', name='main_index'),
    )

