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
]
