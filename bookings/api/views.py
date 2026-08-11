from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from bookings.models import Booking
from .serializers import BookingSerializer

from rest_framework.permissions import IsAuthenticated

from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView
)

from accounts.permissions import IsSystemAdmin

from invoices.models import Invoice

import qrcode

from io import BytesIO

from django.core.files import File

from django.db import transaction

from trips.models import Trip

from bookings.models import Booking

from .serializers import (
    GroupBookingSerializer
)

from accounts.models import User
from .serializers import EmployeeBookingSerializer
from accounts.permissions import IsCompanyManager


class BookingCreateAPIView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def post(self, request):

        serializer = BookingSerializer(
            data=request.data,
            context={
                'request': request
                }
                )

        if serializer.is_valid():

            booking = serializer.save(
                user=request.user
            )
        
            qr = qrcode.make(
                f"Booking:{booking.id}"
                f"|Trip:{booking.trip.id}"
                f"|Seat:{booking.seat_number}"
                
                )
            buffer = BytesIO()
            
            qr.save(buffer)
            
            booking.qr_code.save(
                f'booking_{booking.id}.png',
                File(buffer),
                save=True
                
                )

            Invoice.objects.create(
            booking=booking,
            amount=booking.trip.price,
            payment_type='ONLINE'
            
            )

            trip = booking.trip

            trip.available_seats -= 1

            trip.save()

            return Response(
                BookingSerializer(booking).data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    
class BookingListAPIView(ListAPIView):

    serializer_class = BookingSerializer

    permission_classes = [
        IsAuthenticated,
        IsSystemAdmin
    ]
    def get_queryset(self):

        return Booking.objects.select_related(
            'user',
            'trip',
            'trip__company'
        ).all().order_by('-booking_date')

class BookingDetailAPIView(RetrieveAPIView):

    queryset = Booking.objects.all()

    serializer_class = BookingSerializer

    permission_classes = [
        IsAuthenticated,
        IsSystemAdmin
    ]
class BookingCancelAPIView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def post(self, request, pk):

        try:

            booking = Booking.objects.get(pk=pk)

        except Booking.DoesNotExist:

            return Response(
                {"error": "Booking Not Found"},
                status=status.HTTP_404_NOT_FOUND
            )

        if (
            request.user.user_type != 'SYSTEM_ADMIN'
            and booking.user != request.user
        ):

            return Response(
                {
                    "error": "You are not allowed to cancel this booking"
                },
                status=status.HTTP_403_FORBIDDEN
            )

        if booking.booking_status == 'CANCELLED':

            return Response(
                {
                    "error": "Booking Cancelled Already"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        booking.booking_status = 'CANCELLED'
        booking.save()

        trip = booking.trip

        trip.available_seats += 1
        trip.save()

        return Response(
            {
                "message": "Cancelled Successfully"
            },
            status=status.HTTP_200_OK
        )
    
      
class MyBookingsAPIView(ListAPIView):

    serializer_class = BookingSerializer

    permission_classes = [
        IsAuthenticated
    ]

    def get_queryset(self):

        return Booking.objects.filter(
            user=self.request.user
        )    
    

class GroupBookingAPIView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    @transaction.atomic
    def post(self, request):

        serializer = GroupBookingSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        trip_id = serializer.validated_data[
            'trip'
        ]

        seat_numbers = serializer.validated_data[
            'seat_numbers'
        ]

        trip = Trip.objects.get(
            id=trip_id
        )

        vehicle_capacity = trip.seats.count() or trip.available_seats

        created_bookings = []

        for seat in seat_numbers:

            if seat > vehicle_capacity:

                return Response({

                    'error':
                    f'Seat {seat} '
                    f'does not exist.'

                }, status=400)

            exists = Booking.objects.filter(

                trip=trip,

                seat_number=seat

            ).exists()

            if exists:

                return Response({

                    'error':
                    f'Seat {seat} '
                    f'is already booked.'

                }, status=400)

        for seat in seat_numbers:

            booking = Booking.objects.create(

                user=request.user,

                trip=trip,

                seat_number=seat,

                booking_status='PENDING'

            )

            created_bookings.append({

                'booking_id':
                booking.id,

                'seat_number':
                booking.seat_number

            })

        return Response({

            'message':
            'Group booking created successfully',

            'bookings':
            created_bookings

        })
    

class EmployeeBookingAPIView(APIView):

    permission_classes = [IsAuthenticated]
    def post(self, request):
        if request.user.user_type != 'BOOKING_EMPLOYEE':
            return Response(
            {
                "error": "Only booking employees can use this endpoint."
            },
            status=403
        )
        serializer = EmployeeBookingSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        phone = serializer.validated_data[
            'passenger_phone'
            ]

        try:
            passenger = User.objects.get(
                phone=phone,
                user_type='PASSENGER'
            )

        except User.DoesNotExist:
            return Response(
            {
                "error": "Passenger not found."
            },
            status=404
            )
        trip = serializer.validated_data[
            'trip'
        ]

        if trip.company != request.user.company:

          return Response(
            {
                "error":
                "You can only book trips for your company."
            },
            status=403
            )

        seat_number = serializer.validated_data[
            'seat_number'
        ]

        booking_serializer = BookingSerializer(
            data={
                "trip": trip.id,
                
                "seat_number": seat_number

            },

            context={
                "request": request,
                
                "booking_user": passenger
            }
        )

        booking_serializer.is_valid(
            raise_exception=True
        )

        booking = booking_serializer.save(
            user=passenger
        )

        booking.created_by = request.user

        booking.save()

        qr = qrcode.make(
            f"Booking:{booking.id}"
            f"|Trip:{booking.trip.id}"
            f"|Seat:{booking.seat_number}"
        )

        buffer = BytesIO()

        qr.save(buffer)

        booking.qr_code.save(
            f'booking_{booking.id}.png',
            File(buffer),
            save=True
        )

        Invoice.objects.create(
            booking=booking,

            amount=booking.trip.price,
    
            payment_type='ONLINE'
        )

        trip.available_seats -= 1
    
        trip.save()

        return Response({
            "booking_id": booking.id,

            "passenger": passenger.username,
    
            "seat_number": seat_number,
    
            "trip": trip.id,
    
            "created_by": request.user.username

        }, status=201)


class TripSeatsAPIView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def get(self, request, trip_id):

        try:

            trip = Trip.objects.get(
                id=trip_id
            )

        except Trip.DoesNotExist:

            return Response(
                {
                    "error": "Trip not found"
                },
                status=404
            )

        booked_seats = list(

            Booking.objects.filter(

                trip=trip,

                booking_status='PENDING'

            ).values_list(

                'seat_number',

                flat=True

            )

        )

      # بعد:
        capacity = trip.seats.count() or trip.available_seats

        available_seats = []

        for seat in range(1, capacity + 1):
            if seat not in booked_seats:
                available_seats.append(seat)

        return Response({
            "trip_id": trip.id,
            "vehicle_type": "BUS",
            "capacity": capacity,
            "booked_seats": booked_seats,
            "available_seats": available_seats
        })
    

class SeatLayoutAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, trip_id):

        try:

            trip = Trip.objects.get(id=trip_id)

        except Trip.DoesNotExist:

            return Response(
                {"error": "Trip not found"},
                status=404
            )

        booked_seats = list(

            Booking.objects.filter(
                trip=trip,
                booking_status='PENDING'
            ).values_list(
                'seat_number',
                flat=True
            )
        )

# بعد:
        vehicle_type = 'BUS'
        capacity = trip.seats.count() or trip.available_seats

        layout = []

        if vehicle_type == 'BUS':

            seat = 1

            while seat <= trip.vehicle.seats_count:

                row = []

                for _ in range(4):

                    if seat <= trip.vehicle.seats_count:

                        row.append({

                            "seat_number": seat,

                            "booked":
                            seat in booked_seats

                        })

                        seat += 1

                layout.append(row)

        elif vehicle_type == 'MICROBUS':

            seat = 1

            while seat <= trip.vehicle.seats_count:

                row = []

                for _ in range(3):

                    if seat <= trip.vehicle.seats_count:

                        row.append({

                            "seat_number": seat,

                            "booked":
                            seat in booked_seats

                        })

                        seat += 1

                layout.append(row)

        elif vehicle_type == 'VAN':

            seat = 1

            while seat <= trip.vehicle.seats_count:

                row = []

                for _ in range(3):

                    if seat <= trip.vehicle.seats_count:

                        row.append({

                            "seat_number": seat,

                            "booked":
                            seat in booked_seats

                        })

                        seat += 1

                layout.append(row)

        return Response({

            "trip_id": trip.id,

            "vehicle_type": vehicle_type,

            "layout": layout

        })


class MyCompanyBookingsAPIView(ListAPIView):

    serializer_class = BookingSerializer

    permission_classes = [
        IsAuthenticated,
        IsCompanyManager
    ]

    def get_queryset(self):

        company = self.request.user.managed_company

        return Booking.objects.filter(
            trip__company=company
        ).select_related(
            'user',
            'trip'
        )    