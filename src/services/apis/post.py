from users.models.custom_user import CustomUser, Athlete, Scout, Admin, Organization
from ..models.post import Post
from rest_framework import viewsets, status, permissions, serializers
from rest_framework.response import Response
from django.utils import timezone

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['username', 'created_at', 'description', 'has_attachment']


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        create_at = timezone.now()
        serializer = PostSerializer(data={
                                            'username': request.user,
                                            'created_at': create_at,
                                            'description': request.data['description'],
                                            'has_attachment': request.data['has_attachment']
                                          })

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)