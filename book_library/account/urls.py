from django.urls import path
from .views import RegistrationsView, UserLoginView, ProfileUpdateView
from .import views

urlpatterns = [
        path('user_register/', RegistrationsView.as_view(), name='user_register'),
        path('user_login/', UserLoginView.as_view(), name='user_login'),
        path('user_logout/', views.UserLogOutView, name='user_logout'),
        path('user_profile/', ProfileUpdateView.as_view(), name='user_profile'),
]
