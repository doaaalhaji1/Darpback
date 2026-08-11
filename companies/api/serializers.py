from rest_framework import serializers

from companies.models import (
    City,
    TransportCompany,
    Vehicle
)

from accounts.models import User


class CitySerializer(serializers.ModelSerializer):

    class Meta:

        model = City

        fields = '__all__'


class CompanySerializer(serializers.ModelSerializer):

    class Meta:

        model = TransportCompany

        fields = '__all__'


# ==========================================
# Vehicle
# ==========================================

class VehicleSerializer(serializers.ModelSerializer):

    class Meta:

        model = Vehicle

        fields = [
            'id',
            'vehicle_type',
            'seats_count'
        ]


# ==========================================
# Booking Employee
# ==========================================

class BookingEmployeeSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only=True,
        required=False
    )

    class Meta:

        model = User

        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'phone',
            'password',
            'is_active'
        ]

        read_only_fields = [
            'id'
        ]

    def create(self, validated_data):

        password = validated_data.pop(
            'password',
            None
        )

        user = User.objects.create_user(
            password=password,
            user_type='BOOKING_EMPLOYEE',
            **validated_data
        )

        return user

    def update(self, instance, validated_data):

        password = validated_data.pop(
            'password',
            None
        )

        for attr, value in validated_data.items():

            setattr(
                instance,
                attr,
                value
            )

        if password:

            instance.set_password(
                password
            )

        instance.user_type = 'BOOKING_EMPLOYEE'

        instance.save()

        return instance