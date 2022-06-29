import pytest
from rest_framework import status

from administration.api.views import DepartmentAPI
from administration.tests.api.urls import DepartmentUrl

pytestmark= [pytest.mark.django_db]


def test_department(administration_api):
    response = administration_api.get(
        path=DepartmentUrl.DEPARTMENT_LIST.value,
        view=DepartmentAPI,
        view_kwargs={"get": "list"},
        status=status.HTTP_200_OK
    )

    assert True
