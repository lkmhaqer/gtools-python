# file: netdevice/views.py

from django.shortcuts import get_object_or_404, render, redirect

from netdevice.models import router, interface, logical_interface

from netdevice.forms import RouterForm, InterfaceForm, LogicalInterfaceForm


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
