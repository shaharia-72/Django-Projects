from django import forms
from . models import Album


class Album(forms.ModelForm):

    class Meta:
        model = Album
        fields = '__all__'
