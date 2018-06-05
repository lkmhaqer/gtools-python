# file: address/forms.py

from django import forms

from .models import ipv6_address, ipv4_address


class IPv6AddressForm(forms.ModelForm):

    class Meta:
        model  = ipv6_address
        fields = ('__all__')

class IPv4AddressForm(forms.ModelForm):

    class Meta:
        model  = ipv4_address
        fields = ('__all__')
