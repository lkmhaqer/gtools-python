# file: netdevice/views.py

from django.shortcuts import get_object_or_404, render, redirect

from netdevice.models import router, interface, logical_interface, vrf

from netdevice.forms import RouterForm, InterfaceForm, LogicalInterfaceForm, VrfForm


def router_detail(request, router_id):
    router_obj     = get_object_or_404(router, pk=router_id)
    return render(request, 'netdevice/router.html', {'router': router_obj})

def router_create(request):
    if request.method == "POST":
        form = RouterForm(request.POST)
        if form.is_valid():
            router_obj = form.save()
            return redirect('netdevice:router_detail', router_id=router_obj.pk)
    else:
        form = RouterForm()
    return render(request, 'op_webgui/generic_edit.html', {'form': form})

def router_edit(request, router_id):
    router_obj = get_object_or_404(router, pk=router_id)
    if request.method == "POST":
        form = RouterForm(request.POST, instance=router_obj)
        if form.is_valid():
            router_obj = form.save()
            return redirect('netdevice:router_detail', router_id=router_obj.pk)
    else:
        form = RouterForm(instance=router_obj)
    return render(request, 'op_webgui/generic_edit.html', {'form': form})

def router_config(request, router_id):
    router_obj     = get_object_or_404(router, pk=router_id)
    router_list    = router.objects.exclude(id=router_id)
    nos            = router_obj.network_os.name
    template_name  = 'config_gen/' + nos + '.config.html'
    context        = {
                     'router':               router_obj,
                     'router_list':          router_list,
                     'router_template_name': template_name,
                     }

    return render(request, 'netdevice/router_config.html', context)

def vrf_list(request):
    vrf_list  = vrf.objects.order_by('target')
    vrf_count = vrf_list.count()
    context   = {
                'vrf_list':  vrf_list,
                'vrf_count': vrf_count,
                }
    return render(request, 'netdevice/vrf_list.html', context)

def vrf_detail(request, vrf_id):
    vrf_obj = get_object_or_404(vrf, pk=vrf_id)
    return render(request, 'netdevice/vrf.html', {'vrf': vrf_obj})

def vrf_create(request):
    if request.method == "POST":
        form = VrfForm(request.POST)
        if form.is_valid():
            vrf = form.save()
            return redirect('netdevice:vrf_detail', vrf_id=vrf.pk)
    else:
        form = VrfForm()
    return render(request, 'op_webgui/generic_edit.html', {'form': form})

def vrf_edit(request, vrf_id):
    vrf_obj = get_object_or_404(vrf, pk=vrf_id)
    if request.method == "POST":
        form = VrfForm(request.POST, instance=vrf_obj)
        if form.is_valid():
            vrf_obj = form.save()
            return redirect('netdevice:vrf_detail', vrf_id=vrf_obj.pk)
    else:
        form = VrfForm(instance=vrf_obj)
    return render(request, 'op_webgui/generic_edit.html', {'form': form})

def interface_create(request, router_id):
    router_obj = get_object_or_404(router, pk=router_id)
    if request.method == "POST":
        form = InterfaceForm(request.POST)
        if form.is_valid():
            interface_obj = form.save()
            return redirect('netdevice:router_detail', router_id=interface_obj.router.pk)
    else:
        form = InterfaceForm(initial={'router': router_obj})
    return render(request, 'op_webgui/generic_edit.html', {'form': form})

def interface_edit(request, interface_id):
    interface_obj = get_object_or_404(interface, pk=interface_id)
    if request.method == "POST":
        form = InterfaceForm(request.POST, instance=interface_obj)
        if form.is_valid():
            interface_obj = form.save()
            return redirect('netdevice:router_detail', router_id=interface_obj.router.pk)
    else:
        form = InterfaceForm(instance=interface_obj)
    return render(request, 'op_webgui/generic_edit.html', {'form': form})

def logical_interface_create(request, interface_id):
    interface_obj = get_object_or_404(interface, pk=interface_id)
    if request.method == "POST":
        form = LogicalInterfaceForm(request.POST)
        if form.is_valid():
            logical_interface_obj = form.save()
            return redirect('netdevice:router_detail', router_id=logical_interface_obj.interface.router.pk)
    else:
        form = LogicalInterfaceForm(initial={'interface': interface_obj})
    return render(request, 'op_webgui/generic_edit.html', {'form': form})

def logical_interface_edit(request, logical_interface_id):
    logical_interface_obj = get_object_or_404(logical_interface, pk=logical_interface_id)
    if request.method == "POST":
        form = LogicalInterfaceForm(request.POST, instance=logical_interface_obj)
        if form.is_valid():
            logical_interface_obj = form.save()
            return redirect('netdevice:router_detail', router_id=logical_interface_obj.interface.router.pk)
    else:
        form = LogicalInterfaceForm(instance=logical_interface_obj)
    return render(request, 'op_webgui/generic_edit.html', {'form': form})
