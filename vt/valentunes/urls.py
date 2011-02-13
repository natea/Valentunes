from django.conf.urls.defaults import *

urlpatterns = patterns('valentunes.views',
    url('choose/$', 'choose', name='choose'),
    url('$', 'index', name='main_index'),

    )
