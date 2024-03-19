from django.core.management.base import BaseCommand
from users.models.custom_user import CustomGroup, CustomPermission

class Command(BaseCommand):
    help = 'Mock data for custom groups and permissions'

    def handle(self, *args, **options):
        # Create custom groups
        group_data = [
            {'name': 'athlete'},
            {'name': 'scout'},
            {'name': 'organization'},
            {'name': 'admin'},
        ]
        for data in group_data:
            CustomGroup.objects.get_or_create(**data)
            self.stdout.write(self.style.SUCCESS(f'Created custom group: {data["name"]}'))

        # Create custom permissions
        permission_data = [
            {'name': 'athlete_permission'},
            {'name': 'scout_permission'},
            {'name': 'organization_permission'},
            {'name': 'admin_permission'},
        ]
        for data in permission_data:
            CustomPermission.objects.get_or_create(**data)
            self.stdout.write(self.style.SUCCESS(f'Created custom permission: {data["name"]}'))
