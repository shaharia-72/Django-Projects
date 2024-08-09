from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.userlogin, name='login'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.userlogout, name='userlogout'),

]
