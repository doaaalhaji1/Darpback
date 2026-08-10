from django.contrib import admin
from .models import Invoice


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'booking',
        'amount',
        'payment_type',
        'payment_date',
    )

    list_filter = (
        'payment_type',
    )