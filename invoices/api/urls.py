from django.urls import path

from .views import (
    InvoiceListAPIView,
    InvoiceDetailAPIView,
    InvoicePayAPIView,
    MyInvoicesAPIView,  
)

urlpatterns = [

    path(
        'invoices/',
        InvoiceListAPIView.as_view(),
        name='invoice-list'
    ),
        path('my-invoices/', MyInvoicesAPIView.as_view(), name='my-invoices'),   # ← والمسار


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