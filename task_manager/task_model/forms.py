from django import forms
from . models import TaskModel


class TaskModel(forms.ModelForm):

    class Meta:
        model = TaskModel
        fields = '__all__'
