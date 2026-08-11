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



class AdminCompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = TransportCompany

        fields = [
            'id',
            'company_name',
            'phone',
            'description',
            'manager'
        ]

    def validate_manager(self, manager):

        if manager.user_type != 'COMPANY_MANAGER':

            raise serializers.ValidationError(
                "Selected manager must be a COMPANY_MANAGER."
            )

        return manager

    def create(self, validated_data):

        manager = validated_data['manager']

        company = TransportCompany.objects.create(
            **validated_data
        )

        manager.company = company
        manager.save(
            update_fields=['company']
        )

        return company

    def update(self, instance, validated_data):

        old_manager = instance.manager

        manager = validated_data.get(
            'manager',
            old_manager
        )

        if manager.user_type != 'COMPANY_MANAGER':

            raise serializers.ValidationError(
                "Selected manager must be a COMPANY_MANAGER."
            )

        instance.company_name = validated_data.get(
            'company_name',
            instance.company_name
        )

        instance.phone = validated_data.get(
            'phone',
            instance.phone
        )

        instance.description = validated_data.get(
            'description',
            instance.description
        )

        instance.manager = manager

        instance.save()

        manager.company = instance
        manager.save(
            update_fields=['company']
        )

        if old_manager != manager:

            old_manager.company = None
            old_manager.save(
                update_fields=['company']
            )

        return instance


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

class AdminVehicleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vehicle
        fields = [
            'id',
            'company',
            'vehicle_type',
            'seats_count'
        ]

    def validate_company(self, company):

        if not TransportCompany.objects.filter(
            id=company.id
        ).exists():

            raise serializers.ValidationError(
                "Selected company does not exist."
            )

        return company

    def validate_seats_count(self, seats_count):

        if seats_count <= 0:

            raise serializers.ValidationError(
                "Seats count must be greater than zero."
            )

        return seats_count    