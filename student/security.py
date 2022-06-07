from jose import jwt
from datetime import datetime, timedelta

from django.http import HttpRequest
from django.conf import settings
from django.shortcuts import get_object_or_404
from ninja.security import HttpBearer

from methodist.models import CustomUser


class AuthBearer(HttpBearer):

    def authenticate(self, request: HttpRequest, token: str):
        user = self._get_current_user(self._decode_access_token(token))
        if user is not None:
            return user
        return None

    def _decode_access_token(self, token: str) -> str | None:
        try:
            decode_data = jwt.decode(token, settings.SECRET_KEY, 'HS256')
            exp, user_id = decode_data.get('exp'), decode_data.get('user_id')

            now = datetime.utcnow()
            expired_time = datetime.fromtimestamp(exp) + timedelta(days=10)

            if expired_time < now:
                return None

            return user_id
        except jwt.JWSError:
            return None

    def _get_current_user(self, user_id: int | None) -> CustomUser:
        if user_id is not None:
            return get_object_or_404(CustomUser, id=user_id)
