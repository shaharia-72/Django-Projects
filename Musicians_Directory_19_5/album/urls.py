from django.urls import path
from . import views

urlpatterns = [
    # path('add/', views.add_album, name='add_album'),
    path('add/', views.AddAlbumClassBase.as_view(), name='add_album'),
    # path('delete_album/<int:id>/', views.delete_album, name='delete'),
    path('delete_album/<int:pk>/',
         views.DeleteAlbumClassBase.as_view(), name='delete'),
    # path('edit_album/<int:id>/', views.edit_album, name='edit'),
    path('edit_album/<int:pk>/', views.EditAlbumClassBase.as_view(), name='edit'),
]
