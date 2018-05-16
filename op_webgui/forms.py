# file: op_webgui/forms.py

from django import forms

from netdevice.models import router
from bgp.models import aut_num

class RouterForm(forms.ModelForm):

    class Meta:
        model  = router
        fields = (
                  'routing_id',
                  'hostname',
                  'network_os',
                  'local_aut_num',
                  'ibgp',
                  'service_ssh',
                  'service_netconf',
                 )

class ASNForm(forms.ModelForm):

    class Meta:
        model  = aut_num
        fields = (
                  'asn',
                  'name',
                  'contact',
                 )
