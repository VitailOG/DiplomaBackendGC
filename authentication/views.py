from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenViewBase

from authentication.serializers import CustomTokenObtainPairSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class CreateTokensAPI(TokenViewBase):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        # tokens
        access = serializer.validated_data.pop('access')
        refresh = serializer.validated_data.pop('refresh')

        # create response instance
        response = Response(data=serializer.validated_data)

        # create cookies
        response.set_cookie('access', access)
        response.set_cookie('refresh', refresh)
        return response
