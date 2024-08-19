from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from . import forms
from . import models
# from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin


# @login_required
# def add_post(request):
#     if request.method == 'POST':
#         post_form = forms.PostForm(request.POST)
#         if post_form.is_valid():
#             post_form.instance.author = request.user
#             post_form.save()
#             return redirect('add_post')
#     else:
#         post_form = forms.PostForm(request.POST)
#     return render(request, 'add_post.html', {'post_form': post_form})
class AddPostClassBase(LoginRequiredMixin, CreateView):
    model = models.Post
    form_class = forms.PostForm
    template_name = "add_post.html"
    success_url = reverse_lazy('add_post')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


# def edit_post(request, id):
#     post = models.Post.objects.get(pk=id)
#     post_form = forms.PostForm(instance=post)
#     if request.method == 'POST':
#         post_form = forms.PostForm(request.POST, instance=post)
#         if post_form.is_valid():
#             post_form.save()
#             return redirect('home')
#     return render(request, 'add_post.html', {'form': post_form})


class EditPostClassBase(LoginRequiredMixin, UpdateView):
    model = models.Post
    form_class = forms.PostForm
    template_name = 'add_post.html'
    success_url = reverse_lazy('profile')
    pk_url_kwarg = 'id'


# def delete_post(request, id):
#     post = models.Post.objects.get(pk=id)
#     post.delete()
#     return redirect('home')

class DeletePostClassBase(LoginRequiredMixin, DeleteView):
    model = models.Post
    template_name = 'delete_post.html'
    pk_url_kwarg = 'id'
    success_url = reverse_lazy('profile')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = self.get_object()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        return redirect(success_url)
