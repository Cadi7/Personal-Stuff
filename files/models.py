from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Folder(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='subfolders', on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.files = None
        self.subfolders = None

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()

    def __str__(self):
        return self.name

class File(models.Model):
    folder = models.ForeignKey(Folder, related_name='files', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='uploads/')
    description = models.TextField(blank=True)
    tags = models.CharField(max_length=255, blank=True, help_text='Comma-separated tags')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()

    def __str__(self):
        return self.name

class FileVersion(models.Model):
    file = models.ForeignKey(File, related_name='versions', on_delete=models.CASCADE)
    version_number = models.PositiveIntegerField()
    file_data = models.FileField(upload_to='versions/')
    created_at = models.DateTimeField(auto_now_add=True)
    comment = models.CharField(max_length=255, blank=True)

    class Meta:
        unique_together = ('file', 'version_number')
        ordering = ['-version_number']

    def __str__(self):
        return f"{self.file.name} v{self.version_number}"

class FileAnnotation(models.Model):
    version = models.ForeignKey(FileVersion, related_name='annotations', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Note by {self.user.username} on v{self.version.version_number}"

class SharedFile(models.Model):
    PERMISSION_CHOICES = [
        ('read', 'Read'),
        ('write', 'Write'),
        ('owner', 'Owner'),
    ]
    file = models.ForeignKey(File, related_name='shared_with', on_delete=models.CASCADE)
    shared_with = models.ForeignKey(User, related_name='shared_files', on_delete=models.CASCADE)
    permission = models.CharField(max_length=10, choices=PERMISSION_CHOICES, default='read')
    shared_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('file', 'shared_with')

    def __str__(self):
        return f"{self.file.name} shared with {self.shared_with.username} ({self.permission})"

class FileLog(models.Model):
    ACTION_CHOICES = [
        ('upload', 'Upload'),
        ('edit', 'Edit'),
        ('delete', 'Delete'),
        ('restore', 'Restore'),
        ('share', 'Share'),
        ('download', 'Download'),
        ('comment', 'Comment'),
        ('version', 'Version'),
    ]
    file = models.ForeignKey(File, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)
    notes = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.file.name}: {self.action} by {self.user}"