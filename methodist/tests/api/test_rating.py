import pytest

from rest_framework import status

pytestmark = [pytest.mark.django_db]


# from methodist.tests.api.schemas.rating import *
# from methodist.tests.api.urls import RatingUrl
# from methodist.api.views import RatingApi


# def test_group(api, subjects, students, ratings):
#     r = api.get(RatingUrl.RATING_GROUP.value)
#     res = RatingApi.as_view({"get": "group"})(r, subject_id=subjects.id)
#     assert RatingGroupSchema(**res.data)
#     assert res.status_code == status.HTTP_200_OK
