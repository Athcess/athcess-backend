from django.db.models import Q
from rest_framework.decorators import api_view
from rest_framework import viewsets
from rest_framework import status
from rest_framework import serializers
from rest_framework.response import Response
from django.contrib.auth.models import User


from ..models.physical_attribute import PhysicalAttribute
from ..models.post import Post
from ..models.event import Event
from users.models.custom_user import CustomUser, Athlete, Scout, Organization


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'


class AthleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Athlete
        fields = '__all__'


class ScoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scout
        fields = '__all__'


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'


class PhysicalAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhysicalAttribute
        fields = '__all__'


class SearchViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def create(self, request, *args, **kwargs):

        type = request.data.get('type')
        data = request.data.get('data', '')

        if type == 'athlete':
            athletes = User.objects.filter(Q(first_name__icontains=data) | Q(last_name__icontains=data))
            serializer = UserSerializer(athletes, many=True)
            return Response(serializer.data)

        elif type == 'scout':
            scouts = User.objects.filter(Q(first_name__icontains=data) | Q(last_name__icontains=data))
            serializer = UserSerializer(scouts, many=True)
            return Response(serializer.data)

        elif type == 'organization':
            organizations = Organization.objects.filter(club_name__icontains=data)
            serializer = OrganizationSerializer(organizations, many=True)
            return Response(serializer.data)

        elif type == 'post':
            posts = Post.objects.filter(description__icontains=data)
            serializer = PostSerializer(posts, many=True)
            return Response(serializer.data)

        tier = Scout.objects.get(username=request.user.username).tier
        filters = request.data.get('filters', {})

        if filters and not tier:
            return Response({'error': 'You are not allowed to use filters'}, status=status.HTTP_403_FORBIDDEN)

        queryset = PhysicalAttribute.objects.all()
        for key, value in filters.items():
            if key in ['height', 'weight', 'sit_up', 'push_up', 'run']:
                queryset = queryset.filter(**{f'{key}': value})

        usernames = list(queryset.values_list('username', flat=True))

        queryset = Athlete.objects.filter(username__in=usernames)
        for key, value in request.query_params.items():
            if key in ['age', 'location', 'position']:
                queryset = queryset.filter(**{f'{key}': value})

        athletes = list(queryset.values_list('username', flat=True))

        users = CustomUser.objects.filter(username__in=athletes)

        serializer = CustomUserSerializer(users, many=True)

        return Response(serializer.data)

