# file: op_webgui/forms.py

from django import forms

from netdevice.models import router
from static.models import ipv6_static, ipv4_static
from bgp.models import aut_num

class RouterForm(forms.ModelForm):

    class Meta:
        model  = router
        fields = ('__all__')

class ASNForm(forms.ModelForm):

    class Meta:
        model  = aut_num
        fields = ('__all__')

class IPv6StaticForm(forms.ModelForm):

    class Meta:
        model  = ipv6_static
        fields = ('__all__')

class IPv4StaticForm(forms.ModelForm):

    class Meta:
        model  = ipv4_static
        fields = ('__all__')
