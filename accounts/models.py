from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    USER_TYPES = (
        ('PASSENGER', 'Passenger'),
        ('BOOKING_EMPLOYEE', 'Booking Employee'),
        ('COMPANY_MANAGER', 'Company Manager'),
        ('SYSTEM_ADMIN', 'System Admin'),
    )

    phone = models.CharField(
        max_length=20,
        unique=True
    )

    user_type = models.CharField(
        max_length=30,
        choices=USER_TYPES
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    company = models.ForeignKey(
    'companies.TransportCompany',
    on_delete=models.SET_NULL,
    null=True,
    blank=True
    )

class PassengerProfile(models.Model):

    GENDER_CHOICES = (
        ('MALE', 'Male'),
        ('FEMALE', 'Female'),
    )

    user = models.OneToOneField(
        'accounts.User',
        on_delete=models.CASCADE
    )

    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES
    )

    def __str__(self):
        return self.user.username