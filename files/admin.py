from django.contrib import admin
from .models import Folder, File, FileVersion

admin.site.register(Folder)
admin.site.register(File)
admin.site.register(FileVersion)

# Register your models here.
