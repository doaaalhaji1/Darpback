from django.urls import path

from .views import (
    ProfileAPIView,
    PassengerProfileAPIView,
    RegisterAPIView
)

urlpatterns = [

    path(
    'register/',
    RegisterAPIView.as_view(),
    name='register'
    ),

    path(
        'profile/',
        ProfileAPIView.as_view(),
        name='profile'
    ),

    path(
        'passenger-profile/',
        PassengerProfileAPIView.as_view(),
        name='passenger-profile'
    ),

]