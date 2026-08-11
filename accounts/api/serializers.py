from rest_framework import serializers

from accounts.models import (
    User,
    PassengerProfile
)
from companies.models import TransportCompany


class RegisterSerializer(serializers.ModelSerializer):
    gender = serializers.CharField(
        write_only=True,
        required=True
    )

    password = serializers.CharField(
        write_only=True
    )

    class Meta:

        model = User

        fields = [
            'username',
    
            'first_name',
        
            'last_name',
        
            'phone',
        
            'email',
        
            'password',
        
            'gender'
            ]

    def create(self, validated_data):

        gender = validated_data.pop(
            'gender'
        )

        user = User.objects.create_user(
            username=validated_data['username'],

            first_name=validated_data['first_name'],
        
            last_name=validated_data['last_name'],
        
            phone=validated_data['phone'],
        
            email=validated_data['email'],
        
            password=validated_data['password'],
        
            user_type='PASSENGER'
            )

        PassengerProfile.objects.create(

            user=user,

            gender=gender
        )

        return user


class AdminUserSerializer(serializers.ModelSerializer):

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
            'email',
            'password',
            'user_type',
            'company',
            'is_active'
        ]

    def create(self, validated_data):

        password = validated_data.pop(
            'password',
            None
        )

        user = User.objects.create(
            **validated_data
        )

        if password:
            user.set_password(password)
            user.save()

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
            instance.set_password(password)

        instance.save()

        return instance

from companies.models import TransportCompany


class AdminUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User

        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'phone',
            'email',
            'user_type',
            'company',
            'is_active'
        ]

        read_only_fields = [
            'id'
        ]

    def validate(self, attrs):

        user_type = attrs.get(
            'user_type',
            self.instance.user_type
            if self.instance
            else None
        )

        company = attrs.get(
            'company',
            self.instance.company
            if self.instance
            else None
        )

        if user_type == 'COMPANY_MANAGER' and company is None:

            raise serializers.ValidationError({
                'company':
                'Company Manager must be assigned to a company.'
            })

        if user_type in [
            'SYSTEM_ADMIN',
            'PASSENGER'
        ] and company is not None:

            raise serializers.ValidationError({
                'company':
                'This user type should not be assigned to a company.'
            })

        return attrs