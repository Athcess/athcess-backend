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
from users.models.custom_user import Organization

class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = '__all__'

class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer

    def get(self, request, *args, **kwargs):
        organizations = Organization.objects.all()
        return Response({"organizations": organizations}, status=status.HTTP_200_OK)

    def get_by_name(self, request, org_name=None):
        organization = Organization.objects.get(club_name=org_name)
        serialized_organization = OrganizationSerializer(organization).data
        return Response({"organization": serialized_organization}, status=status.HTTP_200_OK)