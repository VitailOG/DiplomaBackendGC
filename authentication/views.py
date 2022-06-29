from django.http import HttpResponse
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import GenericAPIView
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.views import TokenViewBase
from rest_framework_simplejwt.serializers import TokenRefreshSerializer

from authentication.serializers import (
    CustomTokenObtainPairSerializer,
    ChangePasswordUserSerializer,
    ChangeUsernameSerializer
)

User = get_user_model()


class CustomTokenViewBase(TokenViewBase):
    """ Base api for tokens """

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        # tokens
        access = serializer.validated_data.get('access')
        refresh = serializer.validated_data.get('refresh')

        # create response instance
        response = Response(data=serializer.validated_data)

        # create cookies
        response.set_cookie('access', access)
        response.set_cookie('refresh', refresh)
        return response


class CreateTokensAPI(CustomTokenViewBase):
    """ Create tokens """
    serializer_class = CustomTokenObtainPairSerializer


class TokenRefreshAPI(CustomTokenViewBase):
    """ Refresh token API """
    serializer_class = TokenRefreshSerializer


class LogoutAPI(APIView):
    """ Remove tokens from cookies """
    def post(self, request, *args, **kwargs):
        response = HttpResponse()
        response.delete_cookie('access')
        response.delete_cookie('refresh')
        return response


class ChangePasswordUserAPI(GenericAPIView, APIView):
    """ Change password """
    serializer_class = ChangePasswordUserSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        instance = self.get_serializer(data=request.data)
        instance.is_valid(raise_exception=True)

        # get validated old and new passwords
        old_password, new_password = instance.validated_data.values()
        user = User.objects.get(pk=request.user.id)

        # check user on old password
        if user.check_password(old_password):
            user.set_password(new_password)
            user.save()
            return Response({"updated": True})

        return Response({"updated": False})


class ChangeUsernameAPI(GenericAPIView, APIView):
    """ Change username for user """
    serializer_class = ChangeUsernameSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        instance = self.get_serializer(data=request.data)
        instance.is_valid(raise_exception=True)
        new_username = instance.validated_data['new_username']
        # update username
        User.objects.filter(pk=request.user.id).update(username=new_username)
        return Response({"updated": True})
