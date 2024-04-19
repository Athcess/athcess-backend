from users.models.custom_user import CustomUser, Athlete, Scout, Admin_organization, Organization
from ..models.post import Post
from ..models.comment import Comment
from rest_framework import viewsets, status, permissions, serializers
from rest_framework.response import Response
from django.utils import timezone

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['username', 'post', 'created_at', 'likes', 'description']


class CommentViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def create(self, request, *args, **kwargs):
        created_at = timezone.now()
        serializer = CommentSerializer(data={
                                            'username': request.user.username,
                                            'post': request.data['post'],
                                            'created_at': created_at,
                                            'description': request.data['description']
                                          })

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        queryset = Comment.objects.filter(post=request.data['post'])
        serializer = CommentSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = Comment.objects.get(comment_id=kwargs['pk'])
        serializer = CommentSerializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = Comment.objects.get(comment_id=kwargs['pk'])
        serializer = CommentSerializer(instance, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = Comment.objects.get(comment_id=kwargs['pk'])
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




