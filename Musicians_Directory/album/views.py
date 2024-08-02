from django.shortcuts import render, redirect
from . import forms
from .models import Album


def add_album(request):
    if request.method == 'POST':
        album_form = forms.Album(request.POST)
        if album_form.is_valid():
            album_names = album_form.cleaned_data['album_name']
            if Album.objects.filter(album_name=album_names).exists():
                error_message = "An album with this name already exists."
                return render(request, 'home_album.html', {'album_form': album_form, 'error_message': error_message})
            else:
                album_form.save()
                return redirect('home')
    else:
        album_form = forms.Album()
    return render(request, 'home_album.html', {'album_form': album_form})


def edit_album(request, id):
    album_form = Album.objects.get(pk=id)
    if request.method == 'POST':
        album_forms = forms.Album(request.POST, instance=album_form)
        if album_forms.is_valid():
            album_forms.save()
            return redirect('home')
    else:
        album_forms = forms.Album(instance=album_form)

    return render(request, 'home_album.html', {'album_form': album_forms})


def delete_album(request, id):
    album_form = Album.objects.get(pk=id)
    album_form.delete()
    return redirect('home')
