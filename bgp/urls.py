# file: bgp/urls.py

from django.conf.urls import url
from django.contrib.auth import views as auth_views

from bgp import views

app_name = 'bgp'
urlpatterns = [
    url(
        r'^asn/$',
        views.asn_list,
        name='asn_list'
       ),
    url(
        r'^create/aut_num/$',
        views.aut_num_create,
        name='aut_num_create'
       ),
    url(
        r'^(?P<aut_num_id>[0-9]+)/edit/aut_num/$',
        views.aut_num_edit,
        name='aut_num_edit'
       ),
    url(
        r'^(?P<aut_num_id>[0-9]+)/aut_num/$',
        views.aut_num_detail,
        name='aut_num_detail'
       ),
    url(
        r'^(?P<router_id>[0-9]+)/create/bgp_neighbor/$',
        views.neighbor_create,
        name='neighbor_create'
       ),
    url(
        r'^(?P<neighbor_id>[0-9]+)/edit/bgp_neighbor/$',
        views.neighbor_edit,
        name='neighbor_edit'
       ),
]
