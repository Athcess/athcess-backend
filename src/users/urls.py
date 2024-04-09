from django.urls import path
from . import views
from . import mock_views

urlpatterns = [
    #signup and signin
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    #mock data for dev only no prod.
    path('mock/users/', mock_views.mock_custom_user, name='mock_custom_user'),
    path('mock/athlete/', mock_views.mock_athlete, name='mock_athlete'),
    path('mock/scout/', mock_views.mock_scout, name='mock_scout'),
    path('mock/admin/', mock_views.mock_admin, name='mock_admin'),
    path('mock/organization/', mock_views.mock_organization, name='mock_organization'),
]
