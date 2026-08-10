from rest_framework import serializers
from .models import Trip, Seat, Booking

class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = ['id', 'seat_number', 'is_booked']


class TripSerializer(serializers.ModelSerializer):
    seats = SeatSerializer(many=True, read_only=True) # إرجاع حالة المقاعد مع بيانات الرحلة

    class Meta:
        model = Trip
        fields = '__all__'


class BookingSerializer(serializers.ModelSerializer):
    seat_number = serializers.ReadOnlyField(source='seat.seat_number')
    from_city = serializers.ReadOnlyField(source='trip.from_city')
    to_city = serializers.ReadOnlyField(source='trip.to_city')
    departure_time = serializers.ReadOnlyField(source='trip.departure_time')

    class Meta:
        model = Booking
        fields = [
            'id', 'user', 'trip', 'seat', 'seat_number', 
            'passenger_name', 'passenger_phone', 
            'from_city', 'to_city', 'departure_time', 'created_at'
        ]
        read_only_fields = ['user']

class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = '__all__'  # تحويل جميع حقول موديل Trip تلقائياً