from django.urls import path
from .apis.search import SearchViewSet
from .apis.blob_storage import UploadFileViewSet
from .apis.post import PostViewSet
from .apis.users import UserViewSet
from .apis.like import LikeViewSet
from .apis.calendar import EventViewSet
from .apis.notification import NotificationViewSet
from .apis.organization import OrganizationViewSet

urlpatterns = [
    path('search/', SearchViewSet.searched , name='searched'),
    path('upload/', UploadFileViewSet.as_view({'post': 'create'}), name='upload'),
    path('upload/<int:pk>/', UploadFileViewSet.as_view({'put': 'update', 'delete': 'destroy'}), name='upload-detail'),
    path('post/', PostViewSet.as_view({'post': 'create', 'get': 'list'}), name='post'),
    path('post/<int:pk>/', PostViewSet.as_view({'get': 'retrieve', }), name='post-detail'),
    path('like/<int:pk>/', LikeViewSet.as_view({'post': 'like'}), name='like'),
    path('users/<str:pk>/', UserViewSet.as_view({'get': 'retrieve'}), name='user-detail'),
    path('calendar/get/', EventViewSet.as_view({'get': 'list'}), name='calendar-get'),
    path('calendar/', EventViewSet.as_view({'post': 'create'}), name='calendar'),
    path('calendar/<int:pk>/', EventViewSet.as_view({'put': 'update', 'delete': 'destroy'}), name='calendar-detail'),
    path('calendar/mock/', EventViewSet.as_view({'post': 'generate_mock_events'}), name='calendar-mock'),
    path('notification/', NotificationViewSet.as_view({'get': 'list'}), name='notification'),
    path('notification/<int:pk>/', NotificationViewSet.as_view({'put': 'update'}), name='notification-detail'),
    path('notification/create/', NotificationViewSet.as_view({'post': 'create'}), name='notification-create'),
    path('organization/', OrganizationViewSet.as_view({'get': 'list'}), name='organization'),
    path('organization/<str:org_name>/', OrganizationViewSet.as_view({'get': 'get_by_name'}), name='organization-by-name'),
]