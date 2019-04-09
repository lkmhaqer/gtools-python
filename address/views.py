# file: address/views.py

from django.shortcuts import get_object_or_404, render, redirect

from address.models import ipv6_address, ipv4_address
from netdevice.models import router, interface, logical_interface

from address.forms import IPv6AddressForm, IPv4AddressForm


def ipv6_address_create(request, logical_interface_id):
    logical_interface_obj = get_object_or_404(logical_interface, pk=logical_interface_id)
    if request.method == "POST":
        form = IPv6AddressForm(request.POST)
        if form.is_valid():
            ipv6_address_obj = form.save()
            return redirect('netdevice:router_detail', router_id=ipv6_address_obj.interface.interface.router.pk)
    else:
        form = IPv6AddressForm(initial={'interface': logical_interface_obj})
    return render(request, 'op_webgui/generic_edit.html', {'form': form})

def ipv6_address_edit(request, ipv6_address_id):
    ipv6_address_obj = get_object_or_404(ipv6_address, pk=ipv6_address_id)
    if request.method == "POST":
        form = IPv6AddressForm(request.POST, instance=ipv6_address_obj)
        if form.is_valid():
            ipv6_address_obj = form.save()
            return redirect('netdevice:router_detail', router_id=ipv6_address_obj.interface.interface.router.pk)
    else:
        form = IPv6AddressForm(instance=ipv6_address_obj)
    return render(request, 'op_webgui/generic_edit.html', {'form': form})

def ipv4_address_create(request, logical_interface_id):
    logical_interface_obj = get_object_or_404(logical_interface, pk=logical_interface_id)
    if request.method == "POST":
        form = IPv4AddressForm(request.POST)
        if form.is_valid():
            ipv4_address_obj = form.save()
            return redirect('netdevice:router_detail', router_id=ipv4_address_obj.interface.interface.router.pk)
    else:
        form = IPv4AddressForm(initial={'interface': logical_interface_obj})
    return render(request, 'op_webgui/generic_edit.html', {'form': form})

def ipv4_address_edit(request, ipv4_address_id):
    ipv4_address_obj = get_object_or_404(ipv4_address, pk=ipv4_address_id)
    if request.method == "POST":
        form = IPv4AddressForm(request.POST, instance=ipv4_address_obj)
        if form.is_valid():
            ipv4_address_obj = form.save()
            return redirect('netdevice:router_detail', router_id=ipv4_address_obj.interface.interface.router.pk)
    else:
        form = IPv4AddressForm(instance=ipv4_address_obj)
    return render(request, 'op_webgui/generic_edit.html', {'form': form})
