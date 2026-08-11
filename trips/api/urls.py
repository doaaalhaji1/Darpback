from django.urls import path

from .views import (
    TripListAPIView,
    TripDetailAPIView,
    TripSearchAPIView,
    TripCreateAPIView,
    MyCompanyTripsAPIView,
    CompanyDashboardAPIView,
    TripUpdateAPIView,
    TripDeleteAPIView,
    RevenueDashboardAPIView,
    OccupancyReportAPIView,
    TopTripsReportAPIView,
    PaymentsReportAPIView,
    SystemDashboardAPIView,
    SystemRevenueDashboardAPIView,
    SystemOccupancyReportAPIView,
    SystemPaymentsReportAPIView,
    SystemTopTripsReportAPIView
  
)

urlpatterns = [

    
    path(
    'trips/search/',
    TripSearchAPIView.as_view(),
    name='trip-search'
    ),

    path(
        'trips/',
        TripListAPIView.as_view(),
        name='trip-list'
    ),

    path(
    'trips/create/',
    TripCreateAPIView.as_view(),
    name='trip-create'
    ),

    path(
    'my-company/trips/',
    MyCompanyTripsAPIView.as_view(),
    name='my-company-trips'
    ),

    path(
    'dashboard/',
    CompanyDashboardAPIView.as_view(),
    name='company-dashboard'
    ),

    path(
    'trips/<int:pk>/update/',
    TripUpdateAPIView.as_view(),
    name='trip-update'
    ),

    path(
    'trips/<int:pk>/delete/',
    TripDeleteAPIView.as_view(),
    name='trip-delete'
    ),

    path(
    'dashboard/revenue/',
    RevenueDashboardAPIView.as_view(),
    name='revenue-dashboard'
    ),

    path(
    'dashboard/occupancy/',
    OccupancyReportAPIView.as_view(),
    name='occupancy-report'
    ),

    path(
    'dashboard/top-trips/',
    TopTripsReportAPIView.as_view(),
    name='top-trips-report'
    ),

    
    path(
        'trips/<int:pk>/',
        TripDetailAPIView.as_view(),
        name='trip-detail'
    ),

    path(
    'dashboard/payments/',
    PaymentsReportAPIView.as_view(),
    name='payments-report'
    ),

    path(
        'admin/dashboard/',
        SystemDashboardAPIView.as_view(),
        name='system-dashboard'

    ),

    path(
        'admin/dashboard/revenue/',
        SystemRevenueDashboardAPIView.as_view(),
        name='system-revenue-dashboard'
    ),

    path(
        'admin/dashboard/occupancy/',
        SystemOccupancyReportAPIView.as_view(),
        name='system-occupancy-report'
    ),

    path(
        'admin/dashboard/payments/',
        SystemPaymentsReportAPIView.as_view(),
        name='system-payments-report'
    ),

      path(
        'admin/dashboard/top-trips/',
        SystemTopTripsReportAPIView.as_view(),
        name='system-top-trips'
    ),

]

