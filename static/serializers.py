# file: netdevice/serializers.py

from rest_framework import serializers
from static.models import ipv6_static, ipv4_static


class Ipv6StaticSerializer(serializers.ModelSerializer):
    class Meta:
        model = ipv6_static
        fields = ('__all__')

class Ipv4StaticSerializer(serializers.ModelSerializer):
    class Meta:
        model = ipv4_static
        fields = ('__all__')
