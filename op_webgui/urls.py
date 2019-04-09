# file: op_webgui/urls.py

from django.conf.urls import url
from django.contrib.auth import views as auth_views

from op_webgui import views

app_name = 'op_webgui'
urlpatterns = [
    url(
        r'^$',
        views.index,
        name='index'
       ),
    url(
        r'^router/$',
        views.router_list,
        name='router_list'
       ),
]
