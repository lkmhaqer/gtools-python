# file: bgp/views.py

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404, render, redirect

from netdevice.models import router
from bgp.models import aut_num, neighbor
from bgp.forms import ASNForm, NeighborForm


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

    return render(request, 'bgp/asn_list.html', context)

def aut_num_detail(request, aut_num_id):
    aut_num_obj    = get_object_or_404(aut_num, pk=aut_num_id)
    return render(request, 'bgp/aut_num.html', {'aut_num': aut_num_obj})

def aut_num_create(request):
    if request.method == "POST":
        form = ASNForm(request.POST)
        if form.is_valid():
            asn = form.save()
            return redirect('bgp:aut_num_detail', aut_num_id=asn.pk)
    else:
        form = ASNForm()
    return render(request, 'op_webgui/generic_edit.html', {'form': form})

def aut_num_edit(request, aut_num_id):
    asn = get_object_or_404(aut_num, pk=aut_num_id)
    if request.method == "POST":
        form = ASNForm(request.POST, instance=asn)
        if form.is_valid():
            asn = form.save()
            return redirect('bgp:aut_num_detail', aut_num_id=asn.pk)
    else:
        form = ASNForm(instance=asn)
    return render(request, 'op_webgui/generic_edit.html', {'form': form})

def neighbor_create(request, router_id):
    router_obj = get_object_or_404(router, pk=router_id)
    if request.method == "POST":
        form = NeighborForm(request.POST)
        if form.is_valid():
            neighbor_obj = form.save()
            return redirect('netdevice:router_detail', router_id=neighbor_obj.router.pk)
    else:
        form = NeighborForm(initial={'router': router_obj})
    return render(request, 'op_webgui/generic_edit.html', {'form': form})

def neighbor_edit(request, neighbor_id):
    neighbor_obj = get_object_or_404(neighbor, pk=neighbor_id)
    if request.method == "POST":
        form = NeighborForm(request.POST, instance=neighbor_obj)
        if form.is_valid():
            neighbor_obj = form.save()
            return redirect('netdevice:router_detail', router_id=neighbor_obj.router.pk)
    else:
        form = NeighborForm(instance=neighbor_obj)
    return render(request, 'op_webgui/generic_edit.html', {'form': form})
