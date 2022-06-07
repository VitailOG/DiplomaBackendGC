import string
from random import choice
from mixer.backend.django import mixer

from rest_framework.test import APIRequestFactory, force_authenticate

from methodist.constants import DEPARTMENT_ID_TEST


class APITestRequestFactory(APIRequestFactory):

    def __init__(self, perm: str, anon: bool = False, *args, **kwargs):
        super(APITestRequestFactory, self).__init__(*args, **kwargs)
        self.perm = perm
        self.anon = anon

    def _create_user(self):
        user_opts = {
            'is_staff': False,
            'is_superuser': True,
            'group__name': self.perm,
            'department_id': DEPARTMENT_ID_TEST
        }
        user = mixer.blend('methodist.CustomUser', **user_opts)
        self.password = ''.join([choice(string.hexdigits) for _ in range(6)])
        user.set_password(self.password)
        user.save()
        return user

    def _api_call(self, method: str, expected: int | None = None, *args, **kwargs):
        view = kwargs.pop('view')
        view_kwargs = kwargs.pop('view_kwargs')
        detail_args = kwargs.pop('detail_args') if kwargs.get('detail_args', None) is not None else {}

        request = getattr(super(), method)(*args, **kwargs)

        if not self.anon:
            user = self._create_user()
            force_authenticate(request, user=user)

        response = view.as_view(view_kwargs)(request, **detail_args)

        assert response.status_code == expected

        return response

    def get(self, *args, **kwargs):
        return self._api_call('get', expected=kwargs.pop('status'), **kwargs)

    def post(self, *args, **kwargs):
        return self._api_call('post', expected=kwargs.pop('status'), **kwargs)

    def put(self, *args, **kwargs):
        return self._api_call('put', expected=kwargs.pop('status'), **kwargs)

    def patch(self, *args, **kwargs):
        return self._api_call('patch', expected=kwargs.pop('status'), **kwargs)

    def delete(self, *args, **kwargs):
        return self._api_call('delete', expected=kwargs.pop('status'), **kwargs)
