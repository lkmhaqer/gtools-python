# -*- coding: utf-8 -*-
# file: api/views.py

from __future__ import unicode_literals

from rest_framework import generics

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
