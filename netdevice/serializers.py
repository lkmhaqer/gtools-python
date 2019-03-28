# file: netdevice/serializers.py

from rest_framework import serializers
from .models import logical_interface, interface, router, network_os, vrf


class LogicalInterfaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = logical_interface
        fields = ('__all__')


class InterfaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = interface
        fields = ('__all__')


class RouterSerializer(serializers.ModelSerializer):
    class Meta:
        model = router
        fields = ('__all__')


class VrfSerializer(serializers.ModelSerializer):
    class Meta:
        model  = vrf
        fields = ('__all__')


class NetworkOsSerializer(serializers.ModelSerializer):
    class Meta:
        model = network_os
        fields = ('__all__')
