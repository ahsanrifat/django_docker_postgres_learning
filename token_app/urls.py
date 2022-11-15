from django.urls import path
from rest_framework_simplejwt.views import (
    # TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
    TokenBlacklistView
)

from token_app.views import MyTokenObtainPairView

urlpatterns = [
    path('', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),
]
