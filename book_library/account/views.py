from django.shortcuts import redirect
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

#! user registration views
class RegistrationsView(FormView):
    form_class = RegistrationsForm
    template_name = 'registrations.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)


#! user login views
class UserLoginView(LoginView):
    template_name = 'login.html'

    def get_success_url(self):
        return reverse_lazy('home')

#! user logout views

def UserLogOutView(request):
    logout(request)
    return redirect ('home')

#! user profile update views
class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileForm
    template_name = 'profile.html'
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        return self.request.user
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_page'] = 'profile'  #! pass profile for making hover in template

        personal_account = PersonalAccount.objects.get(user=self.request.user)
        context['points'] = personal_account.points
        return context