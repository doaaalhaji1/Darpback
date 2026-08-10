from django.db import models
from bookings.models import Booking


class Invoice(models.Model):

    PAYMENT_TYPES = (
        ('CASH', 'Cash'),
        ('ONLINE', 'Online'),
    )

    PAYMENT_STATUS = (
        ('PENDING', 'Pending'),
        ('PAID', 'Paid'),
        ('FAILED', 'Failed'),
    )

    booking = models.OneToOneField(
        Booking,
        on_delete=models.CASCADE
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    payment_date = models.DateTimeField(
        null=True,
        blank=True
    )

    payment_type = models.CharField(
        max_length=20,
        choices=PAYMENT_TYPES
    )

    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS,
        default='PENDING'
    )

    def __str__(self):
        return f"Invoice #{self.id}"