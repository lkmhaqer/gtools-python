from django.shortcuts import get_object_or_404, render

from op_webgui.models import router

# Create your views here.

def index(request):
    context     = {}
    return render(request, 'config_gen/index.html', context)

def router_config(request, router_id):
    router_obj  = get_object_or_404(router, pk=router_id)
    router_list = router.objects.exclude(id=router_id)
    nos         = router_obj.network_os.name
    templates   = [
                  'config_gen/' + nos + '.config.html',
                  'config_gen/default.config.html',
                  ]
    context     = {
                  'router': router_obj,
                  'router_list': router_list,
                  }

    return render(request, templates, context)
