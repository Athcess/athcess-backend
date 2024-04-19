from rest_framework.decorators import api_view
from rest_framework import viewsets
from rest_framework import status
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Q
from django.utils import timezone
from datetime import datetime
from django.http import JsonResponse
from ..models.notification import Notification

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    def list(self, request, *args, **kwargs):
        queryset = Notification.objects.all()
        for key, value in request.query_params.items():
            queryset = queryset.filter(**{key: value})
        serializer = NotificationSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        data = {
            'username': request.data.get('username'),
            'content': request.data.get('content'),
            'type': request.data.get('type'),
        }
        notification_serializer = NotificationSerializer(data=data)
        if notification_serializer.is_valid():
            notification_serializer.save()
            return Response(notification_serializer.data, status=status.HTTP_201_CREATED)
        return Response(notification_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        updated_content = request.data.get('updated_content')
        if updated_content:
            instance.content = updated_content
            instance.save()
            serializer = NotificationSerializer(instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'message': 'Updated Content not provided'}, status=status.HTTP_400_BAD_REQUEST)
