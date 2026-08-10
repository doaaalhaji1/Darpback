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