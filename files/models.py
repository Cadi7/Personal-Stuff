from django.db import models
from django.contrib.auth.models import User

class Folder(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='subfolders', on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

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

