# file: op_webgui/urls.py

from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

app_name = 'op_webgui'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^asn/$', views.asn, name='asn'),
    url(r'^create/aut_num/$', views.aut_num_create, name='aut_num_create'),
    url(r'^(?P<aut_num_id>[0-9]+)/edit/aut_num/$', views.aut_num_edit, name='aut_num_edit'),
    url(r'^(?P<aut_num_id>[0-9]+)/aut_num/$', views.aut_num_detail, name='aut_num_detail'),
    url(r'^(?P<router_id>[0-9]+)/create/ipv6_static/$', views.ipv6_static_create, name='ipv6_static_create'),
    url(r'^(?P<ipv6_static_id>[0-9]+)/edit/ipv6_static/$', views.ipv6_static_edit, name='ipv6_static_edit'),
    url(r'^(?P<router_id>[0-9]+)/create/ipv4_static/$', views.ipv4_static_create, name='ipv4_static_create'),
    url(r'^(?P<ipv4_static_id>[0-9]+)/edit/ipv4_static/$', views.ipv4_static_edit, name='ipv4_static_edit'),
    url(r'^create/router/$', views.router_create, name='router_create'),
    url(r'^(?P<router_id>[0-9]+)/edit/router/$', views.router_edit, name='router_edit'),
    url(r'^(?P<router_id>[0-9]+)/routers/$', views.router_detail, name='router_detail'),
    url(r'^(?P<router_id>[0-9]+)/config/$', views.router_config, name='router_config'),
]
