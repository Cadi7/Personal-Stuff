from rest_framework.routers import DefaultRouter
from .api_views import (
    FolderViewSet, FileViewSet, FileVersionViewSet,
    FileAnnotationViewSet, SharedFileViewSet
)

router = DefaultRouter()
router.register(r'folders', FolderViewSet, basename='folder')
router.register(r'files', FileViewSet, basename='file')
router.register(r'versions', FileVersionViewSet, basename='fileversion')
router.register(r'annotations', FileAnnotationViewSet, basename='fileannotation')
router.register(r'shared', SharedFileViewSet, basename='sharedfile')

urlpatterns = router.urls