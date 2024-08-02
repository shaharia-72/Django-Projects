from django.shortcuts import render


def about_us_app(request):
    return render(request, 'about.html')
