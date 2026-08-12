from django.urls import path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
from .views import (
    BookingCreateAPIView,
    BookingListAPIView,
    BookingDetailAPIView,
    BookingCancelAPIView,
    MyBookingsAPIView,
    EmployeeBookingAPIView,
    TripSeatsAPIView,
    SeatLayoutAPIView,
    MyCompanyBookingsAPIView,
    EmployeeBookingsListAPIView
)

from .views import (
    GroupBookingAPIView
)


urlpatterns = [

    path(
        'bookings/',
        BookingListAPIView.as_view(),
        name='booking-list'
    ),

    path(
        'bookings/create/',
        BookingCreateAPIView.as_view(),
        name='booking-create'
    ),

    path(
    'my-bookings/',
    MyBookingsAPIView.as_view(),
    name='my-bookings'
    ),


    path(
        'bookings/<int:pk>/',
        BookingDetailAPIView.as_view(),
        name='booking-detail'
    ),

    
    path(
    'bookings/<int:pk>/cancel/',
    BookingCancelAPIView.as_view(),
    name='booking-cancel'
    ),

    path(

    'bookings/group-create/',

    GroupBookingAPIView.as_view(),

    name='group-booking'
    ),

    path(
    'employee/bookings/create/',
    EmployeeBookingAPIView.as_view(),
    name='employee-booking'
    ),

    path(
    'trips/<int:trip_id>/seats/',
    TripSeatsAPIView.as_view(),
    name='trip-seats'
    ),

    path(
    'trips/<int:trip_id>/layout/',
    SeatLayoutAPIView.as_view(),
    name='seat-layout'
    ),

    path(
        'my-company/bookings/',
        MyCompanyBookingsAPIView.as_view(),
        name='my-company-bookings'
    ),
    path('employee/bookings/', EmployeeBookingsListAPIView.as_view(), name='employee-bookings'),


]

