from django import forms
from .models import Folder, File, FileVersion, FileAnnotation, SharedFile

class FolderForm(forms.ModelForm):
    class Meta:
        model = Folder
        fields = ['name']

class FileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['name', 'file', 'description', 'tags']

class FileVersionForm(forms.ModelForm):
    class Meta:
        model = FileVersion
        fields = ['file_data', 'comment']

class AnnotationForm(forms.ModelForm):
    class Meta:
        model = FileAnnotation
        fields = ['text']

class ShareForm(forms.ModelForm):
    class Meta:
        model = SharedFile
        fields = ['shared_with', 'permission']