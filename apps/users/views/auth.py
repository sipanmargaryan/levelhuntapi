from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from ..serializers import *  # noqa

__all__ = (
    'LogInAPIView',
    'SignupAPIView',
    'ConfirmEmailAPIView',
    'ForgotPasswordAPIView',
    'ResetPasswordAPIView',
    'SocialConnectAPIView',
)


class LogInAPIView(GenericAPIView):
    """
    JWT authentication endpoint
    """
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = serializer.validated_data

        return Response(response)


class SignupAPIView(GenericAPIView):
    serializer_class = SignupSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = serializer.save()

        return Response(response, status=status.HTTP_201_CREATED)


class ConfirmEmailAPIView(GenericAPIView):
    serializer_class = ConfirmEmailSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = serializer.save()

        return Response(response)


class ForgotPasswordAPIView(GenericAPIView):
    serializer_class = ForgotPasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = serializer.save()

        return Response(response)


class ResetPasswordAPIView(GenericAPIView):
    serializer_class = ResetPasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = serializer.save()

        return Response(response)


class SocialConnectAPIView(GenericAPIView):
    serializer_class = SocialConnectSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = serializer.save()

        return Response(response)
