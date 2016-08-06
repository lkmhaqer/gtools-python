from django.shortcuts import get_object_or_404, render

from .models import router, aut_num

def index(request):
    router_list = router.objects.order_by('hostname')
    return render(request, 'op_webgui/index.html', {'router_list': router_list})

def asn(request):
    asn_list = aut_num.objects.order_by('asn')
    return render(request, 'op_webgui/asns.html', {'asn_list': asn_list})

def aut_num_detail(request, aut_num_id):
    aut_num_obj = get_object_or_404(aut_num, pk=aut_num_id)
    return render(request, 'op_webgui/aut_num.html', {'aut_num': aut_num_obj})

def router_detail(request, router_id):
    router_obj = get_object_or_404(router, pk=router_id)
    return render(request, 'op_webgui/router.html', {'router': router_obj})
