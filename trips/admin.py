from django.contrib import admin
from .models import Trip, Seat, Booking

@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ('id', 'from_city', 'to_city', 'departure_time', 'price', 'available_seats')
    list_filter = ('from_city', 'to_city', 'departure_time')
    search_fields = ('from_city', 'to_city', 'bus_number')

@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ('id', 'trip', 'seat_number', 'is_booked')
    list_filter = ('is_booked', 'trip')
    search_fields = ('trip__from_city', 'trip__to_city', 'seat_number')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'passenger_name', 'passenger_phone', 'trip', 'seat', 'created_at')
    list_filter = ('created_at', 'trip')
    search_fields = ('passenger_name', 'passenger_phone')