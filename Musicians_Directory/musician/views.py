from django.shortcuts import render, redirect
from . import forms
from .models import Musician


def add_musician(request):
    if request.method == 'POST':
        musician_form = forms.Musician(request.POST)
        if musician_form.is_valid():
            first_name = musician_form.cleaned_data['first_name']
            last_name = musician_form.cleaned_data['last_name']
            if Musician.objects.filter(first_name=first_name, last_name=last_name).exists():
                error_message = "Musician is already registered."
                return render(request, 'home_musician.html', {'musician_form': musician_form, 'error_message': error_message})
            else:
                musician_form.save()
                return redirect('home')
    else:
        musician_form = forms.Musician()
    return render(request, 'home_musician.html', {'musician_form': musician_form})


def edit_musician(request, id):
    musician_form = Musician.objects.get(pk=id)
    if request.method == 'POST':
        musician_forms = forms.Musician(instance=musician_form)
        if musician_forms.is_valid():
            musician_forms.save()
            return redirect('home')
    else:
        musician_forms = forms.Musician(instance=musician_form)

    return render(request, 'home_musician.html', {'musician_form': musician_forms})
