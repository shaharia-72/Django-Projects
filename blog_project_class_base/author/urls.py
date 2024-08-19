from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('register/', views.register, name='register'),
    # path('login/', views.user_login, name='login'),
    path('login/', views.UserLoginClassBase.as_view(), name='login'),
    # path('logout/', views.user_logout, name='logout'),
    path('logout/', views.UserLogoutClassBase.as_view(), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('profile/pass_change/', views.pass_change, name='pass_change'),


]
