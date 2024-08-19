from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # path('add/', views.add_post, name='add_post'),
    path('add/', views.AddPostClassBase.as_view(), name='add_post'),
    # path('edit/<int:id>', views.edit_post, name='edit_post'),
    path('edit/<int:id>/', views.EditPostClassBase.as_view(), name='edit_post'),
    # path('delete/<int:id>', views.delete_post, name='delete_post'),
    path('delete/<int:id>/', views.DeletePostClassBase.as_view(), name='delete_post'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
