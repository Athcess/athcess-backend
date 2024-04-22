from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Q
from ..models.post import Post
from ..models.blob_storage import BlobStorage
from ..models.event import Event
from django.utils import timezone
from ..utils.mock_event import mock_event_data
from ..utils.calendar_utils import create_calendar, append_event
from datetime import datetime
from django.http import JsonResponse
from rest_framework import viewsets, status, permissions, serializers
from users.models.custom_user import Organization, CustomUser


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'], url_path='get-calendar')
    def get(self, request, *args, **kwargs):
        now = datetime.now()
        year = now.year
        month = now.month
        day = now.day
        calendar_data = create_calendar(year, month)
        events = Event.objects.all()
        calendar_data = append_event(calendar_data, day, events)
        return Response({"calendar": calendar_data}, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        data = {
            'club': Organization.objects.get(username=request.user.username).club_name,
            'content': request.data.get('content'),
            'created_at': timezone.now(),
            'description': request.data.get('description'),
            'start_time': request.data.get('start_time'),
            'end_time': request.data.get('end_time'),
            'has_attachment': request.data.get('has_attachment'),
        }
        event_serializer = EventSerializer(data=data)
        if event_serializer.is_valid():
            event_serializer.save()
            return Response(event_serializer.data, status=status.HTTP_201_CREATED)
        return Response(event_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update_event_by_id(self, request, *args, **kwargs):
        event_id = request.data.get('event_id')

        try:
            event = Event.objects.get(event_id=event_id)
        except Event.DoesNotExist:
            return Response({'message': 'No event found with the given id'}, status=status.HTTP_404_NOT_FOUND)

        data = {
            'club': request.data.get('club'),
            'content': request.data.get('content'),
            'created_at': timezone.now(),
            'description': request.data.get('description'),
            'start_time': request.data.get('start_time'),
            'end_time': request.data.get('end_time'),
            'has_attachment': request.data.get('has_attachment'),
        }

        event_serializer = EventSerializer(instance=event, data=data)
        if event_serializer.is_valid():
            event_serializer.save()
            return Response(event_serializer.data, status=status.HTTP_200_OK)
        return Response(event_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({'message': 'Event deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def generate_mock_events(self, request, *args, **kwargs):
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

    @action(detail=False, methods=['get'], url_path='calendar/')
    def get_event_by_organization(self, request):
        org_name = request.query_params.get('org_name')
        if not org_name:
            return Response({'message': 'Organization name not provided in the query'},
                            status=status.HTTP_400_BAD_REQUEST)

        events = Event.objects.filter(club=org_name)
        if not events:
            return Response({'message': 'No events found for the organization'}, status=status.HTTP_404_NOT_FOUND)

        serializer = EventSerializer(events, many=True).data

        events = []
        for i in serializer:
            try: url = BlobStorage.objects.filter(username=
                                             CustomUser.objects.get(
                                                 username=Organization.objects.get(club_name=i['club']).username.username.username),
                                             is_profile_picture=True).values_list('url',
                                                                                  flat=True).first()
            except:
                url = None
            i['url'] = url
            events.append(i)

        return Response(events, status=status.HTTP_200_OK)

    def get_event_by_id(self, request, *args, **kwargs):
        event_id = request.data.get('event_id')
        event = Event.objects.filter(event_id=event_id)
        if not event:
            return Response({'message': 'No event found with the given id'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'event': event}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='calendar/upcoming/')
    def get_upcoming_events(self, request):
        now = datetime.now()
        events = Event.objects.filter(start_time__month=now.month)
        if not events:
            return Response({'message': 'No events found for the month'}, status=status.HTTP_404_NOT_FOUND)

        serialized_events = EventSerializer(events, many=True).data
        return Response({'events': serialized_events}, status=status.HTTP_200_OK)
