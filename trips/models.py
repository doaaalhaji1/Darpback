from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver


class Trip(models.Model):
    from_city = models.CharField(max_length=100)
    to_city = models.CharField(max_length=100)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available_seats = models.IntegerField(default=28)
    bus_number = models.CharField(max_length=50, blank=True, null=True)
    # المسار ب: ربط الرحلة بشركة (مرجع نصّي لتفادي دوران الاستيراد).
    # null=True ضروري: رحلات الأدمن تُحفظ بلا شركة، والرحلات القديمة قبل التعبئة.
    company = models.ForeignKey(
        'companies.TransportCompany',
        on_delete=models.SET_NULL,
        related_name='trips',
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.from_city} -> {self.to_city} ({self.departure_time.strftime('%Y-%m-%d %H:%M')})"


# موديل المقاعد لكل رحلة (يُستخدم كمصدر السعة الحقيقي)
class Seat(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='seats')
    seat_number = models.IntegerField()
    is_booked = models.BooleanField(default=False)

    class Meta:
        unique_together = ('trip', 'seat_number')

    def __str__(self):
        return f"رحلة {self.trip.id} - مقعد {self.seat_number} ({'محجوز' if self.is_booked else 'متاح'})"


# موديل حجز داخلي (غير مستخدم من الـ API — الـ API يستخدم bookings.models.Booking)
class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings')
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='bookings')
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE, related_name='bookings')
    passenger_name = models.CharField(max_length=100)
    passenger_phone = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"حجز {self.passenger_name} - مقعد {self.seat.seat_number}"


# إشارة لتوليد المقاعد تلقائياً عند إنشاء رحلة جديدة
@receiver(post_save, sender=Trip)
def create_seats_for_trip(sender, instance, created, **kwargs):
    if created:
        seats = [
            Seat(trip=instance, seat_number=i)
            for i in range(1, instance.available_seats + 1)
        ]
        Seat.objects.bulk_create(seats)