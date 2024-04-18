from rest_framework import viewsets, status, permissions, serializers
from rest_framework.response import Response
from azure.storage.blob import BlobServiceClient, generate_blob_sas, BlobSasPermissions
from ..models.blob_storage import BlobStorage
from Backend.config import azure_account_name, azure_account_key
from django.conf import settings
from datetime import datetime, timedelta
import uuid
import hashlib
import os
import mimetypes

BANNED_TYPES = ['application/javascript', 'application/exe', 'application/x-exe', 'application/dos-exe',
                'vms/exe', 'application/x-winexe', 'application/msdos-windows', 'application/x-msdos-program']
TOKEN_EXPIRY_DURATION = 10
STATUS_LIST = ['failed', 'pending']
AZURE_CONTAINER = 'media'
AZURE_BLOB_URL = 'https://{account_name}.blob.core.windows.net'


# Serializer class
class BlobSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlobStorage
        fields = '__all__'


class AzureBlobClient:
    def __init__(self, account_name, account_key):
        self.account_name = azure_account_name
        self.account_key = azure_account_key
        # Initialize BlobServiceClient
        self.blob_service_client = BlobServiceClient(account_url=AZURE_BLOB_URL.format(account_name=self.account_name),
                                                     credential=self.account_key)

    def generate_sas_token(self, blob_name):
        return generate_blob_sas(account_name=self.account_name,
                                 container_name=AZURE_CONTAINER,
                                 blob_name=blob_name,
                                 account_key=self.account_key,
                                 permission=BlobSasPermissions(write=True),
                                 expiry=datetime.now() + timedelta(minutes=TOKEN_EXPIRY_DURATION)
                                 )


class UploadFileViewSet(viewsets.ModelViewSet):
    queryset = BlobStorage.objects.all()
    serializer_class = BlobSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        # Check if required fields are provided
        required_fields = ['file_name', 'content_type', 'file_size']
        if not all(request.data.get(field) for field in required_fields):
            return Response({'error': f'{", ".join(required_fields)} are required'}, status=status.HTTP_400_BAD_REQUEST)

        full_file_name = request.data['file_name']
        content_type = request.data['content_type']
        file_size = request.data['file_size']

        if mimetypes.guess_type(full_file_name)[0] != content_type or content_type in BANNED_TYPES:
            return Response({'error': 'Invalid content type or banned types'}, status=status.HTTP_400_BAD_REQUEST)

        file_name, file_extension = os.path.splitext(full_file_name)
        encrypted_file_name = f'{hashlib.sha256(str(uuid.uuid4()).encode()).hexdigest()}{file_extension}'

        try:
            client = AzureBlobClient(settings.AZURE_CONFIG['account_name'], settings.AZURE_CONFIG['account_key'])
            signed_token = client.generate_sas_token(encrypted_file_name)
        except Exception as e:
            return Response({'error': f'Failed to generate token: {e.__class__.__name__}, {str(e)}'},
                            status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        file_path = f'{AZURE_BLOB_URL.format(account_name=settings.AZURE_CONFIG["account_name"])}/{AZURE_CONTAINER}/{encrypted_file_name}'
        sas_url = f'{file_path}?{signed_token}'

        serializer = self.serializer_class(data={'url': file_path,
                                                 'file_name': full_file_name,
                                                 'file_size': file_size,
                                                 'content_type': content_type,
                                                 'username': self.request.user.username,
                                                 'description': self.request.data.get('description', None),
                                                 'status': STATUS_LIST[1],
                                                 })

        if serializer.is_valid():
            serializer.save()
            return Response({'signed_url': sas_url, 'postgras_id': serializer.data['blob_id']}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        # Validate and update fields
        serializer = self.serializer_class(instance, data=request.data, partial=True)  # Allow partial updates
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
