from django.urls import path
from .views import UserRegistrationView, UserLoginView,UserUpdateView,UserProfileView
from .import views


urlpatterns = [
    path('user_register/', UserRegistrationView.as_view(), name='user_register'),
    path('user_login/', UserLoginView.as_view(), name='user_login'),
    path('user_logout/', views.user_logout, name='user_logout'),
    path('user_profile/', UserProfileView.as_view(), name='user_profile'),
    path('user_edit_profile/', UserUpdateView.as_view(), name='user_edit_profile'),
]
