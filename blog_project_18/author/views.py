from django.shortcuts import render, redirect
from . import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from posts.models import Post
# # Create your views here.


# def add_author(request):
#     if request.method == 'POST':
#         author_form = forms.AuthorForm(request.POST)
#         if author_form.is_valid():
#             author_form.save()
#             return redirect('add_author')
#     else:
#         author_form = forms.AuthorForm(request.POST)
#     return render(request, 'add_author.html', {'author_form': author_form})


def register(request):
    if request.method == 'POST':
        register_form = forms.RegistrationsForm(request.POST)
        if register_form.is_valid():
            register_form.save()
            messages.success(request, 'Account created successfully')
            return redirect('register')
    else:
        register_form = forms.RegistrationsForm()
    return render(request, 'register.html', {'form': register_form, 'type': 'REGISTER'})


def user_login(request):
    if request.method == 'POST':
        login_form = AuthenticationForm(request, data=request.POST)
        if login_form.is_valid():
            user_name = login_form.cleaned_data['username']
            user_pass = login_form.cleaned_data['password']
            user = authenticate(username=user_name, password=user_pass)
            if user is not None:
                messages.success(request, 'Login successfully')
                login(request, user)
                return redirect('home')
        else:
            messages.warning(request, 'Username or password incorrect')
            return redirect('login')
    else:
        login_form = AuthenticationForm()
        return render(request, 'register.html', {'form': login_form, 'type': 'LOGIN'})


@login_required
def profile(request):
    data = Post.objects.filter(author=request.user)
    user = request.user
    context = {
        'user_details': [
            {'title': 'Username', 'value': user.username},
            {'title': 'First Name', 'value': user.first_name},
            {'title': 'Last Name', 'value': user.last_name},
            {'title': 'Email', 'value': user.email},
        ],
        'posts': data
    }
    return render(request, 'profile.html', context)


@login_required
def edit_profile(request):
    if request.method == 'POST':
        profile_form = forms.ChangeUserData(
            request.POST, instance=request.user)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('profile')
    else:
        profile_form = forms.ChangeUserData(instance=request.user)
        return render(request, 'profile_change.html', {'form': profile_form})


@login_required
def pass_change(request):
    if request.method == 'POST':
        pass_change = PasswordChangeForm(request.user, data=request.POST)
        if pass_change.is_valid():
            pass_change.save()
            update_session_auth_hash(request, pass_change.user)
            messages.success(request, 'Password changed successfully')
            return redirect('profile')

    else:
        pass_change = PasswordChangeForm(user=request.user)
    return render(request, 'pass_change.html', {'form': pass_change})


@login_required
def user_logout(request):
    logout(request)
    return redirect('home')
