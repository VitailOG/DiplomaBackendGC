import pytest

from GradeBookGC_BACKEND.request_factory import APITestRequestFactory
from GradeBookGC_BACKEND.settings import PermissionGroupChoice


@pytest.fixture
def administration_api():
    return APITestRequestFactory(perm=PermissionGroupChoice.ADMINISTRATION.value)


@pytest.fixture
def groups():
    ...


@pytest.fixture
def education_programs():
    ...


@pytest.fixture
def department():
    ...
