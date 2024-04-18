from rest_framework import serializers
from users.models.custom_user import CustomUser, Athlete, Scout, Admin_organization
from ..models.blob_storage import BlobStorage
from ..models.achievement import Achievement
from ..models.experience import Experience
from ..models.physical_attribute import PhysicalAttribute
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from django.contrib.auth.models import User


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


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        try:
            username = kwargs.get('pk')
            role = CustomUser.objects.get(username=username).role

            if role == 'athlete':
                instance = Athlete.objects.get(username=username)
                serializer = AthleteSerializer(instance, context={'request': request})
                response = serializer.data

            elif role == 'scout':
                instance = Scout.objects.get(username=username)
                serializer = ScoutSerializer(instance, context={'request': request})
                response = serializer.data

            else:
                return Response({"message": "Invalid role???"}, status=status.HTTP_400_BAD_REQUEST)

            # profile picture
            try:
                profile_picture_url = BlobStorage.objects.get(username=username, is_profile_picture=True).url
                response['profile_picture'] = profile_picture_url
            except BlobStorage.DoesNotExist:
                response['profile_picture'] = None

            # achievements
            try:
                achievements = Achievement.objects.filter(username=username)
                response['achievements'] = [{'achievement': achievement.achievement, 'date': achievement.date} for
                                            achievement in achievements]
            except Achievement.DoesNotExist:
                response['achievement'] = None

            # experience
            try:
                experiences = Experience.objects.get(username=username)
                response['experiences'] = [{'topic': experience.topic, 'date': experience.date, 'description':
                                            experience.description} for experience in experiences]
            except Experience.DoesNotExist:
                response['experience'] = None

            # define tier
            tier = False
            if role == 'scout':
                tier = Scout.objects.get(username=username).tier

            own = request.user.username == kwargs.get('pk')

            # physical attribute
            if role == 'athlete':
                try:
                    physical_attributes = PhysicalAttribute.objects.get(username=username)
                    response['physical_attribute'] = [
                        {
                            'height': physical_attribute.height,
                            'weight': physical_attribute.weight,
                            'fat_mass': physical_attribute.fat_mass,
                            'muscle_mass': physical_attribute.muscle_mass,
                            'run': physical_attribute.run if tier else None,
                            'push_up': physical_attribute.push_up if tier or own else None,
                            'sit_up': physical_attribute.sit_up if tier or own else None
                        }
                        for physical_attribute in physical_attributes
                    ]
                except PhysicalAttribute.DoesNotExist:
                    response['physical_attribute'] = None

            response['first_name'] = User.objects.get(username=username).first_name
            response['last_name'] = User.objects.get(username=username).last_name

            return Response(response)

        except CustomUser.DoesNotExist:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, *args, **kwargs):
        try:
            username = kwargs.get('pk')
            role = CustomUser.objects.get(username=username).role
        except CustomUser.DoesNotExist:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        if role == 'athlete':
            instance = Athlete.objects.get(username=username)
            serializer = AthleteSerializer(instance, data=request.data, context={'request': request})

        elif role == 'scout':
            instance = Scout.objects.get(username=username)
            serializer = ScoutSerializer(instance, data=request.data, context={'request': request})

        else:
            return Response({"message": "Invalid role???"}, status=status.HTTP_400_BAD_REQUEST)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        response = serializer.data

        return Response(response)







