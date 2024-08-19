from django.urls import path
from . import views

urlpatterns = [
    path('car/<int:pk>/', views.CarDetailView.as_view(), name='car_detail'),
    path('car/confirm_order/<int:pk>/',
         views.ConfirmOrderView.as_view(), name='confirm_order'),
]
