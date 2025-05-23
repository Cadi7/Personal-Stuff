from django.contrib import admin
from .models import Folder, File, FileVersion, FileAnnotation, SharedFile, FileLog

@admin.register(Folder)
class FolderAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'owner', 'created_at', 'is_deleted', 'deleted_at')
    list_filter = ('owner', 'is_deleted')
    search_fields = ('name',)

@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ('name', 'folder', 'owner', 'uploaded_at', 'is_deleted', 'deleted_at')
    list_filter = ('owner', 'folder', 'is_deleted')
    search_fields = ('name', 'description', 'tags')

@admin.register(FileVersion)
class FileVersionAdmin(admin.ModelAdmin):
    list_display = ('file', 'version_number', 'created_at', 'comment')
    list_filter = ('file',)
    search_fields = ('file__name', 'comment')

@admin.register(FileAnnotation)
class FileAnnotationAdmin(admin.ModelAdmin):
    list_display = ('version', 'user', 'created_at')
    list_filter = ('user', 'version')
    search_fields = ('version__file__name', 'text')

@admin.register(SharedFile)
class SharedFileAdmin(admin.ModelAdmin):
    list_display = ('file', 'shared_with', 'permission', 'shared_at')
    list_filter = ('permission', 'shared_with')
    search_fields = ('file__name', 'shared_with__username')

@admin.register(FileLog)
class FileLogAdmin(admin.ModelAdmin):
    list_display = ('file', 'user', 'action', 'timestamp', 'notes')
    list_filter = ('action', 'user')
    search_fields = ('file__name', 'notes')