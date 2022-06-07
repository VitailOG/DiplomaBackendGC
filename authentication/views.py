from rest_framework_simplejwt.views import TokenObtainPairView

from authentication.serializers import CustomTokenObtainPairSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
