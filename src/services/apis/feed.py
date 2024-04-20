from users.models.custom_user import CustomUser, Athlete, Scout, Admin_organization, Organization
from ..models.post import Post
from ..models.is_friend_of import IsFriendOf
from rest_framework import viewsets, status, permissions, serializers
from rest_framework.response import Response
from django.utils import timezone

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['post_id', 'username', 'created_at', 'description', 'has_attachment', 'highlight', 'is_repost']


class FeedViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        # Retrieve friends and following
        friends = IsFriendOf.objects.filter(username=request.user).values_list('friend__username', flat=True)
        following = CustomUser.objects.get(username=request.user).following.split(',')

        # Retrieve posts from friends and following users
        posts = Post.objects.filter(username__in=friends)  # Posts from friends
        events = Post.objects.filter(username__in=following)  # Posts from following users

        # Combine posts and events
        combined_posts = posts.union(events)

        # Serialize the posts
        serializer = PostSerializer(combined_posts, many=True)

        return Response(serializer.data)
