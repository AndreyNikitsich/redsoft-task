from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenBlacklistView,
    TokenRefreshView,
)
from .views import UserViewSet

urlpatterns = [
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("users/", UserViewSet.as_view({"get": "list"}), name="list-users"),
    path(
        "users/<int:pk>",
        UserViewSet.as_view(
            {"post": "partial_update", "put": "update", "get": "retrieve"}
        ),
        name="user-retrieve-update",
    ),
    path(
        "registration/",
        UserViewSet.as_view({"post": "create"}),
        name="user-registration",
    ),
    path("logout/", TokenBlacklistView.as_view(), name="token_blacklist"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
