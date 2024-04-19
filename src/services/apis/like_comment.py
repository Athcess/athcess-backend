from users.models.custom_user import CustomUser, Athlete, Scout, Admin_organization, Organization
from ..models.post import Post
from ..models.comment import Comment
from rest_framework import viewsets, status, permissions, serializers
from rest_framework.response import Response
from django.utils import timezone


class LikeCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['username', 'comment_id']


class LikeCommentViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def like(self, request, **kwargs):
        try:
            post = Comment.objects.get(comment_id=kwargs.get('pk'))
        except Post.DoesNotExist:
            return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

        response = post.like(request.user.username)
        return Response(response, status=status.HTTP_200_OK)



