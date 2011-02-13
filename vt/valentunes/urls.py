from django.conf.urls.defaults import *

urlpatterns = patterns('valentunes.views',
    url('choose/(?P<cardid>[\d\w]+)/$', 'choose', name='choose'),
    url('$', 'index', name='main_index'),

    )
