from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

# 1. استيراد CustomTokenObtainPairView من تطبيق users
from users.views import CustomTokenObtainPairView 

urlpatterns = [
    # 2. استخدام الكلاس الجديد بدلاً من TokenObtainPairView
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]