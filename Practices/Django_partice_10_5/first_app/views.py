from django.shortcuts import render
import datetime

# Create your views here.


def home(request):

    d = {
        'add_value': 4,
        'addslashes_value': "Hell'o 'world'",
        'capfirst_value': "hello",
        'center_value': "hello",
        'cut_value': "hello",
        'date_value': datetime.datetime.now(),
        'default_value': "",
        'dictsort_value': [{'name': 'Shaharia'}, {'name': 'Hossain'}, {'name': 'Sadiatur'}],
        'divisibleby_value': 9,
        'filesizeformat_value': 1048576,
        'first_value': [1, 2, 3],
        'join_value': ["a", "b", "c"],
        'last_value': [1, 2, 3],
        'length_value': [1, 2, 3],
    }

    return render(request, 'home.html', d)


def about(request):
    return render(request, 'navigation/about.html')


def privacy(request):
    return render(request, 'navigation/privacy.html')
