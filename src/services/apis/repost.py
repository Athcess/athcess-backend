from users.models.custom_user import CustomUser, Athlete, Scout, Admin_organization, Organization
from ..models.post import Post
from rest_framework import viewsets, status, permissions, serializers
from rest_framework.response import Response
from django.utils import timezone

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['post_id', 'username', 'created_at', 'description', 'has_attachment', 'highlight', 'is_repost']



class RepostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        create_at = timezone.now()

        try:
            Post.objects.get(post_id=request.data['post_id'])
        except Post.DoesNotExist:
            return Response({'error': 'Post does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = PostSerializer(data={
                                            'username': request.user.username,
                                            'created_at': create_at,
                                            'description': request.data['post_id'],
                                            'highlight': request.data['highlight'],
                                            'has_attachment': False,
                                            'is_repost': True
                                          })

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)