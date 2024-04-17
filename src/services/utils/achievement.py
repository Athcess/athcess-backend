import random
from faker import Faker
from django.utils import timezone
from services.models.achievement import Achievement

fake = Faker()

def mock_achievement_data(num_achievements=10):
    achievements = []
    for _ in range(num_achievements):
        achievement = fake.text(max_nb_chars=250)
        create_at = fake.date_time_between(start_date="-1y", end_date="now")
        date = fake.date_time_between(start_date="-1y", end_date="now")
        username = fake.random_element(elements=[choice[0] for choice in CustomUser.ROLE_CHOICES])
        achievement = Achievement(
            achievement=achievement,
            create_at=create_at,
            date=date,
            username=username,
        )
        achievements.append(achievement)
    return achievements