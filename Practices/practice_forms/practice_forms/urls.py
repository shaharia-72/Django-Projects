from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index),
    path('form_app/', include('form_app.urls')),
    path('form_app/', include('form_app.urls')),
]
