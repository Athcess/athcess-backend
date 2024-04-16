from faker import Faker
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta
from users.models.custom_user import CustomUser, Athlete, Scout, Admin_organization, Organization

fake = Faker()
User = get_user_model()

def mock_custom_users(num_users=10):
    users_data = []
    auth_users = []
    for _ in range(num_users):
        user_data = {
            'username': fake.user_name(),
            'password': fake.password(),
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'role': fake.random_element(elements=[choice[0] for choice in CustomUser.ROLE_CHOICES])
        }
        auth_user = {
            'username': user_data['username'],
            'password': user_data['password'],
            'first_name': user_data['first_name'],
            'last_name': user_data['last_name'],
        }
        users_data.append(user_data)
        auth_users.append(auth_user)
    return users_data, auth_users
    #auth user :
    # username firstname lastname password 

def mock_athletes(num_athletes=10):
    athletes = []
    auth_users = []
    for _ in range(num_athletes):
        athlete_user = CustomUser.objects.create(
            username=fake.user_name(),
            password=fake.password(),
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            role='athlete'  # Set the role to 'athlete'
        )
        athlete = {
            'username':athlete_user.username,
            'age':fake.random_int(min=18, max=40),
            'position':fake.random_element(elements=[choice[0] for choice in Athlete.POSITION_CHOICES]),
            'birth_date':fake.date_time_between(start_date="-30y", end_date="-18y"),
            'hometown':fake.random_element(elements=[choice[0] for choice in Athlete.HOMWTOWN_CHOICES]),
            'education':fake.random_element(elements=['Bachelor', 'Master', 'PhD']),
            'description':fake.text(max_nb_chars=200)
        }
        auth_user = {
            'username': athlete_user.username,
            'password': athlete_user.password,
            'first_name': athlete_user.first_name,
            'last_name': athlete_user.last_name,
        }
        athletes.append(athlete)
        auth_users.append(auth_user)
    return athletes, auth_users

def mock_scouts(num_scouts=5):
    scouts = []
    auth_users = []
    for _ in range(num_scouts):
        scout_user = CustomUser.objects.create(
            username=fake.user_name(),
            password=fake.password(),
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            role='scout'  # Set the role to 'scout'
        )
        scout = {
            'username':scout_user,
            'tier':fake.boolean(),
            'birth_date':fake.date_time_between(start_date="-50y", end_date="-30y"),
            'hometown':fake.random_element(elements=[choice[0] for choice in Scout.HOMWTOWN_CHOICES]),
            'age':fake.random_int(min=30, max=60),
            'description':fake.text(max_nb_chars=200)
        }
        auth_user = {
            'username': scout_user.username,
            'password': scout_user.password,
            'first_name': scout_user.first_name,
            'last_name': scout_user.last_name,
        }
        scouts.append(scout)
        auth_users.append(auth_user)
    return scouts, auth_users

def mock_admins(num_admins=2):
    admins = []
    auth_users = []
    for _ in range(num_admins):
        admin = Admin_organization.objects.create(
            username=fake.user_name(),
            password=fake.password(),
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            role='admin',  # Set the role to 'admin'
            description=fake.text(max_nb_chars=200)
        )
        auth_user = {
            'username': admin.username,
            'password': admin.password,
            'first_name': admin.first_name,
            'last_name': admin.last_name,
        }
        admins.append(admin)
        auth_users.append(auth_user)
    return admins, auth_users
def mock_organizations(num_orgs=5):
    orgs = []
    for _ in range(num_orgs):
        org_data = {
            'admin': fake.random_element(elements=Admin_organization.objects.all()).id,
            'club_name': fake.company()
        }
        orgs.append(org_data)
    return orgs