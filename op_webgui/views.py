# file: op_webgui/views.py

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404, render, redirect

from netdevice.models import router
from static.models import ipv6_static, ipv4_static
from bgp.models import aut_num

from .forms import RouterForm, ASNForm, IPv6StaticForm, IPv4StaticForm

@login_required
def index(request):
    router_list   = router.objects.order_by('hostname')
    router_count  = router_list.count()
    context       = {
                    'router_list':  router_list,
                    'router_count': router_count,
                    }
    return render(request, 'op_webgui/index.html', context)

@login_required
def asn(request):
    asns      = aut_num.objects.order_by('asn')
    asn_count = asns.count()
    paginator = Paginator(asns, 20)
    page      = request.GET.get('page')

    try:
        asn_list = paginator.page(page)
    except PageNotAnInteger:
        asn_list = paginator.page(1)
    except EmptyPage:
        asn_list = paginator.page(paginator.num_pages)

    context = {
              'asn_list':  asn_list,
              'asn_count': asn_count,
              }

    return render(request, 'op_webgui/asns.html', context)

@login_required
def aut_num_detail(request, aut_num_id):
    aut_num_obj    = get_object_or_404(aut_num, pk=aut_num_id)
    return render(request, 'op_webgui/aut_num.html', {'aut_num': aut_num_obj})

@login_required
def aut_num_create(request):
    if request.method == "POST":
        form = ASNForm(request.POST)
        if form.is_valid():
            asn = form.save()
            return redirect('op_webgui:aut_num_detail', aut_num_id=asn.pk)
    else:
        form = ASNForm()
    return render(request, 'op_webgui/generic_edit.html', {'form': form})

@login_required
def aut_num_edit(request, aut_num_id):
    asn = get_object_or_404(aut_num, pk=aut_num_id)
    if request.method == "POST":
        form = ASNForm(request.POST, instance=asn)
        if form.is_valid():
            asn = form.save()
            return redirect('op_webgui:aut_num_detail', aut_num_id=asn.pk)
    else:
        form = ASNForm(instance=asn)
    return render(request, 'op_webgui/generic_edit.html', {'form': form})

@login_required
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

@login_required
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

@login_required
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

@login_required
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

@login_required
def router_detail(request, router_id):
    router_obj     = get_object_or_404(router, pk=router_id)
    return render(request, 'op_webgui/router.html', {'router': router_obj})

@login_required
def router_create(request):
    if request.method == "POST":
        form = RouterForm(request.POST)
        if form.is_valid():
            router_obj = form.save()
            return redirect('op_webgui:router_detail', router_id=router_obj.pk)
    else:
        form = RouterForm()
    return render(request, 'op_webgui/generic_edit.html', {'form': form})

@login_required
def router_edit(request, router_id):
    router_obj = get_object_or_404(router, pk=router_id)
    if request.method == "POST":
        form = RouterForm(request.POST, instance=router_obj)
        if form.is_valid():
            router_obj = form.save()
            return redirect('op_webgui:router_detail', router_id=router_obj.pk)
    else:
        form = RouterForm(instance=router_obj)
    return render(request, 'op_webgui/generic_edit.html', {'form': form})

@login_required
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

    return render(request, 'op_webgui/router_config.html', context)
