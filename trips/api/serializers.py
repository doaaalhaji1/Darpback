from rest_framework import serializers

from trips.models import Trip


class TripSerializer(serializers.ModelSerializer):

    departure_city_name = serializers.CharField(
        source='departure_city.city_name',
        read_only=True
    )

    arrival_city_name = serializers.CharField(
        source='arrival_city.city_name',
        read_only=True
    )

    company_name = serializers.CharField(
        source='company.company_name',
        read_only=True
    )

    class Meta:

        model = Trip

        fields = '__all__'

        extra_kwargs = {

            'company': {
                'required': False
            }

        }