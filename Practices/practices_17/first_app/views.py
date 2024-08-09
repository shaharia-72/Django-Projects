from django.shortcuts import render, redirect
from . forms import RegisterForms
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
# Create your views here.


def home(request):
    return render(request, 'home.html')


def signup(request):
    if request.method == 'POST':
        form = RegisterForms(request.POST)
        if form.is_valid():
            messages.success(request, 'Registration Complete')
            form.save()
    else:
        form = RegisterForms()
    return render(request, './singup.html', {'form': form})


def userlogin(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            name = form.cleaned_data['username']
            passw = form.cleaned_data['password']
            user = authenticate(username=name, password=passw)
            if user is not None:
                login(request, user)
                return redirect('profile')
    else:
        form = AuthenticationForm()
        return render(request, './login.html', {'form': form})


def profile(request):
    return render(request, './profile.html', {'user': request.user})


def userlogout(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')
