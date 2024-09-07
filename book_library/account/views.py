from django.shortcuts import render,redirect
from django.views.generic import FormView
from .forms import RegistrationsForm
from django.urls import reverse_lazy
from django.contrib.auth import login,logout
from django.contrib.auth.views import LoginView
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from .forms import ProfileForm
from .models import PersonalAccount

# Create your views here.

class RegistrationsView(FormView):
    template_name = 'registrations.html'
    form_class = RegistrationsForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)

class UserLoginView(LoginView):
    template_name = 'login.html'

    def get_success_url(self):
        return reverse_lazy('home')
    
def UserLogOutView(request):
    logout(request)
    return redirect ('home')


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileForm
    template_name = 'profile.html'
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        return self.request.user
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_page'] = 'profile'

        try:
            personal_account = PersonalAccount.objects.get(user=self.request.user)
            context['points'] = personal_account.points
        except PersonalAccount.DoesNotExist:
            context['points'] = 0
        return context