from django.urls import path
from .apis.search import SearchViewSet
from .apis.blob_storage import UploadFileViewSet
from .apis.post import PostViewSet
from .apis.users import UserViewSet

urlpatterns = [
    path('search/', SearchViewSet.searched , name='searched'),
    path('upload/', UploadFileViewSet.as_view({'post': 'create'}), name='upload'),
    path('upload/<int:pk>/', UploadFileViewSet.as_view({'put': 'update', 'delete': 'destroy'}), name='upload-detail'),
    path('post/', PostViewSet.as_view({'post': 'create', 'get': 'list'}), name='post'),
    path('post/<int:pk>/', PostViewSet.as_view({'get': 'retrieve', }), name='post-detail'),
    path('users/<str:pk>/', UserViewSet.as_view({'get': 'retrieve'}), name='user-detail'),
]