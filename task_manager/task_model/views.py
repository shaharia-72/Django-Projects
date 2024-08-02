from django.shortcuts import render, redirect
from . import forms
from .models import TaskModel
# Create your views here.


# def task_model(request):
#     model_form = forms.TaskModel()
#     return render(request, 'home_model.html', {'model_form': model_form})


def add_task(request):
    if request.method == 'POST':
        model_form = forms.TaskModel(request.POST)
        if model_form.is_valid():
            tasks_name = model_form.cleaned_data['task_title']
            if TaskModel.objects.filter(task_title=tasks_name).exists():
                error_message = "Task title already exists"
                return render(request, 'home_model.html', {'model_form': model_form, 'error_message': error_message})
            else:
                model_form.save()
                return redirect('home')
    else:
        model_form = forms.TaskModel()
        return render(request, 'home_model.html', {'model_form': model_form})


def edit_task(request, id):
    model_form = TaskModel.objects.get(pk=id)
    if request.method == 'POST':
        model_forms = forms.TaskModel(request.POST, instance=model_form)
        if model_forms.is_valid():
            model_forms.save()
            return redirect('home')
    else:
        model_forms = forms.TaskModel(instance=model_form)
    return render(request, 'home_model.html', {'model_form': model_forms})


def delete_task(request, id):
    model_form = TaskModel.objects.get(pk=id)
    model_form.delete()
    return redirect('home')
