# file: op_webgui/views.py

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404, render, redirect

from address.models import ipv6_address, ipv4_address
from bgp.models import aut_num, neighbor
from netdevice.models import router, interface, logical_interface
from static.models import ipv6_static, ipv4_static

from address.forms import IPv6AddressForm, IPv4AddressForm
from bgp.forms import ASNForm, NeighborForm
from netdevice.forms import RouterForm, InterfaceForm, LogicalInterfaceForm
from static.forms import IPv6StaticForm, IPv4StaticForm


def index(request):
    info                 = {}
    info['router_count'] = router.objects.count()
    info['asn_count']    = aut_num.objects.count()
    context = {'info': info}
    return render(request, 'op_webgui/index.html', context)

def router_list(request):
    router_list   = router.objects.order_by('hostname')
    router_count  = router_list.count()
    context       = {
                    'router_list':  router_list,
                    'router_count': router_count,
                    }
    return render(request, 'op_webgui/router_list.html', context)
