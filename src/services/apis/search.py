from rest_framework.decorators import api_view
from rest_framework import viewsets
from rest_framework import status
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Q
from ..models.physical_attribute import PhysicalAttribute
from ..models.post import Post
from ..models.event import Event
from users.models.custom_user import CustomUser, Athlete, Scout, Organization

class CustomUserSerializer(serializers.ModelSerializer) :
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name']

class AthleteSerializer(serializers.ModelSerializer) :
    class Meta:
        model = Athlete
        fields = '__all__'

class ScoutSerializer(serializers.ModelSerializer) :
    class Meta:
        model = Scout
        fields = '__all__'

class OrganizationSerializer(serializers.ModelSerializer) :
    class Meta:
        model = Organization
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer) :
    class Meta:
        model = Post
        fields = '__all__'

class EventSerializer(serializers.ModelSerializer) :
    class Meta:
        model = Event
        fields = '__all__'

class SearchViewSet(viewsets.ModelViewSet) :
    querysetPost = Post.objects.all()
    serializerPost = PostSerializer

    querysetAthlete = Athlete.objects.all()
    serializerAthlete = AthleteSerializer

    querysetOrg = Organization.objects.all()
    serializerOrg = OrganizationSerializer

    querysetScout = Scout.objects.all()
    serializerScout = ScoutSerializer

    querysetUser = CustomUser.objects.all()
    serializerUser = CustomUserSerializer

    querysetEvent = Event.objects.all()
    serializerEvent = EventSerializer


    @action(detail=False, methods=['get'])
    def search(self, request) :
        search_type = request.data['type']
        search_filter = request.data['filter']
        search_desc = request.data['search_info']
        if not search_desc or not search_type :
            return Response('Input value please', status=status.HTTP_400_BAD_REQUEST)
        if search_type == 'Post' :
            querysetPost = Post.objects.all().filter(Q(description__icontains=search_desc) 
            | Q(username__first_name__icontains=search_desc) | Q(username__last_name__icontains=search_desc))
            serializer = PostSerializer(querysetPost, many=True, data=querysetPost)
        elif search_type == 'Athlete' :
            tage = search_filter.get('age')
            tlocation = search_filter.get('hometown')
            filters = {}
            if tage:
                filters['age'] = tage
            if tlocation:
                filters['hometown'] = tlocation
            if search_desc.isdigit() :
                querysetAthlete = Athlete.objects.filter(Q(age__exact=search_desc), **filters)
            else :
                querysetAthlete = Athlete.objects.filter(Q(hometown__icontains=search_desc) | Q(position=search_desc) 
                | Q(username__first_name__icontains=search_desc)| Q(username__last_name__icontains=search_desc), **filters)
            serializer = AthleteSerializer(querysetAthlete, many=True, data=querysetAthlete)
        elif search_type == 'Scout' :
            tage = search_filter.get('age')
            tlocation = search_filter.get('hometown')
            filters = {}
            if tage:
                filters['age'] = tage
            if tlocation:
                filters['hometown'] = tlocation
            querysetScout = Scout.objects.filter((Q(hometown__icontains=search_desc))
            | Q(username__first_name__icontains=search_desc) | Q(username__last_name__icontains=search_desc), **filters)
            serializer = ScoutSerializer(querysetScout, many=True, data=querysetScout)
        elif search_type == 'Organization' :
            tage = search_filter.get('age')       
            tlocation = search_filter.get('location')
            filters = {}
            if tage:
                filters['age'] = tage
            if tlocation:
                filters['hometown'] = tlocation
            querysetOrg = Organization.objects.filter(club_name__icontains=search_desc, **filters)
            serializer = OrganizationSerializer(querysetOrg, many=True, data=querysetOrg)
        elif search_type == 'Event' :
            tage = search_filter.get('age')
            tlocation = search_filter.get('hometown')
            filters = {}
            if tage:
                filters['age'] = tage
            if tlocation:
                filters['hometown'] = tlocation
            querysetEvent = Event.objects.filter((Q(content__icontains=search_desc) | Q(created_at__exact=search_desc)), **filters)
            serializer = AthleteSerializer(querysetEvent, many=True, data=querysetEvent)
        if serializer.is_valid() :
            return Response(serializer.data)
        else :
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserSerializer(serializers.ModelSerializer) :
    class Meta:
        model = CustomUser
        fields = '__all__'

class PhysicalAttributeSerializer(serializers.ModelSerializer) :
    class Meta:
        model = PhysicalAttribute
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer) :
    class Meta:
        model = Post
        fields = '__all__'

class SearchViewSet(viewsets.ModelViewSet) :
    querysetPost = Post.objects.all()
    serializerPost = PostSerializer

    querysetUser = CustomUser.objects.all()
    serializerUser = UserSerializer

    @action(detail=False, methods=['get'])
    def search(self, request) :
        # query_params = request.query_params
        # search_desc = query_params.get('Description')
        search_type = request.data['type']
        search_filter = request.data['filter']
        search_desc = request.data['search_info']
        # seach_model = [Post, Athlete, Scout, Organization, Events]
        if not search_desc or not search_type :
            return Response('Input value please', status=status.HTTP_400_BAD_REQUEST)
        if search_type == 'Post' :
            querysetPost = Post.objects.all().filter(Description__icontains=search_desc)
            serializer = PostSerializer(querysetPost, many=True)
        elif search_type == 'User' :
            tage = search_filter.get('age')
            tsport = search_filter.get('sport')
            tlocation = search_filter.get('location')
            filters = {}
            if tage:
                filters['age'] = tage
            if tsport:
                filters['sport'] = tsport
            if tlocation:
                filters['location'] = tlocation
            querysetUser = User.objects.filter(**filters, name__icontains=search_desc)
            serializer = UserSerializer(querysetUser, many=True)
        return Response(serializer.data)

    