from django.shortcuts import render, redirect
from . import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth import logout
from django.views.generic import ListView
from cars.models import Order, Car

# Create your views here.


def account_create(request):
    if request.method == 'POST':
        account_create = forms.RegistrationsForm(request.POST)
        if account_create.is_valid():
            account_create.save()
            messages.success(request, 'Account created successfully')
            return redirect('home')
    else:
        account_create = forms.RegistrationsForm()
    return render(request, 'account_create.html', {'form': account_create, 'type': 'Register'})


class UserLogin(LoginView):
    template_name = 'account_create.html'

    def get_success_url(self):

        return reverse_lazy('home')

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
def password_change(request):
    if request.method == 'POST':
        password_change = PasswordChangeForm(request.user, data=request.POST)
        if password_change.is_valid():
            password_change.save()
            update_session_auth_hash(request, password_change.user)
            messages.success(request, 'Password changed successfully')
            return redirect('profile')

    else:
        password_change = PasswordChangeForm(user=request.user)
    return render(request, 'password_change.html', {'form': password_change})


@ login_required
def user_logout(request):
    logout(request)
    return redirect('home')


@ login_required
def profile_edit(request):
    if request.method == 'POST':
        profile_form = forms.ProfileEditForm(
            request.POST, instance=request.user)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('profile')
    else:
        profile_form = forms.ProfileEditForm(instance=request.user)
        return render(request, 'profile_edit.html', {'form': profile_form})


@ login_required
def profile(request):
    user = request.user
    orders = Order.objects.filter(user=user)
    context = {
        'user_details': [
            {'title': 'Username', 'value': user.username},
            {'title': 'First Name', 'value': user.first_name},
            {'title': 'Last Name', 'value': user.last_name},
            {'title': 'Email', 'value': user.email},
        ],
        'orders': orders
    }
    return render(request, 'profile.html', context)


class OrderHistoryView(ListView):
    model = Order
    template_name = 'profile.html'
    context_object_name = 'orders'
    orders = Order.objects.all()

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
