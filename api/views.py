# -*- coding: utf-8 -*-
# file: api/views.py

from __future__ import unicode_literals

from rest_framework import generics

from address.models import ipv6_address, ipv4_address
from address.serializers import Ipv6AddressSerializer, Ipv4AddressSerializer

from bgp.models import aut_num, neighbor
from bgp.serializers import AutNumSerializer, NeighborSerializer

from netdevice.models import router, network_os, interface, logical_interface
from netdevice.serializers import RouterSerializer, NetworkOsSerializer, InterfaceSerializer, LogicalInterfaceSerializer


class RouterList(generics.ListCreateAPIView):
    queryset = router.objects.all()
    serializer_class = RouterSerializer

class RouterDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = router.objects.all()
    serializer_class = RouterSerializer

class NetworkOsList(generics.ListCreateAPIView):
    queryset = network_os.objects.all()
    serializer_class = NetworkOsSerializer

class NetworkOsDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = network_os.objects.all()
    serializer_class = NetworkOsSerializer

class InterfaceList(generics.ListCreateAPIView):
    queryset = interface.objects.all()
    serializer_class = InterfaceSerializer

class InterfaceDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = interface.objects.all()
    serializer_class = InterfaceSerializer

class LogicalInterfaceList(generics.ListCreateAPIView):
    queryset = logical_interface.objects.all()
    serializer_class = LogicalInterfaceSerializer

class LogicalInterfaceDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = logical_interface.objects.all()
    serializer_class = LogicalInterfaceSerializer

class Ipv6AddressList(generics.ListCreateAPIView):
    queryset = ipv6_address.objects.all()
    serializer_class = Ipv6AddressSerializer

class Ipv6AddressDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ipv6_address.objects.all()
    serializer_class = Ipv6AddressSerializer

class Ipv4AddressList(generics.ListCreateAPIView):
    queryset = ipv4_address.objects.all()
    serializer_class = Ipv4AddressSerializer

class Ipv4AddressDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ipv4_address.objects.all()
    serializer_class = Ipv4AddressSerializer

class AutNumList(generics.ListCreateAPIView):
    queryset = aut_num.objects.all()
    serializer_class = AutNumSerializer

class AutNumDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = aut_num.objects.all()
    serializer_class = AutNumSerializer

class NeighborList(generics.ListCreateAPIView):
    queryset = neighbor.objects.all()
    serializer_class = NeighborSerializer

class NeighborDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = neighbor.objects.all()
    serializer_class = NeighborSerializer
