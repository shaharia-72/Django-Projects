from django.shortcuts import render
from task_category.models import TaskModel
from task_category.models import TaskCategory


def home(request):
    data = TaskModel.objects.all()
    data1 = TaskCategory.objects.all()
    return render(request, 'home.html', {'data': data, 'data1': data1})
