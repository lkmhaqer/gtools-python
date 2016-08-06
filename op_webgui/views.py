from django.shortcuts import get_object_or_404, render

from .models import router

def index(request):
    router_list = router.objects.order_by('hostname')
    context = {'router_list': router_list}
    return render(request, 'op_webgui/index.html', context)

def router_detail(request, router_id):
    router_obj = get_object_or_404(router, pk=router_id)
    return render(request, 'op_webgui/router.html', {'router': router_obj})
