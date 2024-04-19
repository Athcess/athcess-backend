from django.urls import path
from .apis.search import SearchViewSet
from .apis.blob_storage import UploadFileViewSet
from .apis.post import PostViewSet
from .apis.users import UserViewSet
from .apis.like import LikeViewSet
from .apis.calendar import EventViewSet
from .apis.notification import NotificationViewSet
from .apis.organization import OrganizationViewSet
from .apis.achievement import AchievementViewSets
from .apis.experience import ExperienceViewSet
from .apis.comment import CommentViewSet
from .apis.like_comment import LikeCommentViewSet
from .apis.repost import RepostViewSet
from .apis.follow import FollowViewSet
from .apis.analytic import AnalyticsViewSet

urlpatterns = [
    path('search/', SearchViewSet.as_view({'get': 'search'}), name= 'description-search')
    path('upload/', UploadFileViewSet.as_view({'post': 'create', 'get': 'list'}), name='upload'),
    path('upload/<int:pk>/', UploadFileViewSet.as_view({'put': 'update', 'get': 'retrieve', 'delete': 'destroy'}), name='upload-detail'),
    path('post/', PostViewSet.as_view({'post': 'create', 'get': 'list'}), name='post'),
    path('post/<int:pk>/', PostViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}),
         name='post-detail'),
    path('follow/', FollowViewSet.as_view({'put': 'update'}), name='follow'),
    path('repost/', RepostViewSet.as_view({'post': 'create'}), name='repost'),
    path('like/<int:pk>/', LikeViewSet.as_view({'post': 'like'}), name='like'),
    path('users/<str:pk>/', UserViewSet.as_view({'get': 'retrieve', 'put': 'update'}), name='user-detail'),
    path('calendar/get/', EventViewSet.as_view({'get': 'list'}), name='calendar-get'),
    path('calendar/', EventViewSet.as_view({'post': 'create'}), name='calendar'),
    path('calendar/<int:pk>/', EventViewSet.as_view({'put': 'update', 'delete': 'destroy'}), name='calendar-detail'),
    path('calendar/mock/', EventViewSet.as_view({'post': 'generate_mock_events'}), name='calendar-mock'),
    path('calendar/byname/', EventViewSet.as_view({'get': 'get_event_by_organization'}), name='calendar-org'),
    path('calendar/upcoming/', EventViewSet.as_view({'get': 'get_upcoming_events'}), name='calendar-upcoming'),
    path('notification/', NotificationViewSet.as_view({'get': 'list'}), name='notification'),
    path('notification/<int:pk>/', NotificationViewSet.as_view({'put': 'update'}), name='notification-detail'),
    path('notification/create/', NotificationViewSet.as_view({'post': 'create'}), name='notification-create'),
    path('notification/delete/', NotificationViewSet.as_view({'delete': 'destroy'}), name='notification-delete'),
    path('organization/', OrganizationViewSet.as_view({'get': 'list'}), name='organization'),
    path('organization/<str:org_name>/', OrganizationViewSet.as_view({'get': 'get_by_name'}),
         name='organization-detail'),
    path('achievement/', AchievementViewSets.as_view({'post': 'create', 'get': 'list'}), name='achievement'),
    path('achievement/<str:pk>/',
         AchievementViewSets.as_view({'get': 'retrieve', 'delete': 'destroy', 'put': 'update'}),
         name='achievement-detail'),
    path('achievement/mock/', AchievementViewSets.as_view({'post': 'mock_achievements'}), name='achievement-mock'),
    path('experience/', ExperienceViewSet.as_view({'post': 'create', 'get': 'list'}), name='experience'),
    path('experience/<int:pk>/', ExperienceViewSet.as_view({'get': 'retrieve', 'delete': 'destroy', 'put': 'update'}),
         name='experience-detail'),
    path('comment/', CommentViewSet.as_view({'post': 'create', 'get': 'list'}), name='comment-list'),
    path('comment/<int:pk>/', CommentViewSet.as_view({'get': 'retrieve', 'delete': 'destroy', 'put': 'update'}),
         name='comment-detail'),
    path('like_comment/<int:pk>/', LikeCommentViewSet.as_view({'post': 'like'}), name='like-comment'),
    #example for using analytic
    #height
    #http://127.0.0.1:8000/services/analytics/?player_name=cr7&analytic_type=run&height=171
    #push_up
    #http://127.0.0.1:8000/services/analytics/?player_name=cr7&analytic_type=push_up
    #sit_up
    #http://127.0.0.1:8000/services/analytics/?player_name=cr7&analytic_type=sit_up
    path('analytics/', AnalyticsViewSet.as_view({'get': 'get_analytics'}), name='analytics'),
]
