from django.urls import path

from .views import CityListAPIView

from .views import MyCompanyAPIView

urlpatterns = [

    path(
        'cities/',
        CityListAPIView.as_view()
    ),

]

urlpatterns = [

    path(
        'my-company/',
        MyCompanyAPIView.as_view(),
        name='my-company'
    ),

]