from django.shortcuts import render, redirect
from . import forms
from .models import Musician
from .forms import MusicianForms

#  class base
from django.urls import reverse_lazy
from django.views.generic.edit import FormView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404

# def add_musician(request):
#     if request.method == 'POST':
#         musician_form = forms.Musician(request.POST)
#         if musician_form.is_valid():
#             first_name = musician_form.cleaned_data['first_name']
#             last_name = musician_form.cleaned_data['last_name']
#             if Musician.objects.filter(first_name=first_name, last_name=last_name).exists():
#                 error_message = "Musician is already registered."
#                 return render(request, 'home_musician.html', {'musician_form': musician_form, 'error_message': error_message})
#             else:
#                 musician_form.save()
#                 return redirect('home')
#     else:
#         musician_form = forms.Musician()
#     return render(request, 'home_musician.html', {'musician_form': musician_form})


class AddMusicianClassBase(LoginRequiredMixin, FormView):
    form_class = MusicianForms
    template_name = 'home_musician.html'

    def get_success_url(self):
        return reverse_lazy('home')

    def form_valid(self, form):
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        if Musician.objects.filter(first_name=first_name, last_name=last_name).exists():
            form.add_error(None, 'Musician already exists')
            return super().form_valid(form)
        else:
            form.save()
            return super().form_valid(form)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


# def edit_musician(request, id):
#     musician_form = Musician.objects.get(pk=id)
#     if request.method == 'POST':
#         musician_forms = forms.Musician(instance=musician_form)
#         if musician_forms.is_valid():
#             musician_forms.save()
#             return redirect('home')
#     else:
#         musician_forms = forms.Musician(instance=musician_form)

#     return render(request, 'home_musician.html', {'musician_form': musician_forms})

class EditMusicianClassBase(UpdateView):
    model = Musician
    form_class = MusicianForms
    template_name = 'home_musician.html'

    def get_success_url(self):

        return reverse_lazy('home')

    def get_object(self, queryset=None):
        obj = self.get_queryset().filter(pk=self.kwargs['id']).first()
        if obj is None:
            raise Http404("Musician not found")
        return obj
