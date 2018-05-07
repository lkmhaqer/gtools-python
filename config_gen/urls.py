# file: config_gen/urls.py

from django.conf.urls import url

from . import views

app_name = 'config_gen'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<router_id>[0-9]+)/$', views.router_config, name='router_config'),
]
