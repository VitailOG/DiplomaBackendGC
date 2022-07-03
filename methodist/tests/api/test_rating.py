import pytest

from django.db import IntegrityError
from rest_framework import status

from methodist.tests.api.schemas.rating import RatingGroupSchema
from methodist.tests.api.urls import RatingUrl
from methodist.api.views import RatingApi


pytestmark = [pytest.mark.django_db]


def test_group(methodist_api, subjects, students, ratings):
    res = methodist_api.get(
        path=RatingUrl.RATING_GROUP.value,
        view=RatingApi,
        view_kwargs={"get": "group"},
        status=status.HTTP_200_OK,
        detail_args={"subject_id": subjects.id}
    )

    assert RatingGroupSchema(**res.data)


def test_create_two_rating_for_student(methodist_api, students, subjects, users):
    data = {
      "user": students[0].id,
      "subject": subjects.id,
      "date_rating": "2022-06-30",
      "rating_5": 5,
      "rating_12": 0,
      "retransmission": True,
      "credited": True,
      "semester": 2,
      "is_annual_assessment": True,
      "teacher": users[2].id
    }

    methodist_api.post(
        path=RatingUrl.RATING_GROUP.value,
        view=RatingApi,
        data=data,
        view_kwargs={"post": "create"},
        status=status.HTTP_201_CREATED
    )

    with pytest.raises(IntegrityError):
        methodist_api.post(
            path=RatingUrl.RATING_GROUP.value,
            view=RatingApi,
            data=data,
            view_kwargs={"post": "create"},
            status=status.HTTP_201_CREATED
        )
