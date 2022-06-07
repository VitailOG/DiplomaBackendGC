# import pytest
# from decimal import Decimal
# from django_lifecycle.decorators import DjangoLifeCycleException
# from rest_framework import status
#
# from methodist.tests.api.schemas.group import TopStudentSchema
# from methodist.tests.api.urls import GroupUrl
# from methodist.api.views import GroupApi
# from methodist.models import ExtraPoints
#
# pytestmark = [pytest.mark.django_db]
#
#
# def test_create_extra_point_correct(api, students):
#     data = {
#       "semester": 3,
#       "point": "0.3",
#       "text": "text",
#       "user": students[0].id
#     }
#     assert not ExtraPoints.objects.exists()
#     request = api.post(GroupUrl.CREATE_EXTRA_POINT.value, data=data)
#     response = GroupApi.as_view({"post": "create_extra_points"})(request)
#     assert response.status_code == status.HTTP_201_CREATED
#     assert response.data['semester'] == data['semester']
#     assert response.data['text'] == data['text']
#
#
# def test_create_extra_point_incorrect(api, students):
#     data = {
#       "semester": 3,
#       "point": "0.6",
#       "text": "text",
#       "user": students[0].id
#     }
#     assert not ExtraPoints.objects.exists()
#
#     with pytest.raises(DjangoLifeCycleException):
#         request = api.post(GroupUrl.CREATE_EXTRA_POINT.value, data=data)
#         GroupApi.as_view({"post": "create_extra_points"})(request)
#     assert not ExtraPoints.objects.exists()
#
#
# def test_edit_extra_point(api, extra_point):
#     data = {
#         'point': '0.1'
#     }
#     assert ExtraPoints.objects.first().point == Decimal('0.20')
#     r = api.put(GroupUrl.UPDATE_EXTRA_POINT.value, data=data)
#     res = GroupApi.as_view({"put": "edit"})(r, pk=1)
#     assert ExtraPoints.objects.first().point == Decimal('0.10')
#     assert res.data is None
#     assert res.status_code == status.HTTP_204_NO_CONTENT
#
#
# def test_detail_group_top(api, subjects, students):
#     r = api.get(GroupUrl.DETAIL_GROUP.value, data={"is_all_students": "false"})
#     res = GroupApi.as_view({"get": "detail_group"})(r, pk=2, semester=subjects.semester)
#     assert len(res.data) == 0
#     assert res.status_code == status.HTTP_200_OK
#
#
# def test_detail_group_top_all(api, students, ratings, subjects):
#     r = api.get(GroupUrl.DETAIL_GROUP.value, data={"is_all_students": "true"})
#     res = GroupApi.as_view({"get": "detail_group"})(r, pk=2, semester=subjects.semester)
#     assert len(res.data) == 1
#     assert res.status_code == status.HTTP_200_OK
#
#
# def test_calc_rating(api, students, ratings, subjects):
#     r = api.get(GroupUrl.DETAIL_GROUP.value, data={"is_all_students": "true"})
#     res = GroupApi.as_view({"get": "detail_group"})(r, pk=2, semester=subjects.semester)
#     assert res.data[0]['total_rating'] == 4.5
#
#
# def test_calc_rating_with_extra_point(api, subjects, students, ratings, extra_point):
#     r = api.get(GroupUrl.DETAIL_GROUP.value, data={"is_all_students": "true"})
#     res = GroupApi.as_view({"get": "detail_group"})(r, pk=2, semester=subjects.semester)
#     assert res.data[0]['total_rating'] == 4.7
#     assert TopStudentSchema(**res.data[0])
