# import pytest
#
# from rest_framework import status
# from methodist.tests.api.urls import SubjectUrl
# from methodist.api.views import SubjectApi
# from methodist.tests.api.schemas.subject import SubjectsSchema, SubjectDetailSchema
# from methodist.models import Subject
#
#
# pytestmark = [pytest.mark.django_db]
#
#
# def test_list_subjects(api, methodist):
#     request = api.get(SubjectUrl.SUBJECT_BASE.value)
#     request.user = methodist
#     response = SubjectApi.as_view({"get": "list"})(request)
#     assert SubjectsSchema(**response.data['results'][0])
#     assert response.status_code == status.HTTP_200_OK
#
#
# def test_detail_subjects(api):
#     request = api.get(SubjectUrl.SUBJECT_BASE.value)
#     response = SubjectApi.as_view({"get": "retrieve"})(request, pk=1)
#     assert SubjectDetailSchema(**response.data)
#     assert response.status_code == status.HTTP_200_OK
#
#
# def test_create_subjects(api, data):
#     request = api.post(SubjectUrl.SUBJECT_BASE.value, data=data)
#     response = SubjectApi.as_view({"post": "create"})(request)
#     assert SubjectsSchema(**response.data)
#     assert response.status_code == status.HTTP_201_CREATED
#
#
# def test_update_subject(api, data, methodist):
#     subject = Subject.objects.get(id=1)
#     assert subject.name_subject != data['name_subject']
#     request = api.put(SubjectUrl.SUBJECT_BASE.value, data=data)
#     request.user = methodist
#     response = SubjectApi.as_view({"put": "update"})(request, pk=1)
#     subject.refresh_from_db()
#     assert SubjectsSchema(**response.data)
#     assert subject.name_subject == data['name_subject']
#     assert response.status_code == status.HTTP_200_OK
