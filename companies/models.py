from django.db import models
from django.conf import settings


class City(models.Model):

    city_name = models.CharField(
        max_length=100,
        unique=True
    )

    def __str__(self):
        return self.city_name
    
class TransportCompany(models.Model):

    company_name = models.CharField(
        max_length=150
    )

    phone = models.CharField(
        max_length=20
    )

    description = models.TextField()

    manager = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='managed_company'
    )

    def __str__(self):
        return self.company_name
    
class Vehicle(models.Model):

    VEHICLE_TYPES = (
        ('BUS', 'Bus'),
        ('MICROBUS', 'Microbus'),
        ('VAN', 'Van'),
    )

    company = models.ForeignKey(
        TransportCompany,
        on_delete=models.CASCADE,
        related_name='vehicles'
    )

    vehicle_type = models.CharField(
        max_length=20,
        choices=VEHICLE_TYPES
    )

    seats_count = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.vehicle_type} ({self.seats_count})"    