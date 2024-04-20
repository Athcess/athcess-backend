from users.models.custom_user import CustomUser, Athlete, Scout, Admin_organization, Organization
from ..models.post import Post
from ..models.is_friend_of import IsFriendOf
from rest_framework import viewsets, status, permissions, serializers
from rest_framework.response import Response
from django.utils import timezone
from ..models.event import Event


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['post_id', 'username', 'created_at', 'description', 'has_attachment', 'highlight', 'is_repost']


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'


class FeedViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        # Retrieve friends and following
        friends = IsFriendOf.objects.filter(username=CustomUser.objects.get(username=request.user.username)).values_list('username', flat=True)

        following = CustomUser.objects.get(username=request.user).following.split(',')

        # Retrieve posts from friends and following users
        posts = Post.objects.filter(username__in=friends)  # Posts from friends
        events = Event.objects.filter(club_id__in=following)  # Posts from following users

        # Serialize the posts
        # Serialize posts and events separately
        post_serializer = PostSerializer(posts, many=True)
        event_serializer = EventSerializer(events, many=True)

        # Combine serialized data into a single response data
        response_data = {
            'posts': post_serializer.data,
            'events': event_serializer.data
        }
        return Response(response_data, status=status.HTTP_200_OK)
