from django.urls import path

from .views import CreateTokensAPI, TokenRefreshAPI, LogoutAPI, ChangePasswordUserAPI, ChangeUsernameAPI
from django.utils.decorators import method_decorator


urlpatterns = [
    path('token/refresh/', TokenRefreshAPI.as_view()),
    path('token/create/', CreateTokensAPI.as_view()),
    path('logout/', LogoutAPI.as_view()),
    path('change-password/', ChangePasswordUserAPI.as_view()),
    path('change-username/', ChangeUsernameAPI.as_view()),
]
