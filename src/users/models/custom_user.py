from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('athlete', 'Athlete'),
        ('scout', 'Scout'),
        ('organization', 'Organization'),
    )

    #id = models.AutoField(unique=True, default=None)
    username = models.CharField(max_length=50, primary_key=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    password = models.CharField(max_length=128, blank=True)

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        related_name='custom_user_groups'  # Unique related_name
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        related_name='custom_user_permissions'  # Unique related_name
    )

    class Meta:
        db_table = "user"
        app_label = 'users'

    def __str__(self):
        return f"User: {self.username}"


class Athlete(models.Model):
    POSITION_CHOICES = (
        ('GK', 'Goalkeeper'),
        ('CB', 'Center Back'),
        ('LB', 'Left Back'),
        ('RB', 'Right Back'),
        ('CM', 'Center Midfield'),
        ('LM', 'Left Midfield'),
        ('RM', 'Right Midfield'),
        ('CAM', 'Center Attacking Midfield'),
        ('LW', 'Left Wing'),
        ('RW', 'Right Wing'),
        ('ST', 'Striker'),
    )
    username = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    age = models.IntegerField()
    position = models.CharField(choices=POSITION_CHOICES, max_length=20, blank=True, null=True)
    birth_date = models.DateTimeField()
    hometown = models.CharField(max_length=100)
    education = models.CharField(max_length=100)
    description = models.TextField()
    organization = models.ForeignKey('Organization', on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        db_table = "athlete"

    def __str__(self):
        return f"Athlete: {self.username.username}"


class Scout(models.Model):
    username = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    birth_date = models.DateTimeField()
    hometown = models.CharField(max_length=100)
    age = models.IntegerField()
    organization = models.ForeignKey('Organization', on_delete=models.SET_NULL, blank=True, null=True)
    description = models.TextField()

    class Meta:
        db_table = "scout"

    def __str__(self):
        return f"Scout: {self.username.username}"


class Organization(models.Model):
    username = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    club_name = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = "organization"

    def __str__(self):
        return f"Organization: {self.username.username}"


