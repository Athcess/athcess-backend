from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Q
from django.utils import timezone
from datetime import datetime
from django.http import JsonResponse
from rest_framework import viewsets, status, permissions, serializers
from ..models.blob_storage import BlobStorage
from ..models.physical_attribute import PhysicalAttribute
from utils.analytics.situp import *
from utils.analytics.sprint import *
from utils.analytics.pushup import *

class BlobStorageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlobStorage
        fields = '__all__'

class PhysicalAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhysicalAttribute
        fields = '__all__'

class BlobStorageViewSet(viewsets.ModelViewSet):
    queryset = BlobStorage.objects.all()
    serializer_class = BlobStorageSerializer

    def get_analytics(self, request, *args, **kwargs):
        username = request.query_params.get('player_name')
        physical_attribute_type = request.query_params.get('analytic_type')
        else:
            # Physical attribute does not exist, create a new one
            if physical_attribute_type == 'sit_up':
                count = count_situps(url)

            elif physical_attribute_type == 'push_up':
                count = count_push_ups(url)

            elif physical_attribute_type == 'run':
                speed = calculate_speed(url, height)
                physical_attribute = {
                    'create_at': timezone.now(),
                    'username': username,
                    'run': speed,
                    'height': height,
                }
                serializer = PhysicalAttributeSerializer(data=physical_attribute)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        #get blobstorage with latest date
        blobstorage = BlobStorage.objects.filter(username=username, physical_attribute_type=physical_attribute_type).latest('created_at')
        return Response({'message': 'Invalid analytic type. There are only 3 types of analytics: sit_up, push_up, run'},status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)