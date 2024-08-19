from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms


class RegisterForms(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput())

    class Meta:

        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
