from django.conf import settings

from core.email.utils import send_email
from core.utils.utils import build_client_absolute_url

__all__ = (
    'send_email_address_confirmation',
    'send_forgot_password_request',
)


def send_email_address_confirmation(user):
    email_confirmation_path = '/confirm/{token}'.format(
        token=user.email_confirmation_token
    )

    subject = 'Confirm your registration at {site_name}'.format(
        site_name=settings.SITE_NAME
    )

    send_email(
        subject=subject,
        template_name='emails/email-address-confirmation.html',
        context={
            'email_confirmation_url': build_client_absolute_url(email_confirmation_path),
        },
        to=user.email,
    )


def send_forgot_password_request(user):
    reset_password_path = '/reset-password/{token}'.format(
        token=user.reset_password_token
    )

    subject = 'Reset your {site_name} password'.format(
        site_name=settings.SITE_NAME
    )

    send_email(
        subject=subject,
        template_name='emails/forgot-password-request.html',
        context={
            'reset_password_url': build_client_absolute_url(reset_password_path),
        },
        to=user.email,
    )


def send_change_password(user):
    subject = 'Your {site_name} password has been changed'.format(
        site_name=settings.SITE_NAME
    )

    send_email(
        subject=subject,
        template_name='emails/change-password.html',
        to=user.email,
    )
