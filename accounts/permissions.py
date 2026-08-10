from rest_framework.permissions import BasePermission


class IsSystemAdmin(BasePermission):

    def has_permission(self, request, view):

        return (
            request.user.is_authenticated
            and request.user.user_type == 'SYSTEM_ADMIN'
        )


class IsCompanyManager(BasePermission):

    def has_permission(self, request, view):

        return (
            request.user.is_authenticated
            and request.user.user_type == 'COMPANY_MANAGER'
        )


class IsPassenger(BasePermission):

    def has_permission(self, request, view):

        return (
            request.user.is_authenticated
            and request.user.user_type == 'PASSENGER'
        )


class IsBookingEmployee(BasePermission):

    def has_permission(self, request, view):

        return (
            request.user.is_authenticated
            and request.user.user_type == 'BOOKING_EMPLOYEE'
        )
    
class IsAdminOrCompanyManager(BasePermission):

    def has_permission(self, request, view):

        return (

            request.user.is_authenticated

            and

            request.user.user_type in [

                'SYSTEM_ADMIN',

                'COMPANY_MANAGER'

            ]

        )