from django.db import models

from accounts.models import User
from trips.models import Trip


class Booking(models.Model):
    
    created_by = models.ForeignKey(
    'accounts.User',
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name='created_bookings'
    )

    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('CANCELLED', 'Cancelled'),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    trip = models.ForeignKey(
        Trip,
        on_delete=models.CASCADE
    )

    booking_date = models.DateTimeField(
        auto_now_add=True
    )

    seat_number = models.PositiveIntegerField()

    qr_code = models.ImageField(
    upload_to='qr_codes/',
    null=True,
    blank=True
    )

    booking_status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDING'
    )

    def __str__(self):
        return f"Booking #{self.id}"
    
    class Meta:

        constraints = [

            models.UniqueConstraint(
                fields=['trip', 'seat_number'],
                name='unique_seat_per_trip'
            )

        ]

        