from django.contrib import admin

from .models import interface, neighbor, router, network_os, aut_num

# Register your models here.

admin.site.register(neighbor)
admin.site.register(router)
admin.site.register(network_os)
admin.site.register(aut_num)
admin.site.register(interface)
