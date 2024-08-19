from django.shortcuts import render, redirect
from album.models import Album
from . forms import RegisterForms
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout

# class base
from django.contrib.auth.views import LoginView
from django.views.generic import TemplateView, CreateView
from django.urls import reverse_lazy
from django.views.generic.list import ListView


# def home(request):
#     data = Album.objects.all()
#     return render(request, 'home.html', {'data': data})

class HomeClassBase(ListView):
    model = Album
    template_name = 'home.html'
    context_object_name = 'data'


# def signup(request):
#     if request.method == 'POST':
#         form = RegisterForms(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Registration is completed successfully')
#             return redirect('login')
#     else:
#         form = RegisterForms()
#     return render(request, 'user_signup.html', {'form': form})

class UserRegistrationClassBase(CreateView):
    form_class = RegisterForms
    template_name = 'user_signup.html'
    # success_url = reverse_lazy('user_login.html')

    def get_success_url(self):
        return reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()

        if user:
            login(self.request, user)
        return super().form_valid(form)


# def user_login(request):
#     if request.method == 'POST':
#         form = AuthenticationForm(request=request, data=request.POST)
#         if form.is_valid():
#             n_ame = form.cleaned_data['username']
#             pass_word = form.cleaned_data['password']
#             user = authenticate(username=n_ame, password=pass_word)
#             if user is not None:
#                 login(request, user)
#                 return redirect('home')
#     else:
#         form = AuthenticationForm()
#     return render(request, 'user_login.html', {'form': form})

class UserLoginClassBase(LoginView):
    template_name = 'user_login.html'

    def get_success_url(self):
        return reverse_lazy('home')

    def form_valid(self, form):
        messages.success(self.request, 'User login successful')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.success(self.request, 'User login invalid')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'Login'
        return context


def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully')
    return redirect('home')
