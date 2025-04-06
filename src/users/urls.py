from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from .views import (
    ChangePasswordView,
    RegisterUserAPIView,
    UserListAPIView,
    UserUpdateDestroyAPIView,
)

urlpatterns = [
    path("", UserListAPIView.as_view(), name="user_list"),
    path("<int:id>/", UserUpdateDestroyAPIView.as_view(), name="user_update_delete"),
    path("register/", RegisterUserAPIView.as_view(), name="register_user"),
    path("login/", jwt_views.TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", jwt_views.TokenRefreshView.as_view(), name="token_refresh"),
    path("change_password/", ChangePasswordView.as_view(), name="change_password"),
]
