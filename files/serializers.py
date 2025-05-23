from rest_framework import serializers
from .models import Folder, File, FileVersion, FileAnnotation, SharedFile

class FolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Folder
        fields = '__all__'

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = '__all__'

class FileVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileVersion
        fields = '__all__'

class FileAnnotationSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileAnnotation
        fields = '__all__'

class SharedFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = SharedFile
        fields = '__all__'