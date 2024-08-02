from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('about/<int:id>', views.about, name='about'),
]
