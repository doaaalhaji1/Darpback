from django.contrib import admin
from .models import City, TransportCompany, Vehicle


@admin.register(City)
class CityAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'city_name',
    )

    search_fields = (
        'city_name',
    )


@admin.register(TransportCompany)
class TransportCompanyAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'company_name',
        'phone',
        'manager',
    )

    search_fields = (
        'company_name',
        'phone',
    )


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'vehicle_type',
        'seats_count',
        'company',
    )

    list_filter = (
        'vehicle_type',
    )