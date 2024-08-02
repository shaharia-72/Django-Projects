from django.shortcuts import render

# Create your views here.


def home(request):
    d = {'author': "Rahim", 'age': 13}  # context
    return render(request, 'home.html', d)
