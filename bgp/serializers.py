# file: bgp/serializers.py

from rest_framework import serializers
from bgp.models import aut_num, neighbor


class AutNumSerializer(serializers.ModelSerializer):
    class Meta:
        model = aut_num
        fields = ('__all__')

class NeighborSerializer(serializers.ModelSerializer):
    class Meta:
        model = neighbor
        fields = ('__all__')
