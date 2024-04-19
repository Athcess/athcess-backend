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

        #get blobstorage with latest date
        blobstorage = BlobStorage.objects.filter(username=username, physical_attribute_type=physical_attribute_type).latest('created_at')

