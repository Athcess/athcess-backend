from rest_framework.decorators import api_view
from rest_framework import viewsets
from rest_framework import status
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Q
from ..models.user import User
from ..models.post import Post
from ..models.event import Event


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"


class SearchViewSet(viewsets.ModelViewSet):
    querysetPost = Post.objects.all()
    serializerPost = PostSerializer

    querysetUser = User.objects.all()
    serializerUser = UserSerializer

    @action(detail=False, methods=["get"])
    def search(self, request):
        # query_params = request.query_params
        # search_desc = query_params.get('Description')
        search_type = request.data["type"]
        search_filter = request.data["filter"]
        search_desc = request.data["search_info"]
        # seach_model = [Post, Athlete, Scout, Organization, Events]
        if not search_desc or not search_type:
            return Response("Input value please", status=status.HTTP_400_BAD_REQUEST)
        if search_type == "Post":
            querysetPost = Post.objects.all().filter(Description__icontains=search_desc)
            serializer = PostSerializer(querysetPost, many=True)
        elif search_type == "User":
            tage = search_filter.get("age")
            tsport = search_filter.get("sport")
            tlocation = search_filter.get("location")
            filters = {}
            if tage:
                filters["age"] = tage
            if tsport:
                filters["sport"] = tsport
            if tlocation:
                filters["location"] = tlocation
            querysetUser = User.objects.filter(**filters, name__icontains=search_desc)
            serializer = UserSerializer(querysetUser, many=True)
        return Response(serializer.data)
