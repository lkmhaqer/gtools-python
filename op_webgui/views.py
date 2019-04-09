# file: op_webgui/views.py

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404, render, redirect

from bgp.models import aut_num
from netdevice.models import router


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
