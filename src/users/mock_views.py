from rest_framework.decorators import api_view
from rest_framework import serializers
from .models.custom_user import CustomUser, Athlete, Scout, Admin
from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from .utils.user_mock import mock_athletes, mock_scouts, mock_admins, mock_organizations

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['role', 'username']


class AthleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Athlete
        fields = '__all__'

        extra_kwargs = {
            'organization': {'required': False}
        }


class ScoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scout
        fields = ['username', 'birth_date', 'hometown', 'age', 'tier']

    extra_kwargs = {
        'organization': {'required': False}
    }


class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = '__all__'

@api_view(['POST'])
def mock_athlete(request):
    if request.method == 'POST':
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            custom_user = serializer.save()
            athlete_data = mock_athletes()
            athlete_data['username'] = custom_user.username
            athlete_serializer = AthleteSerializer(data=athlete_data)
            if athlete_serializer.is_valid():
                athlete_serializer.save()
                return Response(athlete_serializer.data, status=status.HTTP_201_CREATED)
            
            return Response(athlete_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def mock_scout(request):
    if request.method == 'POST':
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            custom_user = serializer.save()
            scout_data = mock_scouts() 
            scout_data['username'] = custom_user.username
            scout_serializer = ScoutSerializer(data=scout_data)
            if scout_serializer.is_valid():
                scout_serializer.save()
                return Response(scout_serializer.data, status=status.HTTP_201_CREATED)
            
            return Response(scout_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def mock_admin(request):
    if request.method == 'POST':
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            custom_user = serializer.save()
            admin_data = mock_admins()
            admin_data['username'] = custom_user.username
            admin_serializer = AdminSerializer(data=admin_data)
            if admin_serializer.is_valid():
                admin_serializer.save()
                return Response(admin_serializer.data, status=status.HTTP_201_CREATED)
            
            return Response(admin_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def mock_organization(request):
    if request.method == 'POST':
        # Assuming request.data contains mock organization data
        mock_data = mock_organizations()  # Mock organization data
        serializer = OrganizationSerializer(data=mock_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
