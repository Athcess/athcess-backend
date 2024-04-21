from django.db.models import Q
from rest_framework.decorators import api_view
from rest_framework import viewsets, permissions
from rest_framework import status
from rest_framework import serializers
from rest_framework.response import Response
from django.contrib.auth.models import User

from ..models.physical_attribute import PhysicalAttribute
from ..models.post import Post
from ..models.event import Event
from users.models.custom_user import CustomUser, Athlete, Scout, Organization
from ..models.search import Search


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']


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
        fields = ['username', 'club_name', 'location', 'followers']


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
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):

        type = request.data.get('type')
        data = request.data.get('data', '')

        if type == 'athlete':
            athletes_data = []

            athletes = CustomUser.objects.filter(
                Q(first_name__icontains=data) | Q(last_name__icontains=data),
                role='athlete'
            )

            athlete_details = Athlete.objects.filter(username__in=athletes.values_list('username', flat=True))

            for athlete in athletes:
                athlete_data = {
                    'username': athlete.username,
                    'first_name': athlete.first_name,
                    'last_name': athlete.last_name,
                    **athlete_details.filter(username=athlete.username).values('age', 'hometown', 'position').first()
                }

                athletes_data.append(athlete_data)

            search = Search.objects.create(data=athletes_data)
            search_id = search.search_id

            return Response({'search_id': search_id, 'data': athletes_data})

        elif type == 'scout':
            scouts_data = []
            scouts = CustomUser.objects.filter(Q(first_name__icontains=data) | Q(last_name__icontains=data),
                                               role='scout')

            scout_details = Scout.objects.filter(username__in=scouts.values_list('username', flat=True))

            for scout in scouts:
                scout_data = {
                    'username': scout.username,
                    'first_name': scout.first_name,
                    'last_name': scout.last_name,
                    **scout_details.filter(username=scout.username).values('hometown').first()
                }
                scouts_data.append(scout_data)

            search = Search.objects.create(data=scouts_data)
            search_id = search.search_id

            return Response({'search_id': search_id, 'data': scouts_data})

        elif type == 'organization':
            organizations = Organization.objects.filter(club_name__icontains=data)
            serializer = OrganizationSerializer(organizations, many=True)
            search = Search.objects.create(data=serializer.data)
            search_id = search.search_id
            return Response({'search_id': search_id, 'data': serializer.data})

        elif type == 'post':
            posts = Post.objects.filter(description__icontains=data)
            serializer = PostSerializer(posts, many=True)
            search = Search.objects.create(data=serializer.data)
            search_id = search.search_id
            return Response({'search_id': search_id, 'data': serializer.data})

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
        for key, value in filters.items():
            if key in ['age', 'location', 'position']:
                queryset = queryset.filter(**{f'{key}': value})

        athletes = list(queryset.values_list('username', flat=True))

        users = CustomUser.objects.filter(username__in=athletes)

        serializer = CustomUserSerializer(users, many=True)
        search = Search.objects.create(data=serializer.data)
        search_id = search.search_id
        return Response({'search_id': search_id, 'data': serializer.data})

    def retrieve(self, request, *args, **kwargs):
        search = Search.objects.get(pk=kwargs['pk'])
        return Response({'search_id': search.search_id, 'data': search.data})
