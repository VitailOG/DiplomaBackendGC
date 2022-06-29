from typing import NamedTuple
from jose import jwt
from datetime import datetime

from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import authentication, exceptions
from rest_framework.exceptions import AuthenticationFailed


User = get_user_model()


class AuthResponse(NamedTuple):
    user: User
    token: str


class JWTAuthBackend(authentication.BaseAuthentication):
    authentication_header_prefix = 'Bearer'

    def authenticate(self, request, token=None, **kwargs) -> AuthResponse | None:
        auth_cookie = request.COOKIES.get('access', None)

        if auth_cookie is not None:
            return self.cookies_auth(token=auth_cookie)

        auth_header = authentication.get_authorization_header(request).split()
        header_prefix = self.authentication_header_prefix.encode().lower()

        if not auth_header or auth_header[0].lower() != header_prefix:
            return None

        if len(auth_header) == 1:
            raise exceptions.AuthenticationFailed('Invalid token header. No credential provided.')

        elif len(auth_header) > 2:
            raise exceptions.AuthenticationFailed(
                'Invalid token header. Token string should not contain spaces'
            )

        try:
            token = auth_header[1].decode('utf-8')
        except UnicodeError:
            raise exceptions.AuthenticationFailed(
                'Invalid token header. Token string should not contain invalid characters.'
            )

        return self.authenticate_credential(token)

    def cookies_auth(self, token: str) -> AuthResponse:
        return self.authenticate_credential(token)

    def authenticate_credential(self, token: str) -> AuthResponse:

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)
        except jwt.JWSError:
            raise exceptions.AuthenticationFailed('Invalid authentication. Could not decode token.')

        token_exp = datetime.fromtimestamp(payload['exp'])
        if token_exp < datetime.utcnow():
            raise exceptions.AuthenticationFailed('Token expired.')

        user = self.get_user(user_id=payload['user_id'])

        return AuthResponse(user=user, token=token)

    def get_user(self, user_id: int):

        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            raise AuthenticationFailed('User not found', code='user_not_found')

        if not user.is_active:
            raise AuthenticationFailed('User not active', code='user_not_active')

        return user
