from users.models.custom_user import CustomUser, Athlete, Scout, Admin_organization, Organization
from ..models.post import Post
from ..models.is_friend_of import IsFriendOf
from rest_framework import viewsets, status, permissions, serializers
from rest_framework.response import Response
from django.utils import timezone


class IsFriendOfSerializer(serializers.ModelSerializer):
    class Meta:
        model = IsFriendOf
        fields = ['id', 'username', 'friend_username', 'status', 'since']


class IsFriendOfViewSet(viewsets.ModelViewSet):
    queryset = IsFriendOf.objects.all()
    serializer_class = IsFriendOfSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        create_at = timezone.now()
        serializer = IsFriendOfSerializer(data={
            'username': request.user.username,
            'friend_username': request.data['friend_username'],
            'status': 'pending',
            'since': create_at
        })

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if request.user.username == request.data['friend_username']:
            return Response({'error': 'Cannot add yourself as friend'}, status=status.HTTP_400_BAD_REQUEST)

        if IsFriendOf.objects.filter(username=request.data['friend_username'],
                                     friend_username=request.user.username).exists():
            if IsFriendOf.objects.get(username=request.data['friend_username'],
                                      friend_username=request.user.username).status == 'accepted':
                return Response({'error': 'You are already friends'}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'error': 'They have sent you a friend request'}, status=status.HTTP_400_BAD_REQUEST)

        if IsFriendOf.objects.filter(username=request.user.username,
                                     friend_username=request.data['friend_username']).exists():
            return Response({'error': 'You have sent them a friend request'}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()

        response = serializer.data

        return Response(response, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        if request.data['status'] == 'rejected':
            if instance.status == 'accepted':
                return Response({'error': 'You are already friends'}, status=status.HTTP_400_BAD_REQUEST)
            instance.delete()
            return Response({'message': 'Friend request rejected'}, status=status.HTTP_200_OK)

        if request.data['status'] == 'accepted':
            if instance.friend_username.username != request.user.username:
                return Response({'error': 'You cannot accept a friend request that is not yours'}, status=status.HTTP_400_BAD_REQUEST)
            instance.since = timezone.now()
            instance.status = 'accepted'
            instance.save()
            serializer = IsFriendOfSerializer(data={
                'username': instance.friend_username.username,
                'friend_username': instance.username.username,
                'status': 'accepted',
                'since': instance.since
            })

            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            serializer.save()
            return Response({'message': serializer.data['friend_username']+' is now your friend'}, status=status.HTTP_200_OK)

        return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        queryset = IsFriendOf.objects.all()
        for key, value in request.query_params.items():
            queryset = queryset.filter(**{key: value})
        serializer = IsFriendOfSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
