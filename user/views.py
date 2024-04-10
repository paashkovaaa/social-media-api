from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import generics, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from social_media_system.permissions import IsOwnerProfileOrReadOnly
from user.models import User
from user.serializers import (
    UserRegistrationSerializer,
    UserProfileSerializer,
)


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer


class ManageUserView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserProfileSerializer
    authentication_classes = [
        JWTAuthentication,
    ]
    permission_classes = [
        IsOwnerProfileOrReadOnly,
    ]

    def get_object(self):
        return self.request.user


class UsersView(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet,
):
    serializer_class = UserProfileSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    @staticmethod
    def _params_to_ints(qs):
        """Converts a list of string IDs to a list of integers"""
        return [int(str_id) for str_id in qs.split(",")]

    def get_queryset(self):
        username = self.request.query_params.get("username")
        queryset = User.objects.all()

        if username:
            queryset = queryset.filter(username__icontains=username)
        return queryset.distinct()

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "username",
                type=OpenApiTypes.STR,
                description="Filter by username (ex. ?username=user1)",
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
