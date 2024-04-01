# from rest_framework.decorators import api_view
# from rest_framework import serializers
# from .models.custom_user import CustomUser, Athlete, Scout, Organization
# from django.contrib.auth.hashers import make_password
# from rest_framework import status
# from rest_framework.response import Response
# from rest_framework.authtoken.models import Token
# from django.utils import timezone
# from django.http import HttpRequest
# from django.contrib.auth import get_user_model
# from django.contrib.auth.models import User


# class CustomUserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CustomUser
#         fields = ['role']


# class AthleteSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Athlete
#         fields = '__all__'

#         extra_kwargs = {
#             'organization': {'required': False}
#         }


# class ScoutSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Scout
#         fields = '__all__'

#     extra_kwargs = {
#         'organization': {'required': False}
#     }


# class OrganizationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Organization
#         fields = '__all__'


# @api_view(['POST'])
# def signup(request):
#     if request.method == 'POST':
#         if request.data['password'] != request.data['confirm_password']:
#             return Response({'error': 'Password not match'}, status=status.HTTP_400_BAD_REQUEST)
#         hashed_password = make_password(request.data['confirm_password'])
#         auth_serializer = CustomUserSerializer(data={'username': request.data['username'],
#                                                      'last_name': request.data['last_name'],
#                                                      'role': request.data['role'],
#                                                      'password': hashed_password})
#         if not auth_serializer.is_valid() and s:
#             return Response(auth_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#         auth_serializer.save()
#         response = auth_serializer.data

#         if auth_serializer.data['role'] == 'athlete':
#             serializer_data = {
#                 'username': auth_serializer.data['username'],
#                 'age': request.data['age'],
#                 'position': request.data['position'],
#                 'birth_date': request.data['birth_date'],
#                 'hometown': request.data['hometown'],
#                 'education': request.data['education'],
#                 'description': request.data['description'],
#             }

#             if 'organization' in request.data:
#                 serializer_data['organization'] = request.data['organization']

#             athlete_serializer = AthleteSerializer(data=serializer_data)
#             if athlete_serializer.is_valid():
#                 athlete_serializer.save()
#                 response['athlete'] = athlete_serializer.data

#         if auth_serializer.data['role'] == 'scout':
#             scout_serializer = ScoutSerializer(data={'username': auth_serializer.data['username'],
#                                                      'birth_date': request.data['birth_date'],
#                                                      'hometown': request.data['hometown'],
#                                                      'age': request.data['age'],
#                                                      'organization': request.data['organization'],
#                                                      }
#                                                )
#             if scout_serializer.is_valid():
#                 scout_serializer.save()
#                 response['scout'] = scout_serializer.data

#         if auth_serializer.data['role'] == 'organization':
#             organization_serializer = OrganizationSerializer(data={'username': auth_serializer.data['username'],
#                                                                    'club_name': request.data['club_name']
#                                                                    }
#                                                              )
#             if organization_serializer.is_valid():
#                 organization_serializer.save()
#                 response['organization'] = organization_serializer.data

#         temp = {'username': request.data['username'], 'password': request.data['password']}

#         request = HttpRequest()
#         request.method = 'POST'
#         request.data = temp
#         print(request.data)

#         signin(request)
#         return Response(response, status=status.HTTP_201_CREATED)


# CustomUser = get_user_model()


# @api_view(['POST'])
# def signin(request):
#     if request.method == 'POST':
#         try:
#             user = CustomUser.objects.get(username=request.data['username'])
#         except CustomUser.DoesNotExist:
#             return Response({'message': 'User not found'}, status=status.HTTP_400_BAD_REQUEST)

#         if not user.check_password(request.data['password']):
#             return Response({'message': 'Wrong Password'}, status=status.HTTP_400_BAD_REQUEST)

#         # Authentication successful, generate tokens
#         token, _ = Token.objects.get_or_create(user=user)

#         # Set expiration time for the tokens
#         token.created = timezone.now()
#         token.expires = token.created + timezone.timedelta(hours=2)
#         token.save()

#         return Response({'message': 'Login Success', 'token': token.key, 'expires': token.expires},
#                         status=status.HTTP_200_OK)  # if expired, force user to login again
