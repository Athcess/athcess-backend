from rest_framework.decorators import api_view
from rest_framework import viewsets
from rest_framework import status
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Q
from ..models.post import Post
from ..models.event import Event
from django.utils import timezone
from ..utils.mock_event import mock_event_data

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"

@api_view(['GET'])
def get_event(request):
    if request.method == 'GET':
        events = Event.objects.all() 
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def create_event(request):
    if request.method == 'POST':
        data = {
            'event_id': request.data.get('event_id'),
            'club': request.data.get('org_name'),
            'content': request.data.get('content'),
            'created_at': timezone.now(),
        }
        event_serializer = EventSerializer(data=data)
        if event_serializer.is_valid():
            event_serializer.save()
            return Response(event_serializer.data, status=status.HTTP_201_CREATED)
        return Response(event_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_event(request):
    if request.method == 'DELETE':
        event_id = request.data.get('event_id')
        if event_id:
            try:
                event = Event.objects.get(id=event_id)
                event.delete()
                return Response({'message': 'Event deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
            except Event.DoesNotExist:
                return Response({'message': 'Event not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'message': 'Event ID not provided'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def update_event(request):
    if request.method == 'PUT':
        event_id = request.data.get('event_id')
        updated_content = request.data.get('updated_content')
        if event_id and updated_content:
            try:
                event = Event.objects.get(id=event_id)
                event.content = updated_content
                event.save()
                serializer = EventSerializer(event)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Event.DoesNotExist:
                return Response({'message': 'Event not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'message': 'Event ID or Updated Content not provided'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def generate_mock_events(request):
    if request.method == 'POST':
        num_events = request.data.get('num_events', 10) 
        events_data = mock_event_data(num_events=num_events)
        created_events = []
        for event_data in events_data:
            event = Event.objects.create(
                club=event_data.club,
                content=event_data.content,
                created_at=event_data.created_at,
                like=event_data.like
            )
            created_events.append(event)
        
        return Response({'message': f'{num_events} mock events created successfully'}, status=status.HTTP_201_CREATED)