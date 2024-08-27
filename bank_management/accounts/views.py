from django.shortcuts import render, redirect
from django.views.generic import FormView
from .forms import UserRegistrationForm,UserUpdateForm,UserProfileForm, User
from django.contrib.auth import login, logout
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView
from django.views.generic.detail import DetailView
from django.urls import reverse



# Create your views here.


class UserRegistrationView(FormView):
    template_name = 'accounts/user_registrations.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('register')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)


class UserLoginView(LoginView):
    template_name = 'accounts/user_login.html'

    def get_success_url(self):
        return reverse_lazy('home')


# class UserLogOutView(LogoutView):

#     def get_success_url(self):
#         if self.request.user.is_authenticated():
#             logout(self.request)
#             return reverse_lazy('home')


def user_logout(request):

    logout(request)
    return redirect('home')

class UserProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'accounts/user_profile.html'
    context_object_name = 'form' 

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = UserProfileForm(instance=self.request.user)
        context['form'] = form
        return context  

class UserUpdateView(LoginRequiredMixin, UpdateView):
    form_class = UserUpdateForm
    template_name = 'accounts/user_update_profile.html'
    
    def get_success_url(self):
        return reverse('user_profile')

    def get_object(self, queryset=None):
        return self.request.user      