from rest_framework import serializers

from bookings.models import Booking
from trips.models import Trip
from accounts.models import PassengerProfile
from accounts.models import User


def get_adjacent_seats(
    vehicle_type,
    seat_number
):

    if vehicle_type == 'BUS':

        if seat_number % 4 == 1:
            return [seat_number + 1]

        if seat_number % 4 == 2:
            return [seat_number - 1]

        if seat_number % 4 == 3:
            return [seat_number + 1]

        if seat_number % 4 == 0:
            return [seat_number - 1]

    elif vehicle_type in [

        'MICROBUS',
        'VAN'

    ]:

        row_start = (

            ((seat_number - 1) // 3) * 3

        ) + 1

        row_seats = [

            row_start,
            row_start + 1,
            row_start + 2

        ]

        adjacent = []

        if seat_number - 1 in row_seats:
            adjacent.append(
                seat_number - 1
            )

        if seat_number + 1 in row_seats:
            adjacent.append(
                seat_number + 1
            )

        return adjacent

    return []


class BookingSerializer(serializers.ModelSerializer):

    qr_code = serializers.ImageField(
        read_only=True
    )

    class Meta:
        model = Booking

        fields = '__all__'

        extra_kwargs = {
            'user': {
                'required': False
            }
        }

    def validate(self, data):
        if self.context.get(
            'group_booking',
            False):
            return data

        trip = data['trip']
        seat_number = data['seat_number']

        if trip.available_seats <= 0:
            raise serializers.ValidationError(
                "No seats are available for this trip."
            )

        seat_exists = Booking.objects.filter(
            trip=trip,
            seat_number=seat_number
        ).exists()

        if seat_exists:
            raise serializers.ValidationError(
                "This seat is already reserved."
            )

        capacity = trip.seats.count() or trip.available_seats

        user = self.context.get(
            'booking_user',
            self.context['request'].user
        )
        if user.user_type == 'PASSENGER':
            try:
                passenger_gender = (
                    user.passengerprofile.gender
                )
            except PassengerProfile.DoesNotExist:
                raise serializers.ValidationError(
                    "Passenger gender is required."
                )
            vehicle_type = 'BUS'
            adjacent_seats = get_adjacent_seats(
                vehicle_type,
                seat_number
            )
            for adjacent_seat in adjacent_seats:
                adjacent_booking = Booking.objects.filter(
                    trip=trip,
                    seat_number=adjacent_seat
                ).first()
                if adjacent_booking:
                    try:
                        adjacent_gender = (
                            adjacent_booking.user
                            .passengerprofile
                            .gender
                        )
                        if adjacent_gender != passenger_gender:
                            raise serializers.ValidationError(
                                "Male and female passengers cannot sit together."
                            )
                    except PassengerProfile.DoesNotExist:
                        pass

        if seat_number > capacity:
            raise serializers.ValidationError(
                f"This vehicle has only {capacity} seats."
            )
        return data


class GroupBookingSerializer(
    serializers.Serializer
):

    trip = serializers.IntegerField()

    seat_numbers = serializers.ListField(

        child=serializers.IntegerField(),

        min_length=2

    )


class EmployeeBookingSerializer(serializers.Serializer):

    passenger_phone = serializers.CharField()

    trip = serializers.PrimaryKeyRelatedField(
        queryset=Trip.objects.all()
    )

    seat_number = serializers.IntegerField()