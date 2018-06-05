# file: api/urls.py

from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from .views import RouterList, RouterDetail, NetworkOsList, NetworkOsDetail

app_name = 'api'
urlpatterns = [
    url(r'^routers/$', RouterList.as_view()),
    url(r'^routers/(?P<pk>[0-9]+)/$', RouterDetail.as_view()),
    url(r'^nos/$', NetworkOsList.as_view()),
    url(r'^nos/(?P<pk>[0-9]+)/$', NetworkOsDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
