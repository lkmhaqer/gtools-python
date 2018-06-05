# file: api/urls.py

from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from api import views

app_name = 'api'
urlpatterns = [
    url(r'^routers/$', views.RouterList.as_view()),
    url(r'^routers/(?P<pk>[0-9]+)/$', views.RouterDetail.as_view()),
    url(r'^nos/$', views.NetworkOsList.as_view()),
    url(r'^nos/(?P<pk>[0-9]+)/$', views.NetworkOsDetail.as_view()),
    url(r'^interfaces/$', views.InterfaceList.as_view()),
    url(r'^interfaces/(?P<pk>[0-9]+)/$', views.InterfaceDetail.as_view()),
    url(r'^logical_interfaces/$', views.LogicalInterfaceList.as_view()),
    url(r'^logical_interfaces/(?P<pk>[0-9]+)/$', views.LogicalInterfaceDetail.as_view()),
    url(r'^ipv6_address/$', views.Ipv6AddressList.as_view()),
    url(r'^ipv6_address/(?P<pk>[0-9]+)/$', views.Ipv6AddressDetail.as_view()),
    url(r'^ipv4_address/$', views.Ipv4AddressList.as_view()),
    url(r'^ipv4_address/(?P<pk>[0-9]+)/$', views.Ipv4AddressDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
