from rest_framework.decorators import api_view
from rest_framework import serializers
from .models.custom_user import CustomUser, Athlete, Scout, Admin_organization, Organization
from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from .utils.user_mock import mock_custom_users,mock_athletes, mock_scouts, mock_admins, mock_organizations
from faker import Faker


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
        model = Admin_organization
        fields = '__all__'

class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = '__all__'

@api_view(['POST'])
def mock_custom_user(request):
    if request.method == 'POST':
        num_users = request.data.get('num_users', 10) 
        users = mock_custom_users(num_users)
        serializer = CustomUserSerializer(data=users, many=True)
        if serializer.is_valid():
            serializer.save()
            User.objects.create()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def mock_athlete(request):
    if request.method == 'POST':
        athletes = mock_athletes(num_athletes=1)  # Create one athlete
        if athletes:
            athlete_serializer = AthleteSerializer(athletes[0])
            return Response(athlete_serializer.data, status=status.HTTP_201_CREATED)
        
        return Response({"message": "Failed to create athlete"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def mock_scout(request):
    if request.method == 'POST':
        scouts = mock_scouts(num_scouts=1)  # Create one scout
        if scouts:
            scout_serializer = ScoutSerializer(scouts[0])
            return Response(scout_serializer.data, status=status.HTTP_201_CREATED)
        
        return Response({"message": "Failed to create scout"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def mock_admin(request):
    if request.method == 'POST':
        fake = Faker()
        custom_user = CustomUser.objects.create(
            username=fake.user_name(),
            password=fake.password(),
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            role='admin'
        )
        
        admin_organization = Admin_organization.objects.create(username=custom_user)
        
        return Response("Admin created successfully.", status=status.HTTP_201_CREATED)
    
    return Response("Invalid request method.", status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
def mock_organization(request):
    if request.method == 'POST':
        mock_data = mock_organizations()
        serializer = OrganizationSerializer(data=mock_data, many=True) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
