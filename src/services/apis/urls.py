from django.urls import path
from . import calendar

urlpatterns = [
    path('calendar/event/', calendar.get_event, name='get_event'),
    path('calendar/create_event/', calendar.create_event, name='create_event'),
    path('calendar/delete_event/', calendar.delete_event, name='delete_event'),
    path('calendar/update_event/', calendar.update_event, name='update_event'),
    path('calendar/generate_mock_events/', calendar.generate_mock_events, name='generate_mock_events'),
]