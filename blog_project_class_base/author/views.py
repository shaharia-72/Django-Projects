from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from . import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from posts.models import Post
from django.contrib.auth.views import LoginView, LogoutView
# from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy


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


# def user_login(request):
#     if request.method == 'POST':
#         login_form = AuthenticationForm(request, data=request.POST)
#         if login_form.is_valid():
#             user_name = login_form.cleaned_data['username']
#             user_pass = login_form.cleaned_data['password']
#             user = authenticate(username=user_name, password=user_pass)
#             if user is not None:
#                 messages.success(request, 'Login successfully')
#                 login(request, user)
#                 return redirect('home')
#         else:
#             messages.warning(request, 'Username or password incorrect')
#             return redirect('login')
#     else:
#         login_form = AuthenticationForm()
#         return render(request, 'register.html', {'form': login_form, 'type': 'LOGIN'})

class UserLoginClassBase(LoginView):
    template_name = 'register.html'
    # success_url = reverse_lazy('profile')

    def get_success_url(self):
        # if not self.success_url:
        #     raise ImproperlyConfigured(
        #         "No URL to redirect to. Provide a success_url.")
        # return str(self.success_url)
        return reverse_lazy('profile')

    def form_valid(self, form):
        messages.success(self.request, 'Logged in successful')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.success(
            self.request, 'Logged in unsuccessful. rechecking username and  password')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'Login'
        return context


@ login_required
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


@ login_required
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


@ login_required
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


# @ login_required
# def user_logout(request):
#     logout(request)
#     return redirect('home')


class UserLogoutClassBase(LogoutView):
    def get_success_url(self):
        return reverse_lazy('home')


class HomeView(TemplateView):
    template_name = 'home.html'
