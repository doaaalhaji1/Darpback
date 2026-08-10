from django.urls import path

from .views import (
    InvoiceListAPIView,
    InvoiceDetailAPIView,
    InvoicePayAPIView
)

urlpatterns = [

    path(
        'invoices/',
        InvoiceListAPIView.as_view(),
        name='invoice-list'
    ),

    path(
        'invoices/<int:pk>/',
        InvoiceDetailAPIView.as_view(),
        name='invoice-detail'
    ),

    path(
        'invoices/<int:pk>/pay/',
        InvoicePayAPIView.as_view(),
        name='invoice-pay'
    ),

]