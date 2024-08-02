from django.urls import path

from . import views

urlpatterns = [
    path('', views.app, name='app'),
    path('form/', views.submit_form, name='submit_form'),
    path('django_app/', views.django_form, name='django_form'),
    path('crispy_form', views.crispy_form, name='crispy_form'),
]
