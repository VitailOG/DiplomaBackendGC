from rest_framework import routers

from administration.api.views import DepartmentAPI

router = routers.SimpleRouter()

router.register('department', DepartmentAPI)

urlpatterns = []

urlpatterns += router.urls

