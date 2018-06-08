# file: api/urls.py

from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from api import views

app_name = 'api'
urlpatterns = [
    url(
        r'^routers/$',
        views.RouterList.as_view(),
        name='routers'
       ),
    url(
        r'^routers/(?P<pk>[0-9]+)/$',
        views.RouterDetail.as_view(),
        name='routers_detail'
       ),
    url(
        r'^nos/$',
        views.NetworkOsList.as_view(),
        name='network_os'
       ),
    url(
        r'^nos/(?P<pk>[0-9]+)/$',
        views.NetworkOsDetail.as_view(),
        name='network_os_detail'
       ),
    url(
        r'^interfaces/$',
        views.InterfaceList.as_view(),
        name='interfaces'
       ),
    url(
        r'^interfaces/(?P<pk>[0-9]+)/$',
        views.InterfaceDetail.as_view(),
        name='interfaces_detail'
       ),
    url(
        r'^logical_interfaces/$',
        views.LogicalInterfaceList.as_view(),
        name='logical_interfaces'
       ),
    url(
        r'^logical_interfaces/(?P<pk>[0-9]+)/$',
        views.LogicalInterfaceDetail.as_view(),
        name='logical_interfaces_detail'
       ),
    url(
        r'^ipv6_address/$',
        views.Ipv6AddressList.as_view(),
        name='ipv6_address'),
    url(
        r'^ipv6_address/(?P<pk>[0-9]+)/$',
        views.Ipv6AddressDetail.as_view(),
        name='ipv6_address_detail'
       ),
    url(
        r'^ipv4_address/$',
        views.Ipv4AddressList.as_view(),
        name='ipv4_address'
       ),
    url(
        r'^ipv4_address/(?P<pk>[0-9]+)/$',
        views.Ipv4AddressDetail.as_view(),
        name='ipv4_address_detail'
       ),
    url(
        r'^ipv6_static/$',
        views.Ipv6StaticList.as_view(),
        name='ipv6_static'
       ),
    url(
        r'^ipv6_static/(?P<pk>[0-9]+)/$',
        views.Ipv6StaticDetail.as_view(),
        name='ipv6_static_detail'
       ),
    url(
        r'^ipv4_static/$',
        views.Ipv4StaticList.as_view(),
        name='ipv4_static'
       ),
    url(
        r'^ipv4_static/(?P<pk>[0-9]+)/$',
        views.Ipv4StaticDetail.as_view(),
        name='ipv4_static_detail'
       ),
    url(
        r'^aut_num/$',
        views.AutNumList.as_view(),
        name='aut_num'
       ),
    url(
        r'^aut_num/(?P<pk>[0-9]+)/$',
        views.AutNumDetail.as_view(),
        name='aut_num_detail'
       ),
    url(
        r'^bgp_neighbor/$',
        views.NeighborList.as_view(),
        name='bgp_neighbor'
       ),
    url(
        r'^bgp_neighbor/(?P<pk>[0-9]+)/$',
        views.NeighborDetail.as_view(),
        name='bgp_neighbor_detail'
       ),
]

urlpatterns = format_suffix_patterns(urlpatterns)
