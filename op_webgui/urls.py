# file: op_webgui/urls.py

from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

app_name = 'op_webgui'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^router/$', views.router_list, name='router_list'),
    url(r'^asn/$', views.asn_list, name='asn_list'),
    url(r'^create/aut_num/$', views.aut_num_create, name='aut_num_create'),
    url(r'^(?P<aut_num_id>[0-9]+)/edit/aut_num/$', views.aut_num_edit, name='aut_num_edit'),
    url(r'^(?P<aut_num_id>[0-9]+)/aut_num/$', views.aut_num_detail, name='aut_num_detail'),
    url(r'^(?P<router_id>[0-9]+)/create/bgp_neighbor/$', views.neighbor_create, name='neighbor_create'),
    url(r'^(?P<neighbor_id>[0-9]+)/edit/bgp_neighbor/$', views.neighbor_edit, name='neighbor_edit'),
    url(r'^(?P<router_id>[0-9]+)/create/ipv6_static/$', views.ipv6_static_create, name='ipv6_static_create'),
    url(r'^(?P<ipv6_static_id>[0-9]+)/edit/ipv6_static/$', views.ipv6_static_edit, name='ipv6_static_edit'),
    url(r'^(?P<router_id>[0-9]+)/create/ipv4_static/$', views.ipv4_static_create, name='ipv4_static_create'),
    url(r'^(?P<ipv4_static_id>[0-9]+)/edit/ipv4_static/$', views.ipv4_static_edit, name='ipv4_static_edit'),
    url(r'^(?P<logical_interface_id>[0-9]+)/create/ipv6_address/$', views.ipv6_address_create, name='ipv6_address_create'),
    url(r'^(?P<ipv6_address_id>[0-9]+)/edit/ipv6_address/$', views.ipv6_address_edit, name='ipv6_address_edit'),
    url(r'^(?P<logical_interface_id>[0-9]+)/create/ipv4_address/$', views.ipv4_address_create, name='ipv4_address_create'),
    url(r'^(?P<ipv4_address_id>[0-9]+)/edit/ipv4_address/$', views.ipv4_address_edit, name='ipv4_address_edit'),
    url(r'^(?P<router_id>[0-9]+)/create/interface/$', views.interface_create, name='interface_create'),
    url(r'^(?P<interface_id>[0-9]+)/edit/interface/$', views.interface_edit, name='interface_edit'),
    url(r'^(?P<interface_id>[0-9]+)/create/logical_interface/$', views.logical_interface_create, name='logical_interface_create'),
    url(r'^(?P<logical_interface_id>[0-9]+)/edit/logical_interface/$', views.logical_interface_edit, name='logical_interface_edit'),
    url(r'^create/router/$', views.router_create, name='router_create'),
    url(r'^(?P<router_id>[0-9]+)/edit/router/$', views.router_edit, name='router_edit'),
    url(r'^(?P<router_id>[0-9]+)/routers/$', views.router_detail, name='router_detail'),
    url(r'^(?P<router_id>[0-9]+)/config/$', views.router_config, name='router_config'),
]
