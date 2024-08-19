from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('account_create/', views.account_create, name='account_create'),
    path('login/', views.UserLogin.as_view(), name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('profile_edit/', views.profile_edit, name='profile_edit'),
    path('profile/password_change/', views.password_change, name='password_change'),


]
