from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('', views.folder_list, name='folder_list'),
    path('folder/<int:folder_id>/', views.folder_detail, name='folder_detail'),
    path('file/<int:file_id>/', views.file_detail, name='file_detail'),
    path('upload/', views.file_upload, name='file_upload'),
    path('folder/<int:folder_id>/rename/', views.folder_rename, name='folder_rename'),
    path('folder/<int:folder_id>/delete/', views.folder_delete, name='folder_delete'),
]

