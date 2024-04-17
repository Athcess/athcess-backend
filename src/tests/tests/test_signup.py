from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.reverse import reverse
from rest_framework.test import APIClient
from django.utils import timezone
from users.models.custom_user import CustomUser, Athlete, Scout, Admin_organization, Organization
from rest_framework import serializers
from django.core.management import call_command


class SignupTest(TestCase):
    fixtures = [
        'auth_user.json',
        'user.json',
        'athlete.json',
    ]

    data = {
        "username": "cr7",
        "first_name": "cristiano",
        "last_name":"ronaldo",
        "role": "athlete",
        "password": "123456",
        "confirm_password": "123456",
        "age": 21,
        "position": "ST",
        "birth_date": "2002-10-12T00:00:00Z",
        "hometown": "Bangkok",
        "education": "B. Eng",
        "description": "hi"
    }

    def setUp(self):
        # destroy all data
        call_command('flush', '--noinput')
        # load fixtures
        call_command('loaddata', *self.fixtures)
        # Create a client
        self.client = APIClient()
        self.user = User.objects.get(pk=1) # in fixture

    # teardown function
    def tearDown(self):
        pass

    def test_signup(self):
        url = reverse('signup')
        response = self.client.post(url, self.data, format='json')
        self.assertEqual(response.status_code, 201)
