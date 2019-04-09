# file: static/views.py

from django.shortcuts import get_object_or_404, render, redirect

from netdevice.models import router
from static.models import ipv6_static, ipv4_static

from static.forms import IPv6StaticForm, IPv4StaticForm


def ipv6_static_create(request, router_id):
    router_obj = get_object_or_404(router, pk=router_id)
    if request.method == "POST":
        form = IPv6StaticForm(request.POST)
        if form.is_valid():
            ipv6_static_obj = form.save()
            return redirect('netdevice:router_detail', router_id=ipv6_static_obj.router.pk)
    else:
        form = IPv6StaticForm(initial={'router': router_obj})
    return render(request, 'op_webgui/generic_edit.html', {'form': form})

def ipv6_static_edit(request, ipv6_static_id):
    ipv6_static_obj = get_object_or_404(ipv6_static, pk=ipv6_static_id)
    if request.method == "POST":
        form = IPv6StaticForm(request.POST, instance=ipv6_static_obj)
        if form.is_valid():
            ipv6_static_obj = form.save()
            return redirect('netdevice:router_detail', router_id=ipv6_static_obj.router.pk)
    else:
        form = IPv6StaticForm(instance=ipv6_static_obj)
    return render(request, 'op_webgui/generic_edit.html', {'form': form})

def ipv4_static_create(request, router_id):
    router_obj = get_object_or_404(router, pk=router_id)
    if request.method == "POST":
        form = IPv4StaticForm(request.POST)
        if form.is_valid():
            ipv4_static_obj = form.save()
            return redirect('netdevice:router_detail', router_id=ipv4_static_obj.router.pk)
    else:
        form = IPv4StaticForm(initial={'router': router_obj})
    return render(request, 'op_webgui/generic_edit.html', {'form': form})

def ipv4_static_edit(request, ipv4_static_id):
    ipv4_static_obj = get_object_or_404(ipv4_static, pk=ipv4_static_id)
    if request.method == "POST":
        form = IPv4StaticForm(request.POST, instance=ipv4_static_obj)
        if form.is_valid():
            ipv4_static_obj = form.save()
            return redirect('netdevice:router_detail', router_id=ipv4_static_obj.router.pk)
    else:
        form = IPv4StaticForm(instance=ipv4_static_obj)
    return render(request, 'op_webgui/generic_edit.html', {'form': form})
