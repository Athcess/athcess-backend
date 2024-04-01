from rest_framework.decorators import api_view
from rest_framework import serializers
from .models.custom_user import CustomUser, Athlete, Scout, Organization
from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken, Token


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
        fields = '__all__'

    extra_kwargs = {
        'organization': {'required': False}
    }


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = '__all__'


@api_view(['POST'])
def signup(request):
    if request.method == 'POST':
        if request.data['password'] != request.data['confirm_password']:
            return Response({'error': 'Password not match'}, status=status.HTTP_400_BAD_REQUEST)
        hashed_password = make_password(request.data['confirm_password'])
        auth_serializer = CustomUserSerializer(data={'username': request.data['username'],
                                                     'role': request.data['role'],
                                                     'password': hashed_password})
        if not auth_serializer.is_valid():
            return Response(auth_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        auth_serializer.save()
        User.objects.create(username=request.data['username'], first_name=request.data['first_name']
                            , last_name=request.data['last_name'], password=hashed_password)

        response = auth_serializer.data

        if auth_serializer.data['role'] == 'athlete':
            serializer_data = {
                'username': auth_serializer.data['username'],
                'age': request.data['age'],
                'position': request.data['position'],
                'birth_date': request.data['birth_date'],
                'hometown': request.data['hometown'],
                'education': request.data['education'],
                'description': request.data['description'],
            }

            """if 'organization' in request.data:
                serializer_data['organization'] = request.data['organization']
"""
            athlete_serializer = AthleteSerializer(data=serializer_data)
            if athlete_serializer.is_valid():
                athlete_serializer.save()
                response['athlete'] = athlete_serializer.data

        if auth_serializer.data['role'] == 'scout':
            serializer_data = {'username': auth_serializer.data['username'],
                               'birth_date': request.data['birth_date'],
                               'hometown': request.data['hometown'],
                               'age': request.data['age'],
                               }

            """if 'organization' in request.data:
                serializer_data['organization'] = request.data['organization']"""
            scout_serializer = ScoutSerializer(data=serializer_data)

            if scout_serializer.is_valid():
                scout_serializer.save()
                response['scout'] = scout_serializer.data

        """if auth_serializer.data['role'] == 'organization':
            organization_serializer = OrganizationSerializer(data={'username': auth_serializer.data['username'],
                                                                   'club_name': request.data['club_name']
                                                                   }
                                                             )
            if organization_serializer.is_valid():
                organization_serializer.save()
                response['organization'] = organization_serializer.data
"""
        return Response(response, status=status.HTTP_201_CREATED)

CustomUser = get_user_model()



@api_view(['POST'])
def signin(request):
    if request.method == 'POST':
        try:
            user = User.objects.get(username=request.data['username'])
        except CustomUser.DoesNotExist:
            return Response({'message': 'User not found'}, status=status.HTTP_400_BAD_REQUEST)

        if not user.check_password(request.data['password']):
            return Response({'message': 'Wrong Password'}, status=status.HTTP_400_BAD_REQUEST)

        # Authentication successful, generate JWT tokens
        refresh = RefreshToken.for_user(user)

        return Response({'message': 'Login Success', 'access_token': str(refresh.access_token),
                         'refresh_token': str(refresh)},
                        status=status.HTTP_200_OK)
