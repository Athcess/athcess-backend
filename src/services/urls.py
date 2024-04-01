from django.urls import path
from .apis.search import SearchViewSet

urlpatterns = [
    path('search/', SearchViewSet.searched , name='searched')
]