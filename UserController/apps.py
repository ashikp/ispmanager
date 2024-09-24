from django.apps import AppConfig
from django.db.models.signals import post_migrate

def seed_roles(sender, **kwargs):
    from django.core.management import call_command
    call_command('seed_roles')

class UserControllerConfig(AppConfig):
    name = 'UserController'

    def ready(self):
        post_migrate.connect(seed_roles, sender=self)