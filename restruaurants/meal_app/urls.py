from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.meal_app, name='meal'),
]
