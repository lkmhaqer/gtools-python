# file: address/serializers.py

from rest_framework import serializers
from address.models import ipv6_address, ipv4_address


class Ipv6AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ipv6_address
        fields = ('__all__')

class Ipv6AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ipv6_address
        fields = ('__all__')
