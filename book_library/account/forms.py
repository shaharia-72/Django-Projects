from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django import forms
from .models import PersonalAccount

class RegistrationsForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={ 'id': 'required'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'id': 'required'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'id': 'required', 'placeholder':'example@example.com'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name','email']
    
    def save(self, commit = True):
        user = super().save(commit=True)
        if commit == True:
           PersonalAccount.objects.create(user=user)
        return user


class ProfileEditForm(UserChangeForm):
    password = None

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

class ProfileForm(forms.ModelForm):
    

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name','email']



