# file: op_webgui/admin.py

from django.contrib import admin

from .models import ipv6_address, ipv4_address, logical_interface, interface, neighbor, router, network_os, aut_num

# Register your models here.

admin.site.register(neighbor)
admin.site.register(router)
admin.site.register(network_os)
admin.site.register(aut_num)
admin.site.register(interface)
admin.site.register(logical_interface)
admin.site.register(ipv4_address)
admin.site.register(ipv6_address)
