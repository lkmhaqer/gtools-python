# file: netdevice/forms.py

from django import forms

from netdevice.models import router, interface, logical_interface, vrf


class RouterForm(forms.ModelForm):

    class Meta:
        model  = router
        fields = ('__all__')


class VrfForm(forms.ModelForm):

    class Meta:
        model = vrf
        fields = ('__all__')


class InterfaceForm(forms.ModelForm):

    class Meta:
        model  = interface
        fields = ('__all__')


class LogicalInterfaceForm(forms.ModelForm):

    class Meta:
        model  = logical_interface
        fields = ('__all__')
