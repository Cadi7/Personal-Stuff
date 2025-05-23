from rest_framework import viewsets, permissions
from .models import Folder, File, FileVersion, FileAnnotation, SharedFile
from .serializers import (
    FolderSerializer, FileSerializer, FileVersionSerializer,
    FileAnnotationSerializer, SharedFileSerializer
)

class FolderViewSet(viewsets.ModelViewSet):
    queryset = Folder.objects.all()
    serializer_class = FolderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Folder.objects.filter(owner=self.request.user, is_deleted=False)

class FileViewSet(viewsets.ModelViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return File.objects.filter(owner=self.request.user, is_deleted=False)

class FileVersionViewSet(viewsets.ModelViewSet):
    queryset = FileVersion.objects.all()
    serializer_class = FileVersionSerializer
    permission_classes = [permissions.IsAuthenticated]

class FileAnnotationViewSet(viewsets.ModelViewSet):
    queryset = FileAnnotation.objects.all()
    serializer_class = FileAnnotationSerializer
    permission_classes = [permissions.IsAuthenticated]

class SharedFileViewSet(viewsets.ModelViewSet):
    queryset = SharedFile.objects.all()
    serializer_class = SharedFileSerializer
    permission_classes = [permissions.IsAuthenticated]