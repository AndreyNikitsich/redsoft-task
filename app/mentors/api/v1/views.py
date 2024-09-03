from django.contrib.auth import get_user_model
from rest_framework import permissions, viewsets, mixins
from rest_framework.response import Response

from .permissions import IsTheSameUserOrReadOnly
from .serializers import (
    UserRegistrationSerializer,
    UserDetailSerializer,
    UserUpdateSerializer,
)


class UserViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = get_user_model().objects

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = (permissions.AllowAny,)
        elif self.action in ["list", "retrieve"]:
            self.permission_classes = (permissions.IsAuthenticated,)
        elif self.action in ["update", "partial_update"]:
            self.permission_classes = (
                permissions.IsAuthenticated,
                IsTheSameUserOrReadOnly,
            )
        return super(UserViewSet, self).get_permissions()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        if request.user.id == instance.id:
            data["password"] = instance.get_decrypted_password()
        return Response(data)

    def get_serializer_class(self):
        if self.action == "create":
            return UserRegistrationSerializer
        elif self.action in ["list", "retrieve"]:
            return UserDetailSerializer
        elif self.action in ["update", "partial_update"]:
            return UserUpdateSerializer
        else:
            return UserDetailSerializer
