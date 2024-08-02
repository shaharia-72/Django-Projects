from django.shortcuts import render
from form_app.forms import contact_form


def app(request):
    return render(request, 'app.html')


def submit_form(request):
    print(request.POST)
    return render(request, 'form.html')


def django_form(request):
    if request.method == 'POST':
        form = contact_form(request.POST, request.FILES)
        if form.is_valid():
            file = form.cleaned_data['file']
            with open('./form_app/upload/' + file.name, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
            print(form.cleaned_data)
            return render(request, 'django_form.html', {'form': form})
    else:
        form = contact_form()
    return render(request, 'django_form.html', {'form': form})


def crispy_form(request):
    if request.method == 'POST':
        form = contact_form(request.POST, request.FILES)
        if form.is_valid():
            file = form.cleaned_data['file']
            print(form.cleaned_data)
            return render(request, 'crispy_form.html', {'form': form})
    else:
        form = contact_form()
    return render(request, 'crispy_form.html', {'form': form})
