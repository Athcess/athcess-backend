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
from django.contrib.auth.models import User as AuthUser
from django.utils import timezone 


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

class AuthUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthUser
        fields = ['username', 'password', 'first_name', 'last_name']

@api_view(['POST'])
def mock_custom_user(request):
    if request.method == 'POST':
        num_users = request.data.get('num_users', 10) 
        users, auth_user = mock_custom_users(num_users)
        serializer = CustomUserSerializer(data=users, many=True)
        auth_serializer = AuthUserSerializer(data=auth_user, many=True)
        if not auth_serializer.is_valid():
            return Response(auth_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        auth_serializer.save()
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def mock_athlete(request):
    if request.method == 'POST':
        athlete, auth_user = mock_athletes(num_athletes=1)
        auth_serializer = AuthUserSerializer(data=auth_user, many=True)
        if not auth_serializer.is_valid():
            return Response(auth_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        auth_serializer.save()
        athlete_serializer = AthleteSerializer(data=athlete, many=True)
        if athlete_serializer.is_valid():
            athlete_serializer.save()
            return Response(athlete_serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(athlete_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def mock_scout(request):
    if request.method == 'POST':
        scouts, auth_users = mock_scouts(num_scouts=1) 

        serialized_scouts = [ScoutSerializer(scout).data for scout in scouts]
        serialized_auth_users = auth_users 
        scout_serializer = ScoutSerializer(data=serialized_scouts, many=True)
        auth_serializer = AuthUserSerializer(data=serialized_auth_users, many=True)

        if scout_serializer.is_valid() and auth_serializer.is_valid():
            scout_serializer.save()
            auth_serializer.save()

            return Response({
                'scouts': scout_serializer.data,
                'auth_users': auth_serializer.data
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'scout_errors': scout_serializer.errors if not scout_serializer.is_valid() else None,
                'auth_errors': auth_serializer.errors if not auth_serializer.is_valid() else None,
            }, status=status.HTTP_400_BAD_REQUEST)

    return Response("Invalid request method.", status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def mock_admin(request):
    if request.method == 'POST':
        username = fake.user_name()
        password = fake.password()
        first_name = fake.first_name()
        last_name = fake.last_name()

        custom_user = CustomUser.objects.create(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            role='admin'
        )
        
        admin_organization = Admin_organization.objects.create(username=custom_user)

        auth_serializer = AuthUserSerializer(
            data={
                'username': username,
                'password': password,
                'first_name': first_name,
                'last_name': last_name,
            }
        )
        if not auth_serializer.is_valid():
            return Response(auth_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        auth_serializer.save()
        
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
