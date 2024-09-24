from django.core.management.base import BaseCommand
from UserController.models import Role

class Command(BaseCommand):
    help = 'Seed database with default roles'

    def handle(self, *args, **kwargs):
        roles = ['Admin', 'Manager', 'Customer', 'Reseller']

        for role in roles:
            role_obj, created = Role.objects.get_or_create(name=role)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Role "{role}" created'))
            else:
                self.stdout.write(self.style.WARNING(f'Role "{role}" already exists'))

        self.stdout.write(self.style.SUCCESS('Seeding roles completed successfully'))
