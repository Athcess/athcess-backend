from django.urls import path
from .apis.search import SearchViewSet
from .apis.blob_storage import UploadFileViewSet

urlpatterns = [
    path('search/', SearchViewSet.searched , name='searched'),
    path('upload/', UploadFileViewSet.as_view({'post': 'create'}), name='upload'),
]