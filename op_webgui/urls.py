# file: op_webgui/urls.py

from django.conf.urls import url

from . import views

app_name = 'op_webgui'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^asn/$', views.asn, name='asn'),
    url(r'^(?P<aut_num_id>[0-9]+)/aut_num/$', views.aut_num_detail, name='aut_num_detail'),
    url(r'^(?P<router_id>[0-9]+)/routers/$', views.router_detail, name='router_detail'),
    url(r'^(?P<router_id>[0-9]+)/config/$', views.router_config, name='router_config'),
]
