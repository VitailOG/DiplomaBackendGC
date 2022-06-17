from decimal import Decimal

import pytest
from django_lifecycle.decorators import DjangoLifeCycleException

from rest_framework import status

from methodist.tests.api.schemas.group import TopStudentSchema, CommonRatingSchema
from methodist.tests.api.urls import GroupUrl
from methodist.api.views import GroupApi
from methodist.models import ExtraPoints

pytestmark = [pytest.mark.django_db]


@pytest.fixture
def present_data_extra_point(students):
    return {
      "semester": 3,
      "point": "0.3",
      "text": "text",
      "user": students[0].id
    }


def test_create_extra_point_correct(methodist_api, present_data_extra_point):
    assert not ExtraPoints.objects.exists()
    response = methodist_api.post(
        path=GroupUrl.CREATE_EXTRA_POINT.value,
        view=GroupApi,
        data=present_data_extra_point,
        view_kwargs={"post": "create_extra_points"},
        status=status.HTTP_201_CREATED
    )

    assert response.data['semester'] == present_data_extra_point['semester']
    assert response.data['text'] == present_data_extra_point['text']


def test_create_extra_point_not_methodist(not_methodist_api, present_data_extra_point):
    not_methodist_api.post(
        path=GroupUrl.CREATE_EXTRA_POINT.value,
        view=GroupApi,
        data=present_data_extra_point,
        view_kwargs={"post": "create_extra_points"},
        status=status.HTTP_403_FORBIDDEN
    )


def test_create_extra_point_incorrect(methodist_api, students):
    data = {
          "semester": 3,
          "point": "0.6",
          "text": "text",
          "user": students[0].id
    }
    assert not ExtraPoints.objects.exists()

    with pytest.raises(DjangoLifeCycleException):
        methodist_api.post(
            path=GroupUrl.CREATE_EXTRA_POINT.value,
            view=GroupApi,
            data=data,
            view_kwargs={"post": "create_extra_points"},
            status=status.HTTP_201_CREATED
        )

    assert not ExtraPoints.objects.exists()


def test_edit_extra_point(methodist_api, extra_point):
    data = {
        'point': '0.1'
    }
    assert ExtraPoints.objects.first().point == Decimal('0.20')
    req = methodist_api.put(
        path=GroupUrl.UPDATE_EXTRA_POINT.value,
        view=GroupApi,
        data=data,
        view_kwargs={"put": "edit"},
        status=status.HTTP_204_NO_CONTENT,
        detail_args={"pk": extra_point.id}
    )

    assert req.data is None
    assert ExtraPoints.objects.first().point == Decimal('0.10')


def test_detail_group_top(methodist_api, subjects, students):
    response = methodist_api.get(
        path=GroupUrl.DETAIL_GROUP.value,
        view=GroupApi,
        view_kwargs={"get": "detail_group"},
        detail_args={"pk": 2, "semester": subjects.semester},
        status=status.HTTP_200_OK
    )

    assert len(response.data) == 0


def test_detail_group_top_all(methodist_api, subjects, students):
    response = methodist_api.get(
        path=GroupUrl.DETAIL_GROUP.value,
        view=GroupApi,
        view_kwargs={"get": "detail_group"},
        detail_args={"pk": 2, "semester": subjects.semester},
        status=status.HTTP_200_OK,
        data={"is_all_students": "true"}
    )

    assert TopStudentSchema(**response.data[0])
    assert len(response.data) == 1


def test_calc_rating(methodist_api, students, ratings, subjects):
    response = methodist_api.get(
        path=GroupUrl.DETAIL_GROUP.value,
        data={"is_all_students": "true"},
        view=GroupApi,
        view_kwargs={"get": "detail_group"},
        detail_args={"pk": 2, "semester": subjects.semester},
        status=status.HTTP_200_OK
    )

    assert response.data[0]['total_rating'] == 4.5


def test_calc_rating_with_extra_point(methodist_api, subjects, students, ratings, extra_point):
    response = methodist_api.get(
        path=GroupUrl.DETAIL_GROUP.value,
        view=GroupApi,
        data={"is_all_students": "true"},
        detail_args={"pk": 2, "semester": subjects.semester},
        view_kwargs={"get": "detail_group"},
        status=status.HTTP_200_OK
    )

    assert response.data[0]['total_rating'] == 4.7
    assert TopStudentSchema(**response.data[0])


def test_common_rating_students(methodist_api, students):
    req = methodist_api.get(
        path='/methodist/group/1/common-ratings-students/',
        view=GroupApi,
        view_kwargs={"get": "common_rating_students"},
        detail_args={"pk": 2},
        status=status.HTTP_200_OK
    )

    assert CommonRatingSchema(**req.data[0])
