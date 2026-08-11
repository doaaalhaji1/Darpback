from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import (
    User,
    PassengerProfile
)

from rest_framework import status

from rest_framework import generics
from .serializers import (
    RegisterSerializer,
    AdminUserSerializer
)
from accounts.permissions import IsSystemAdmin


class ProfileAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        gender = None

        if hasattr(
            request.user,
            'passengerprofile'
        ):
            gender = request.user.passengerprofile.gender

        return Response({

            "id": request.user.id,

            "username": request.user.username,

            "user_type": request.user.user_type,

            "gender": gender

        })
    

class PassengerProfileAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        if request.user.user_type != 'PASSENGER':

            return Response(
                {
                    "detail":
                    "Only passengers can set gender."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        gender = request.data.get('gender')

        if gender not in ['MALE', 'FEMALE']:

            return Response(
                {
                    "detail":
                    "Gender must be MALE or FEMALE."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        PassengerProfile.objects.update_or_create(
            user=request.user,
            defaults={
                'gender': gender
            }
        )

        return Response({
            "message":
            "Passenger profile updated successfully."
        })
    
class RegisterAPIView(generics.CreateAPIView):

    serializer_class = RegisterSerializer

class AdminUserListCreateAPIView(generics.ListCreateAPIView):

    serializer_class = AdminUserSerializer

    permission_classes = [
        IsAuthenticated,
        IsSystemAdmin
    ]

    def get_queryset(self):
        return User.objects.all().order_by('id')

class AdminUserDetailAPIView(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = AdminUserSerializer

    permission_classes = [
        IsAuthenticated,
        IsSystemAdmin
    ]
    queryset = User.objects.all()