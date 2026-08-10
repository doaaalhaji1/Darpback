"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from companies.api.views import CompanyListAPIView
from rest_framework_simplejwt.views import TokenRefreshView
from accounts.views import CustomTokenObtainPairView


from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from django.http import HttpResponse

def home(request):
    return HttpResponse("Darbak API is running successfully")



urlpatterns = [
    path('api/companies/', CompanyListAPIView.as_view(), name='company-list'),
    path('', home),

     path(
    'api/token/',
    CustomTokenObtainPairView.as_view(),
    name='token_obtain_pair'
    ),
    path(
    'api/token/refresh/',
    TokenRefreshView.as_view(),
    name='token_refresh'
    ),

    path(
        'admin/',
        admin.site.urls
    ),

    path(
        'api/',
        include('companies.api.urls')
    ),

    path(
    'api/',
    include('trips.api.urls')
    ),

    path(
    'api/',
    include('bookings.api.urls')
    ),

    path(
    'api/',
    include('accounts.api.urls')
    ),

    path(
    'api/',
    include('companies.api.urls')
    ),

    path(
    'api/',
    include('invoices.api.urls')
    ),


]

urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)


