# file: op_webgui/views.py

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404, render, redirect

from netdevice.models import router, interface, logical_interface
from address.models import ipv6_address, ipv4_address
from static.models import ipv6_static, ipv4_static
from bgp.models import aut_num, neighbor

from .forms import RouterForm, ASNForm, NeighborForm
from .forms import IPv6StaticForm, IPv4StaticForm
from .forms import InterfaceForm, LogicalInterfaceForm
from .forms import IPv6AddressForm, IPv4AddressForm

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

def asn_list(request):
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

    return render(request, 'op_webgui/asn_list.html', context)

def aut_num_detail(request, aut_num_id):
    aut_num_obj    = get_object_or_404(aut_num, pk=aut_num_id)
    return render(request, 'op_webgui/aut_num.html', {'aut_num': aut_num_obj})

def aut_num_create(request):
    if request.method == "POST":
        form = ASNForm(request.POST)
        if form.is_valid():
            asn = form.save()
            return redirect('op_webgui:aut_num_detail', aut_num_id=asn.pk)
    else:
        form = ASNForm()
    return render(request, 'op_webgui/generic_edit.html', {'form': form})

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

def neighbor_create(request, router_id):
    router_obj = get_object_or_404(router, pk=router_id)
    if request.method == "POST":
        form = NeighborForm(request.POST)
        if form.is_valid():
            neighbor_obj = form.save()
            return redirect('op_webgui:router_detail', router_id=neighbor_obj.router.pk)
    else:
        form = NeighborForm(initial={'router': router_obj})
    return render(request, 'op_webgui/generic_edit.html', {'form': form})

def neighbor_edit(request, neighbor_id):
    neighbor_obj = get_object_or_404(neighbor, pk=neighbor_id)
    if request.method == "POST":
        form = NeighborForm(request.POST, instance=neighbor_obj)
        if form.is_valid():
            neighbor_obj = form.save()
            return redirect('op_webgui:router_detail', router_id=neighbor_obj.router.pk)
    else:
        form = NeighborForm(instance=neighbor_obj)
    return render(request, 'op_webgui/generic_edit.html', {'form': form})

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

def router_detail(request, router_id):
    router_obj     = get_object_or_404(router, pk=router_id)
    return render(request, 'op_webgui/router.html', {'router': router_obj})

def router_create(request):
    if request.method == "POST":
        form = RouterForm(request.POST)
        if form.is_valid():
            router_obj = form.save()
            return redirect('op_webgui:router_detail', router_id=router_obj.pk)
    else:
        form = RouterForm()
    return render(request, 'op_webgui/generic_edit.html', {'form': form})

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
