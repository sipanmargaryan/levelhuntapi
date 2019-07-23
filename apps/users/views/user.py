from rest_framework import parsers, permissions, viewsets
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from users.models import User
from users.serializers import (
    ChangeAvatarSerializer, ChangePasswordSerializer, UserSerializer
)

__all__ = (
    'UserViewSet',
    'ChangePasswordAPIView',
    'ChangeAvatarViewSet',
)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user


class ChangePasswordAPIView(GenericAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user

    def patch(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data,
            context=dict(
                user=self.get_object()
            )
        )

        serializer.is_valid(raise_exception=True)
        response = serializer.change_password(
            password=serializer.validated_data['new_password'],
        )

        return Response(response)


class ChangeAvatarViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = ChangeAvatarSerializer
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = (parsers.MultiPartParser,)

    def get_object(self):
        return self.request.user
