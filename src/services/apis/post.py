from users.models.custom_user import CustomUser, Athlete, Scout, Admin_organization, Organization
from ..models.post import Post
from ..models.blob_storage import BlobStorage
from rest_framework import viewsets, status, permissions, serializers
from rest_framework.response import Response
from django.utils import timezone


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['post_id', 'username', 'created_at', 'description', 'has_attachment', 'highlight', 'is_repost',
                  'likes']


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        create_at = timezone.now()
        serializer = PostSerializer(data={
            'username': request.user.username,
            'created_at': create_at,
            'description': request.data['description'],
            'has_attachment': request.data['has_attachment'],
            'highlight': request.data['highlight'],
            'is_repost': False

        })

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        for key, value in request.query_params.items():
            queryset = queryset.filter(**{key: value})
        serializer = self.get_serializer(queryset, many=True)

        posts = []
        for i in serializer.data:
            url = BlobStorage.objects.filter(username=i['username'], is_profile_picture=True).values_list('url',
                                                                                                                 flat=True).first()
            i['url'] = url
            posts.append(i)

        return Response(posts, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = PostSerializer(instance, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
