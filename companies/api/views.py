from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView
)
from rest_framework import generics

from rest_framework.permissions import IsAuthenticated

from companies.models import (
    City,
    TransportCompany,
    Vehicle
)

from accounts.models import User

from accounts.permissions import (
    IsAdminOrCompanyManager,
    IsCompanyManager,
    IsSystemAdmin
)

from .serializers import (
    CitySerializer,
    CompanySerializer,
    VehicleSerializer,
    BookingEmployeeSerializer,
    AdminCompanySerializer
)


# ==========================================
# Cities
# ==========================================

class CityListAPIView(ListAPIView):

    queryset = City.objects.all()

    serializer_class = CitySerializer


# ==========================================
# Companies
# ==========================================

class CompanyListAPIView(ListAPIView):

    queryset = TransportCompany.objects.all()

    serializer_class = CompanySerializer

    permission_classes = [
        IsAuthenticated
    ]


class MyCompanyAPIView(RetrieveAPIView):

    serializer_class = CompanySerializer

    permission_classes = [
        IsAuthenticated,
        IsAdminOrCompanyManager
    ]

    def get_object(self):

        return TransportCompany.objects.get(
            manager=self.request.user
        )


# ==========================================
# Company Vehicles
# ==========================================

class MyCompanyVehicleListCreateAPIView(
    ListCreateAPIView
):

    serializer_class = VehicleSerializer

    permission_classes = [
        IsAuthenticated,
        IsCompanyManager
    ]

    def get_queryset(self):

        company = self.request.user.managed_company

        return Vehicle.objects.filter(
            company=company
        )

    def perform_create(self, serializer):

        company = self.request.user.managed_company

        serializer.save(
            company=company
        )


class MyCompanyVehicleDetailAPIView(
    RetrieveUpdateDestroyAPIView
):

    serializer_class = VehicleSerializer

    permission_classes = [
        IsAuthenticated,
        IsCompanyManager
    ]

    def get_queryset(self):

        company = self.request.user.managed_company

        return Vehicle.objects.filter(
            company=company
        )


# ==========================================
# Company Booking Employees
# ==========================================

class MyCompanyEmployeeListCreateAPIView(
    ListCreateAPIView
):

    serializer_class = BookingEmployeeSerializer

    permission_classes = [
        IsAuthenticated,
        IsCompanyManager
    ]

    def get_queryset(self):

        company = self.request.user.managed_company

        return User.objects.filter(
            company=company,
            user_type='BOOKING_EMPLOYEE'
        )

    def perform_create(self, serializer):

        company = self.request.user.managed_company

        serializer.save(
            company=company
        )


class MyCompanyEmployeeDetailAPIView(
    RetrieveUpdateDestroyAPIView
):

    serializer_class = BookingEmployeeSerializer

    permission_classes = [
        IsAuthenticated,
        IsCompanyManager
    ]

    def get_queryset(self):

        company = self.request.user.managed_company

        return User.objects.filter(
            company=company,
            user_type='BOOKING_EMPLOYEE'
        )

class AdminCompanyListCreateAPIView(
    generics.ListCreateAPIView
):

    serializer_class = AdminCompanySerializer

    permission_classes = [
        IsAuthenticated,
        IsSystemAdmin
    ]

    def get_queryset(self):

        return TransportCompany.objects.all().order_by('id')

class AdminCompanyDetailAPIView(
    generics.RetrieveUpdateDestroyAPIView
):

    serializer_class = AdminCompanySerializer

    permission_classes = [
        IsAuthenticated,
        IsSystemAdmin
    ]

    queryset = TransportCompany.objects.all()