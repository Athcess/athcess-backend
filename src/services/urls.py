from django.urls import path
from .apis.search import SearchViewSet
from .apis.blob_storage import UploadFileViewSet
from .apis.post import PostViewSet

urlpatterns = [
    path('search/', SearchViewSet.searched , name='searched'),
    path('upload/', UploadFileViewSet.as_view({'post': 'create'}), name='upload'),
    path('post/', PostViewSet.as_view({'post': 'create', 'get': 'list'}), name='post'),
    path('post/<int:pk>/', PostViewSet.as_view({'get': 'retrieve', }), name='post-detail'),
]