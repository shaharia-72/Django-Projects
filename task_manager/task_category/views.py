from django.shortcuts import render, redirect
from . import forms
from . models import TaskCategory
# Create your views here.


def task_category(request):
    category_form = forms.TaskCategory()
    return render(request, 'home_category.html', {'category_form': category_form})


def add_category(request):
    if request.method == 'POST':
        add_category = forms.TaskCategory(request.POST)
        if add_category.is_valid():
            categories_name = add_category.cleaned_data['category_name']
            if TaskCategory.objects.filter(category_name=categories_name).exists():
                error_message = 'Task category already exists'
                return render(request, 'home_category.html', {'add_category': add_category, 'error_message': error_message})
            else:
                add_category.save()
                return redirect('home')

    else:
        add_category = forms.TaskCategory()
        return render(request, 'home_category.html', {'add_category': add_category})
