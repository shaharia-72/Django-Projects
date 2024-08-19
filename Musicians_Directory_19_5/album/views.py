from django.shortcuts import render, redirect
from .forms import AlbumForm
from .models import Album

# class view
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView, UpdateView, DeleteView


# def add_album(request):
#     if request.method == 'POST':
#         album_form = forms.Album(request.POST)
#         if album_form.is_valid():
#             album_names = album_form.cleaned_data['album_name']
#             if Album.objects.filter(album_name=album_names).exists():
#                 error_message = "An album with this name already exists."
#                 return render(request, 'home_album.html', {'album_form': album_form, 'error_message': error_message})
#             else:
#                 album_form.save()
#                 return redirect('home')
#     else:
#         album_form = forms.Album()
#     return render(request, 'home_album.html', {'album_form': album_form})

class AddAlbumClassBase(LoginRequiredMixin, FormView):
    form_class = AlbumForm
    template_name = 'home_album.html'

    def get_success_url(self):
        return reverse_lazy('home')

    def form_valid(self, form):
        album_names = form.cleaned_data['album_name']
        if Album.objects.filter(album_name=album_names).exists():
            form.add_error('album_name', "The album name already exists")
            return self.form_invalid(form)
        form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


# def edit_album(request, id):
#     album_form = Album.objects.get(pk=id)
#     if request.method == 'POST':
#         album_forms = Album(request.POST, instance=album_form)
#         if album_forms.is_valid():
#             album_forms.save()
#             return redirect('home')
#     else:
#         album_forms = Album(instance=album_form)

#     return render(request, 'home_album.html', {'album_form': album_forms})

class EditAlbumClassBase(LoginRequiredMixin, UpdateView):
    model = Album
    form_class = AlbumForm
    template_name = 'home_album.html'
    context_object_name = 'album_form'

    def get_success_url(self):
        return reverse_lazy('home')


# def delete_album(request, id):
#     album_form = Album.objects.get(pk=id)
#     album_form.delete()
#     return redirect('home')

class DeleteAlbumClassBase(LoginRequiredMixin, DeleteView):
    model = Album
    template_name = 'confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('home')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
