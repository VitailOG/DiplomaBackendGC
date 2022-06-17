from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import CustomTokenObtainPairView, CreateTokensAPI
from django.utils.decorators import method_decorator


urlpatterns = [
    path('api/token/', CustomTokenObtainPairView.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view()),
    path('api/t/', CreateTokensAPI.as_view())
]
