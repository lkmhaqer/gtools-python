from django.conf.urls import url

from . import views

app_name = 'op_webgui'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<router_id>[0-9]+)/routers/$', views.router_detail, name='router_detail'),
]
