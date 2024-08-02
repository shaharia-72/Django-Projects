from django.shortcuts import render
import datetime

# Create your views here.


def home(request):
    d = {'author': 'Rahim', 'age': 5, 'list': ['python', 'java', 'c++'], 'courses': [
        {
            'id': 1,
            'name': 'python',
            'fee': 5000
        },
        {
            'id': 2,
            'name': 'c++',
            'fee': 7000
        },
        {
            'id': 3,
            'name': 'javascript',
            'fee': 8000
        },
    ], 'birthday': datetime.datetime.now(), }
    return render(request, 'home.html', d)
