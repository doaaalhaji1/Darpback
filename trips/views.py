from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions, status
from .models import Trip , Booking, Seat
from .serializers import TripSerializer , BookingSerializer, SeatSerializer
from rest_framework.response import Response
from .permissions import IsAdminOrReadOnly


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff

class TripViewSet(viewsets.ModelViewSet):
    queryset = Trip.objects.all().order_by('-departure_time')
    serializer_class = TripSerializer
    permission_classes = [IsAdminOrReadOnly]

class BookingViewSet(viewsets.ModelViewSet):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # المستخدم يرى حجوزاته فقط، والأدمن يرى جميع الحجوزات
        if self.request.user.is_staff:
            return Booking.objects.all().order_by('-created_at')
        return Booking.objects.filter(user=self.request.user).order_by('-created_at')

    def create(self, request, *args, **kwargs):
        seat_id = request.data.get('seat')
        
        try:
            seat = Seat.objects.get(id=seat_id)
        except Seat.DoesNotExist:
            return Response({"detail": "المقعد غير موجود"}, status=status.HTTP_400_BAD_REQUEST)

        # التحقق مما إذا كان المقعد محجوزاً مسبقاً
        if seat.is_booked:
            return Response({"detail": "عذراً، هذا المقعد محجوز بالفعل!"}, status=status.HTTP_400_BAD_REQUEST)

        # إنشاء الحجز
        serializer = self.get_serializer(data=request.data)
        serializer.is_validate_ok = serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)

        # تحديث حالة المقعد إلى محجوز وتنقيص عدد المقاعد المتاحة بالرحلة
        seat.is_booked = True
        seat.save()

        trip = seat.trip
        if trip.available_seats > 0:
            trip.available_seats -= 1
            trip.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
