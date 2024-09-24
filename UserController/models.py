from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser


class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class UserRole(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.ForeignKey('Role', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} - {self.role.name}'

class CustomUser(AbstractUser):
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)

    def save(self, *args, **kwargs):
        # If the role is not provided, default to the role with id=2 (Customer)
        if self.role is None:
            try:
                self.role = Role.objects.get(id=3)  # Assuming role with id=2 is "Customer"
            except Role.DoesNotExist:
                raise ValueError("Role with id=3 does not exist. Please create the 'Customer' role.")
        
        # Call the original save method
        super().save(*args, **kwargs)

    def __str__(self):
        if self.role:
            return f'{self.username} - {self.role.name}'
        else:
            return f'{self.username} - No role assigned'
