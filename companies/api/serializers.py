from rest_framework import serializers

from companies.models import (
    City,
    TransportCompany
)


class CitySerializer(serializers.ModelSerializer):

    class Meta:

        model = City

        fields = '__all__'


class CompanySerializer(serializers.ModelSerializer):

    class Meta:

        model = TransportCompany

        fields = '__all__'