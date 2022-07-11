from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static
from ninja import NinjaAPI

from GradeBookGC_BACKEND import settings
from GradeBookGC_BACKEND.swagger import schema_view
from student.api.views import api
from analytics.api.views import api as analytics_api
from trello.api.views import api as trello_api

app = NinjaAPI()

app.add_router('/', api)
app.add_router('/analytics', analytics_api)
app.add_router('/trello', trello_api)


urlpatterns = [
    path('admin/', admin.site.urls),

    path('methodist/', include('methodist.urls')),
    path('auth/', include('authentication.urls')),
    path('administration/', include('administration.urls')),
    path('student/', app.urls),

    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('__debug__/', include('debug_toolbar.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
