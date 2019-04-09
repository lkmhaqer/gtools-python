# file: address/urls.py

from django.conf.urls import url
from django.contrib.auth import views as auth_views

from address import views

app_name = 'address'
urlpatterns = [
    url(
        r'^(?P<logical_interface_id>[0-9]+)/create/ipv6_address/$',
        views.ipv6_address_create,
        name='ipv6_address_create'
       ),
    url(
        r'^(?P<ipv6_address_id>[0-9]+)/edit/ipv6_address/$',
        views.ipv6_address_edit,
        name='ipv6_address_edit'
       ),
    url(
        r'^(?P<logical_interface_id>[0-9]+)/create/ipv4_address/$',
        views.ipv4_address_create,
        name='ipv4_address_create'
       ),
    url(
        r'^(?P<ipv4_address_id>[0-9]+)/edit/ipv4_address/$',
        views.ipv4_address_edit,
        name='ipv4_address_edit'
       ),
]
