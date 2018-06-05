# file: static/forms.py

from django import forms

from .models import ipv6_static, ipv4_static


class IPv6StaticForm(forms.ModelForm):

    class Meta:
        model  = ipv6_static
        fields = ('__all__')

class IPv4StaticForm(forms.ModelForm):

    class Meta:
        model  = ipv4_static
        fields = ('__all__')
