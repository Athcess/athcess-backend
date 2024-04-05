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
        likes = [random.randint(1, 100) for _ in range(random.randint(0, 10))]
        event = Event(club= club,content=content, created_at=time_post, like=likes)
        events.append(event)
    return events
