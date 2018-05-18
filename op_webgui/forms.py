# file: op_webgui/forms.py

from django import forms

from netdevice.models import router, interface, logical_interface
from static.models import ipv6_static, ipv4_static
from bgp.models import aut_num, neighbor

class RouterForm(forms.ModelForm):

    class Meta:
        model  = router
        fields = ('__all__')

class InterfaceForm(forms.ModelForm):

    class Meta:
        model  = interface
        fields = ('__all__')

class LogicalInterfaceForm(forms.ModelForm):

    class Meta:
        model  = logical_interface
        fields = ('__all__')

class ASNForm(forms.ModelForm):

    class Meta:
        model  = aut_num
        fields = ('__all__')

class NeighborForm(forms.ModelForm):

    class Meta:
        model  = neighbor
        fields = ('__all__')

class IPv6StaticForm(forms.ModelForm):

    class Meta:
        model  = ipv6_static
        fields = ('__all__')

class IPv4StaticForm(forms.ModelForm):

    class Meta:
        model  = ipv4_static
        fields = ('__all__')
