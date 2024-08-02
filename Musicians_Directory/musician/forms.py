from django import forms
from . models import Musician


class Musician(forms.ModelForm):

    class Meta:
        model = Musician
        fields = '__all__'
