from django.db import models
from task_model.models import TaskModel


class TaskCategory(models.Model):
    category_name = models.CharField(max_length=255)
    tasks = models.ManyToManyField(TaskModel, related_name='categories')

    def __str__(self):
        return self.category_name
