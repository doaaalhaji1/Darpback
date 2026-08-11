from rest_framework import serializers

from accounts.models import (
    User,
    PassengerProfile
)


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