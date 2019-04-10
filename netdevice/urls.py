# file: netdevice/urls.py

from django.conf.urls import url
from django.contrib.auth import views as auth_views

from netdevice import views


app_name = 'netdevice'
urlpatterns = [
    url(
        r'^create/router/$',
        views.router_create,
        name='router_create'
       ),
    url(
        r'^(?P<router_id>[0-9]+)/edit/router/$',
        views.router_edit,
        name='router_edit'
       ),
    url(
        r'^(?P<router_id>[0-9]+)/routers/$',
        views.router_detail,
        name='router_detail'
       ),
    url(
        r'^(?P<router_id>[0-9]+)/config/$',
        views.router_config,
        name='router_config'
       ),
    url(
        r'^vrf/$',
        views.vrf_list,
        name='vrf_list'
       ),
    url(
        r'^create/vrf/$',
        views.vrf_create,
        name='vrf_create'
       ),
    url(
        r'^(?P<vrf_id>[0-9]+)/edit/vrf/$',
        views.vrf_edit,
        name='vrf_edit'
       ),
    url(
        r'^(?P<vrf_id>[0-9]+)/vrf/$',
        views.vrf_detail,
        name='vrf_detail'
       ),
    url(
        r'^(?P<router_id>[0-9]+)/create/interface/$',
        views.interface_create,
        name='interface_create'
       ),
    url(
        r'^(?P<interface_id>[0-9]+)/edit/interface/$',
        views.interface_edit,
        name='interface_edit'
       ),
    url(
        r'^(?P<interface_id>[0-9]+)/create/logical_interface/$',
        views.logical_interface_create,
        name='logical_interface_create'
       ),
    url(
        r'^(?P<logical_interface_id>[0-9]+)/edit/logical_interface/$',
        views.logical_interface_edit,
        name='logical_interface_edit'
       ),
]
