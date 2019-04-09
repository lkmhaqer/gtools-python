# file: address/urls.py

from django.conf.urls import url
from django.contrib.auth import views as auth_views

from static import views


app_name = 'static'
urlpatterns = [
    url(
        r'^(?P<router_id>[0-9]+)/create/ipv6_static/$',
        views.ipv6_static_create,
        name='ipv6_static_create'
       ),
    url(
        r'^(?P<ipv6_static_id>[0-9]+)/edit/ipv6_static/$',
        views.ipv6_static_edit,
        name='ipv6_static_edit'
       ),
    url(
        r'^(?P<router_id>[0-9]+)/create/ipv4_static/$',
        views.ipv4_static_create,
        name='ipv4_static_create'
       ),
    url(
        r'^(?P<ipv4_static_id>[0-9]+)/edit/ipv4_static/$',
        views.ipv4_static_edit,
        name='ipv4_static_edit'
       ),
]
