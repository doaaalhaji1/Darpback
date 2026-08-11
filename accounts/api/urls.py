from django.urls import path
from .views import (
    AdminUserListCreateAPIView,
    AdminUserDetailAPIView
)

from .views import (
    ProfileAPIView,
    PassengerProfileAPIView,
    RegisterAPIView,
    AdminUserListAPIView,
    AdminUserDetailAPIView
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

    path(
    'admin/users/',
    AdminUserListCreateAPIView.as_view(),
    name='admin-users'
    ),
    path(
        'admin/users/<int:pk>/',
        AdminUserDetailAPIView.as_view(),
        name='admin-user-detail'
    ),

    path(
        'admin/users/',
        AdminUserListAPIView.as_view(),
        name='admin-user-list'
    ),
    path(
        'admin/users/<int:pk>/',
        AdminUserDetailAPIView.as_view(),
        name='admin-user-detail'
    ),

]