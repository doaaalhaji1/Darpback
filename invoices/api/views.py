from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView
)

from rest_framework.permissions import IsAuthenticated

from invoices.models import Invoice

from .serializers import InvoiceSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.utils import timezone
from invoices.models import Invoice

from accounts.permissions import IsSystemAdmin

from rest_framework.permissions import IsAuthenticated


class InvoiceListAPIView(ListAPIView):

    serializer_class = InvoiceSerializer

    permission_classes = [
        IsAuthenticated,
        IsSystemAdmin
    ]

    def get_queryset(self):

        return Invoice.objects.select_related(
            'booking',
            'booking__user',
            'booking__trip',
            'booking__trip__company'
        ).all().order_by('-id')

    
class InvoiceDetailAPIView(RetrieveAPIView):

    queryset = Invoice.objects.all()

    serializer_class = InvoiceSerializer

    permission_classes = [
        IsAuthenticated,
        IsSystemAdmin
    ]
class InvoicePayAPIView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def post(self, request, pk):

        try:

            invoice = Invoice.objects.get(
                pk=pk,
                booking__user=request.user
            )

        except Invoice.DoesNotExist:

            return Response(
                {
                    "error": "Invoice Not Found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        if invoice.payment_status == 'PAID':

            return Response(
                {
                    "error": "Invoice Already Paid"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        invoice.payment_status = 'PAID'

        invoice.payment_date = timezone.now()

        invoice.save()

        return Response(
            {
                "message": "Payment Completed Successfully"
            }
        )