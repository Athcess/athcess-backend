import random
from faker import Faker
from django.utils import timezone
from services.models.event import Event

fake = Faker()

def mock_event_data(num_events=10):
    events = []
    for _ in range(num_events):
        club = fake.company()
        content = fake.text(max_nb_chars=200)
        time_post = fake.date_time_between(start_date="-1y", end_date="now")
        date_start = fake.date_between(start_date=timezone.now().date(), end_date="+1y")
        date_end = fake.date_between(start_date=date_start, end_date="+1y")
        time_start = fake.time_object()
        time_end = fake.time_object()
        likes = [random.randint(1, 100) for _ in range(random.randint(0, 10))]
        event = Event(
            club=club,
            content=content,
            created_at=time_post,
            date_start=date_start,
            date_end=date_end,
            time_start=time_start,
            time_end=time_end,
            like=likes,
        )
        events.append(event)
    return events
