# file: bgp/forms.py

from django import forms

from .models import aut_num, neighbor


class ASNForm(forms.ModelForm):

    class Meta:
        model  = aut_num
        fields = ('__all__')

class NeighborForm(forms.ModelForm):

    class Meta:
        model  = neighbor
        fields = ('__all__')
