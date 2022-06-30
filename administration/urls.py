from rest_framework import routers

from administration.api.views import DepartmentAPI, TeacherAPI

router = routers.SimpleRouter()

router.register('department', DepartmentAPI)

router.register('teachers', TeacherAPI)

urlpatterns = []

urlpatterns += router.urls

