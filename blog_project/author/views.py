from django.shortcuts import render, redirect
from . import forms
# Create your views here.


def add_author(request):
    if request.method == 'POST':
        author_form = forms.AuthorForm(request.POST)
        if author_form.is_valid():
            author_form.save()
            return redirect('add_author')
    else:
        author_form = forms.AuthorForm(request.POST)
    return render(request, 'add_author.html', {'author_form': author_form})
