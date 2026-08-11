from django.urls import path

from .views import (
    CompanyListAPIView,
    CityListAPIView,
    MyCompanyAPIView,

    MyCompanyVehicleListCreateAPIView,
    MyCompanyVehicleDetailAPIView,

    MyCompanyEmployeeListCreateAPIView,
    MyCompanyEmployeeDetailAPIView,

    AdminCompanyListCreateAPIView,
    AdminCompanyDetailAPIView,

    AdminVehicleListCreateAPIView,
    AdminVehicleDetailAPIView
)


urlpatterns = [

    # ==========================
    # Companies
    # ==========================

    path(
        'companies/',
        CompanyListAPIView.as_view(),
        name='company-list'
    ),

    path(
        'cities/',
        CityListAPIView.as_view(),
        name='city-list'
    ),

    path(
        'my-company/',
        MyCompanyAPIView.as_view(),
        name='my-company'
    ),


    # ==========================
    # Vehicles
    # ==========================

    path(
        'my-company/vehicles/',
        MyCompanyVehicleListCreateAPIView.as_view(),
        name='my-company-vehicles'
    ),

    path(
        'my-company/vehicles/<int:pk>/',
        MyCompanyVehicleDetailAPIView.as_view(),
        name='my-company-vehicle-detail'
    ),


    # ==========================
    # Booking Employees
    # ==========================

    path(
        'my-company/employees/',
        MyCompanyEmployeeListCreateAPIView.as_view(),
        name='my-company-employees'
    ),

    path(
        'my-company/employees/<int:pk>/',
        MyCompanyEmployeeDetailAPIView.as_view(),
        name='my-company-employee-detail'
    ),

    path(
        'admin/companies/',
        AdminCompanyListCreateAPIView.as_view(),
        name='admin-company-list'
    ),

    path(
        'admin/companies/<int:pk>/',
        AdminCompanyDetailAPIView.as_view(),
        name='admin-company-detail'
    ),

    path(
        'admin/vehicles/',
        AdminVehicleListCreateAPIView.as_view(),
        name='admin-vehicle-list'
    ),

    path(
        'admin/vehicles/<int:pk>/',
        AdminVehicleDetailAPIView.as_view(),
        name='admin-vehicle-detail'
    ),
]