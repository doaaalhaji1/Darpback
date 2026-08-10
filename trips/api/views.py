from django.db.models import Sum
from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError, PermissionDenied
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    CreateAPIView,
    UpdateAPIView,
    DestroyAPIView,
)

from accounts.permissions import IsAdminOrCompanyManager
from companies.models import TransportCompany
from trips.models import Trip
from bookings.models import Booking
from invoices.models import Invoice

from .serializers import TripSerializer


# ملاحظة (المسار ب): أُعيدت الفلترة حسب الشركة عبر Trip.company (FK جديد).
# أُبقيت إصلاحات رؤية A: from_city/to_city نصّيان، لا trip_status، وإصلاح
# أخطاء الإزاحة (return داخل الحلقة) في تقريرَي الإشغال وأعلى الرحلات.


def get_manager_company(user):
    """يعيد شركة المدير أو يرمي 403 واضحاً بدل 500 غامض عند عدم الربط."""
    try:
        return TransportCompany.objects.get(manager=user)
    except TransportCompany.DoesNotExist:
        raise PermissionDenied(
            "هذا المستخدم غير مربوط بأي شركة "
            "(لا توجد TransportCompany بـ manager = هذا المستخدم)."
        )


class TripListAPIView(ListAPIView):

    queryset = Trip.objects.all()
    serializer_class = TripSerializer


class TripDetailAPIView(RetrieveAPIView):

    queryset = Trip.objects.all()
    serializer_class = TripSerializer


class TripSearchAPIView(ListAPIView):

    serializer_class = TripSerializer

    def get_queryset(self):

        queryset = Trip.objects.all()

        departure = self.request.GET.get('from')
        arrival = self.request.GET.get('to')
        trip_date = self.request.GET.get('date')

        if departure:
            # رؤية A: from_city نصّي (كان departure_city__city_name__icontains)
            queryset = queryset.filter(from_city__icontains=departure)

        if arrival:
            queryset = queryset.filter(to_city__icontains=arrival)

        if trip_date:
            # رؤية A: لا trip_date؛ نفلتر على تاريخ departure_time
            queryset = queryset.filter(departure_time__date=trip_date)

        return queryset


class TripCreateAPIView(CreateAPIView):

    serializer_class = TripSerializer
    queryset = Trip.objects.all()

    permission_classes = [
        IsAuthenticated,
        IsAdminOrCompanyManager,
    ]

    def perform_create(self, serializer):
        user = self.request.user

        if user.user_type == 'COMPANY_MANAGER':
            # المدير: تُسند الرحلة لشركته تلقائياً
            company = get_manager_company(user)
            serializer.save(company=company)
        else:
            # الأدمن: تُحفظ بلا شركة (company=NULL) → تظهر له فقط
            serializer.save()


class MyCompanyTripsAPIView(ListAPIView):

    serializer_class = TripSerializer

    permission_classes = [
        IsAuthenticated,
        IsAdminOrCompanyManager,
    ]

    def get_queryset(self):
        if self.request.user.user_type == 'SYSTEM_ADMIN':
            return Trip.objects.all()

        company = get_manager_company(self.request.user)
        return Trip.objects.filter(company=company)


class CompanyDashboardAPIView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsAdminOrCompanyManager,
    ]

    def get(self, request):

        if request.user.user_type == 'SYSTEM_ADMIN':
            trips = Trip.objects.all()
            total_bookings = Booking.objects.count()
            cancelled_bookings = Booking.objects.filter(
                booking_status='CANCELLED'
            ).count()
        else:
            company = get_manager_company(request.user)
            trips = Trip.objects.filter(company=company)
            total_bookings = Booking.objects.filter(
                trip__company=company
            ).count()
            cancelled_bookings = Booking.objects.filter(
                trip__company=company,
                booking_status='CANCELLED'
            ).count()

        total_trips = trips.count()

        # رؤية A: لا trip_status. "النشطة" = الرحلات القادمة.
        active_trips = trips.filter(
            departure_time__gte=timezone.now()
        ).count()

        total_available_seats = sum(
            trip.available_seats for trip in trips
        )

        return Response({
            'total_trips': total_trips,
            'active_trips': active_trips,
            'total_bookings': total_bookings,
            'cancelled_bookings': cancelled_bookings,
            'total_available_seats': total_available_seats,
        })


class RevenueDashboardAPIView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsAdminOrCompanyManager,
    ]

    def get(self, request):

        if request.user.user_type == 'SYSTEM_ADMIN':
            paid_invoices = Invoice.objects.filter(payment_status='PAID')
            pending_invoices = Invoice.objects.filter(payment_status='PENDING')
        else:
            company = get_manager_company(request.user)
            paid_invoices = Invoice.objects.filter(
                booking__trip__company=company,
                payment_status='PAID'
            )
            pending_invoices = Invoice.objects.filter(
                booking__trip__company=company,
                payment_status='PENDING'
            )

        total_revenue = paid_invoices.aggregate(
            total=Sum('amount')
        )['total'] or 0

        return Response({
            'total_revenue': total_revenue,
            'paid_invoices': paid_invoices.count(),
            'pending_invoices': pending_invoices.count(),
            'total_bookings': paid_invoices.count(),
        })


class OccupancyReportAPIView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsAdminOrCompanyManager,
    ]

    def get(self, request):

        if request.user.user_type == 'SYSTEM_ADMIN':
            trips = Trip.objects.all()
        else:
            company = get_manager_company(request.user)
            trips = Trip.objects.filter(company=company)

        data = []

        for trip in trips:

            booked_seats = Booking.objects.filter(
                trip=trip
            ).exclude(
                booking_status='CANCELLED'
            ).count()

            total_capacity = booked_seats + trip.available_seats

            occupancy = 0
            if total_capacity > 0:
                occupancy = round(
                    (booked_seats / total_capacity) * 100,
                    2
                )

            data.append({
                "trip_id": trip.id,
                # رؤية A: from_city / to_city نصّيان
                "route": f"{trip.from_city} → {trip.to_city}",
                "total_seats": total_capacity,
                "booked_seats": booked_seats,
                "available_seats": trip.available_seats,
                "occupancy_percentage": occupancy,
            })

        # إصلاح إزاحة: return خارج الحلقة (كان يعيد بعد أول رحلة فقط).
        return Response(data)


class TripUpdateAPIView(UpdateAPIView):

    serializer_class = TripSerializer

    permission_classes = [
        IsAuthenticated,
        IsAdminOrCompanyManager,
    ]

    def get_queryset(self):
        if self.request.user.user_type == 'SYSTEM_ADMIN':
            return Trip.objects.all()

        company = get_manager_company(self.request.user)
        return Trip.objects.filter(company=company)


class TripDeleteAPIView(DestroyAPIView):

    permission_classes = [
        IsAuthenticated,
        IsAdminOrCompanyManager,
    ]

    def get_queryset(self):
        if self.request.user.user_type == 'SYSTEM_ADMIN':
            return Trip.objects.all()

        company = get_manager_company(self.request.user)
        return Trip.objects.filter(company=company)

    def perform_destroy(self, instance):
        # نستخدم موديل الحجز صراحةً بدل instance.booking_set
        # (يوجد علاقتان عكسيتان booking/bookings على Trip).
        active_bookings = Booking.objects.filter(
            trip=instance,
            booking_status='CONFIRMED'
        ).exists()

        if active_bookings:
            raise ValidationError(
                "لا يمكن حذف الرحلة لأنها تحتوي على حجوزات"
            )

        instance.delete()


class TopTripsReportAPIView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsAdminOrCompanyManager,
    ]

    def get(self, request):

        if request.user.user_type == 'SYSTEM_ADMIN':
            trips = Trip.objects.all()
        else:
            company = get_manager_company(request.user)
            trips = Trip.objects.filter(company=company)

        result = []

        for trip in trips:

            bookings_count = Booking.objects.filter(
                trip=trip
            ).exclude(
                booking_status='CANCELLED'
            ).count()

            result.append({
                "trip_id": trip.id,
                "route": f"{trip.from_city} → {trip.to_city}",
                "bookings": bookings_count,
            })

        # إصلاح إزاحة: الفرز و return خارج الحلقة.
        result = sorted(
            result,
            key=lambda x: x['bookings'],
            reverse=True
        )

        return Response(result)


class PaymentsReportAPIView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsAdminOrCompanyManager,
    ]

    def get(self, request):

        if request.user.user_type == 'SYSTEM_ADMIN':
            invoices = Invoice.objects.all()
        else:
            company = get_manager_company(request.user)
            invoices = Invoice.objects.filter(
                booking__trip__company=company
            )

        paid = invoices.filter(payment_status='PAID')
        pending = invoices.filter(payment_status='PENDING')

        total_amount = paid.aggregate(total=Sum('amount'))['total'] or 0

        return Response({
            "paid_invoices": paid.count(),
            "pending_invoices": pending.count(),
            "total_amount": total_amount,
        })