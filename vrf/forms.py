# file: vrf/forms.py

from django import forms

from vrf.models import vrf


class VRFForm(forms.ModelForm):

    class Meta:
        model = vrf
        fields = ('__all__')
