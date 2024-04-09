from faker import Faker
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta

fake = Faker()
User = get_user_model()

def mock_custom_users(num_users=10):
    users = []
    for _ in range(num_users):
        user = User.objects.create_user(
            username=fake.user_name(),
            password=fake.password(),
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            role=fake.random_element(elements=[choice[0] for choice in CustomUser.ROLE_CHOICES])
        )
        users.append(user)
    return users

def mock_athletes(num_athletes=10):
    athletes = []
    for _ in range(num_athletes):
        athlete = Athlete.objects.create(
            username=fake.random_element(elements=User.objects.filter(role='athlete')),
            age=fake.random_int(min=18, max=40),
            position=fake.random_element(elements=[choice[0] for choice in Athlete.POSITION_CHOICES]),
            birth_date=fake.date_time_between(start_date="-30y", end_date="-18y"),
            hometown=fake.random_element(elements=[choice[0] for choice in Athlete.HOMWTOWN_CHOICES]),
            education=fake.random_element(elements=['Bachelor', 'Master', 'PhD']),
            description=fake.text(max_nb_chars=200)
        )
        athletes.append(athlete)
    return athletes

def mock_scouts(num_scouts=5):
    scouts = []
    for _ in range(num_scouts):
        scout = Scout.objects.create(
            username=fake.random_element(elements=User.objects.filter(role='scout')),
            tier=fake.boolean(),
            birth_date=fake.date_time_between(start_date="-50y", end_date="-30y"),
            hometown=fake.random_element(elements=[choice[0] for choice in Scout.HOMWTOWN_CHOICES]),
            age=fake.random_int(min=30, max=60),
            description=fake.text(max_nb_chars=200)
        )
        scouts.append(scout)
    return scouts

def mock_admins(num_admins=2):
    admins = []
    for _ in range(num_admins):
        admin = Admin.objects.create(
            username=fake.random_element(elements=User.objects.filter(role='admin')),
            description=fake.text(max_nb_chars=200)
        )
        admins.append(admin)
    return admins

def mock_organizations(num_orgs=5):
    orgs = []
    for _ in range(num_orgs):
        org = Organization.objects.create(
            admin=fake.random_element(elements=Admin.objects.all()),
            club_name=fake.company()
        )
        orgs.append(org)
    return orgs