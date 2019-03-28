# file: vrf/serializers.py

from rest_framework import serializers
from vrf.models import vrf


class VrfSerializer(serializers.ModelSerializer):
    class Meta:
        model  = vrf
        fields = ('__all__')
