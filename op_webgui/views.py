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

def ipv6_static_create(request, router_id):
    router_obj = get_object_or_404(router, pk=router_id)
    if request.method == "POST":
        form = IPv6StaticForm(request.POST)
        if form.is_valid():
            ipv6_static_obj = form.save()
            return redirect('op_webgui:router_detail', router_id=ipv6_static_obj.router.pk)
    else:
        form = IPv6StaticForm(initial={'router': router_obj})
    return render(request, 'op_webgui/generic_edit.html', {'form': form})

def ipv6_static_edit(request, ipv6_static_id):
    ipv6_static_obj = get_object_or_404(ipv6_static, pk=ipv6_static_id)
    if request.method == "POST":
        form = IPv6StaticForm(request.POST, instance=ipv6_static_obj)
        if form.is_valid():
            ipv6_static_obj = form.save()
            return redirect('op_webgui:router_detail', router_id=ipv6_static_obj.router.pk)
    else:
        form = IPv6StaticForm(instance=ipv6_static_obj)
    return render(request, 'op_webgui/generic_edit.html', {'form': form})

def ipv4_static_create(request, router_id):
    router_obj = get_object_or_404(router, pk=router_id)
    if request.method == "POST":
        form = IPv4StaticForm(request.POST)
        if form.is_valid():
            ipv4_static_obj = form.save()
            return redirect('op_webgui:router_detail', router_id=ipv4_static_obj.router.pk)
    else:
        form = IPv4StaticForm(initial={'router': router_obj})
    return render(request, 'op_webgui/generic_edit.html', {'form': form})

def ipv4_static_edit(request, ipv4_static_id):
    ipv4_static_obj = get_object_or_404(ipv4_static, pk=ipv4_static_id)
    if request.method == "POST":
        form = IPv4StaticForm(request.POST, instance=ipv4_static_obj)
        if form.is_valid():
            ipv4_static_obj = form.save()
            return redirect('op_webgui:router_detail', router_id=ipv4_static_obj.router.pk)
    else:
        form = IPv4StaticForm(instance=ipv4_static_obj)
    return render(request, 'op_webgui/generic_edit.html', {'form': form})

def ipv6_address_create(request, logical_interface_id):
    logical_interface_obj = get_object_or_404(logical_interface, pk=logical_interface_id)
    if request.method == "POST":
        form = IPv6AddressForm(request.POST)
        if form.is_valid():
            ipv6_address_obj = form.save()
            return redirect('op_webgui:router_detail', router_id=ipv6_address_obj.interface.interface.router.pk)
    else:
        form = IPv6AddressForm(initial={'interface': logical_interface_obj})
    return render(request, 'op_webgui/generic_edit.html', {'form': form})

def ipv6_address_edit(request, ipv6_address_id):
    ipv6_address_obj = get_object_or_404(ipv6_address, pk=ipv6_address_id)
    if request.method == "POST":
        form = IPv6AddressForm(request.POST, instance=ipv6_address_obj)
        if form.is_valid():
            ipv6_address_obj = form.save()
            return redirect('op_webgui:router_detail', router_id=ipv6_address_obj.interface.interface.router.pk)
    else:
        form = IPv6AddressForm(instance=ipv6_address_obj)
    return render(request, 'op_webgui/generic_edit.html', {'form': form})

def ipv4_address_create(request, logical_interface_id):
    logical_interface_obj = get_object_or_404(logical_interface, pk=logical_interface_id)
    if request.method == "POST":
        form = IPv4AddressForm(request.POST)
        if form.is_valid():
            ipv4_address_obj = form.save()
            return redirect('op_webgui:router_detail', router_id=ipv4_address_obj.interface.interface.router.pk)
    else:
        form = IPv4AddressForm(initial={'interface': logical_interface_obj})
    return render(request, 'op_webgui/generic_edit.html', {'form': form})

def ipv4_address_edit(request, ipv4_address_id):
    ipv4_address_obj = get_object_or_404(ipv4_address, pk=ipv4_address_id)
    if request.method == "POST":
        form = IPv4AddressForm(request.POST, instance=ipv4_address_obj)
        if form.is_valid():
            ipv4_address_obj = form.save()
            return redirect('op_webgui:router_detail', router_id=ipv4_address_obj.interface.interface.router.pk)
    else:
        form = IPv4AddressForm(instance=ipv4_address_obj)
    return render(request, 'op_webgui/generic_edit.html', {'form': form})

def interface_create(request, router_id):
    router_obj = get_object_or_404(router, pk=router_id)
    if request.method == "POST":
        form = InterfaceForm(request.POST)
        if form.is_valid():
            interface_obj = form.save()
            return redirect('op_webgui:router_detail', router_id=interface_obj.router.pk)
    else:
        form = InterfaceForm(initial={'router': router_obj})
    return render(request, 'op_webgui/generic_edit.html', {'form': form})

def interface_edit(request, interface_id):
    interface_obj = get_object_or_404(interface, pk=interface_id)
    if request.method == "POST":
        form = InterfaceForm(request.POST, instance=interface_obj)
        if form.is_valid():
            interface_obj = form.save()
            return redirect('op_webgui:router_detail', router_id=interface_obj.router.pk)
    else:
        form = InterfaceForm(instance=interface_obj)
    return render(request, 'op_webgui/generic_edit.html', {'form': form})

def logical_interface_create(request, interface_id):
    interface_obj = get_object_or_404(interface, pk=interface_id)
    if request.method == "POST":
        form = LogicalInterfaceForm(request.POST)
        if form.is_valid():
            logical_interface_obj = form.save()
            return redirect('op_webgui:router_detail', router_id=logical_interface_obj.interface.router.pk)
    else:
        form = LogicalInterfaceForm(initial={'interface': interface_obj})
    return render(request, 'op_webgui/generic_edit.html', {'form': form})

def logical_interface_edit(request, logical_interface_id):
    logical_interface_obj = get_object_or_404(logical_interface, pk=logical_interface_id)
    if request.method == "POST":
        form = LogicalInterfaceForm(request.POST, instance=logical_interface_obj)
        if form.is_valid():
            logical_interface_obj = form.save()
            return redirect('op_webgui:router_detail', router_id=logical_interface_obj.interface.router.pk)
    else:
        form = LogicalInterfaceForm(instance=logical_interface_obj)
    return render(request, 'op_webgui/generic_edit.html', {'form': form})
