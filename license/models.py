from django.db import models

# Create your models here.
class Keys(models.Model):
    name = models.CharField(max_length=100)
    license_key = models.CharField(max_length=100)
    license_type = models.CharField(max_length=100)
    license_status = models.CharField(max_length=100)
    license_expiry = models.CharField(max_length=100)
    connection_limit = models.IntegerField()
    payment_system = models.CharField(max_length=100)
    mac_address = models.CharField(max_length=1000)
    ip_address = models.CharField(max_length=1000)

    def __str__(self):
        return self.name