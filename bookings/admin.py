from django.contrib import admin
from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'user',
        'trip',
        'seat_number',
        'booking_status',
        'booking_date',
        'created_by'
    )

    list_filter = (
        'booking_status',
    )