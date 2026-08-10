from rest_framework.generics import ListAPIView

from companies.models import City
from .serializers import CitySerializer

from rest_framework.generics import RetrieveAPIView

from rest_framework.permissions import IsAuthenticated

from companies.models import TransportCompany

from .serializers import CompanySerializer
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from companies.models import TransportCompany
from .serializers import CompanySerializer
from accounts.permissions import (
    IsAdminOrCompanyManager
)

class CompanyListAPIView(ListAPIView):
    queryset = TransportCompany.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated]
class CityListAPIView(ListAPIView):

    queryset = City.objects.all()

    serializer_class = CitySerializer

class MyCompanyAPIView(RetrieveAPIView):

    serializer_class = CompanySerializer

    permission_classes = [
        IsAuthenticated,
        IsAdminOrCompanyManager
    ]

    def get_object(self):

        return TransportCompany.objects.get(
            manager=self.request.user
        )