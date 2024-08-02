from django.shortcuts import render, redirect
from posts.models import Post
# Create your views here.


def home(request):
    data = Post.objects.all()
    return render(request, 'home.html', {'data': data})
