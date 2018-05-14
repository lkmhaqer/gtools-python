from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^', include('op_webgui.urls')),
    url(r'^raw/', include('config_gen.urls')),
    url(r'^admin/', admin.site.urls),
]
