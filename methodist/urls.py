from rest_framework import routers

from methodist.api.views import StudentApi, SubjectApi, RatingApi, GroupApi

router = routers.SimpleRouter()

router.register('student', StudentApi, basename='student')

router.register('subject', SubjectApi, basename='subject')

router.register('rating', RatingApi, basename='rating')

router.register('group', GroupApi, basename='group')

urlpatterns = []

urlpatterns += router.urls
