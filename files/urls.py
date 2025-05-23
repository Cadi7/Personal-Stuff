from django.urls import path, include
from . import views

app_name = 'files'

urlpatterns = [
    path('', views.folder_list, name='folder_list'),
    path('folder/<int:pk>/', views.folder_detail, name='folder_detail'),
    path('folder/add/', views.folder_create, name='folder_create'),
    path('folder/<int:parent_pk>/add/', views.folder_create, name='folder_create_sub'),
    path('folder/<int:pk>/delete/', views.folder_delete, name='folder_delete'),
    path('folder/<int:folder_pk>/upload/', views.file_upload, name='file_upload'),
    path('file/<int:pk>/', views.file_detail, name='file_detail'),
    path('file/<int:pk>/delete/', views.file_delete, name='file_delete'),
    path('file/<int:pk>/restore/', views.file_restore, name='file_restore'),
    path('file/<int:pk>/share/', views.share_file, name='share_file'),
    path('version/<int:version_pk>/annotate/', views.add_annotation, name='add_annotation'),
    path('api/files/', include('files.api_urls')),
    # Add more URLs as needed for versions, trash, etc.
]