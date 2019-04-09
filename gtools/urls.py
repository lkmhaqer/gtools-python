from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^', include('op_webgui.urls')),
    url(r'^bgp/', include('bgp.urls')),
    url(r'^netdevice/', include('netdevice.urls')),
    url(r'^static_route/', include('static.urls')),
    url(r'^api/', include('api.urls')),
    url(r'^raw/', include('config_gen.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('django.contrib.auth.urls')),
]
