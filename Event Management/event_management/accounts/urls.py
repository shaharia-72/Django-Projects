# urls.py
from django.urls import path
from .views import RegisterView, ParticipantRegistrationView, OrganizerRegistrationView, CustomLoginView,logout_view

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('register/participant/', ParticipantRegistrationView.as_view(), name='register_participant'),
    path('register/organizer/', OrganizerRegistrationView.as_view(), name='register_organizer'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
]
