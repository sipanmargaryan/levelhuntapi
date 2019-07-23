import collections
import secrets

from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from core.utils import get_file_path
from skills.models import Skill

__all__ = (
    'User',
    'SocialConnection',
)


class User(AbstractUser):
    NEWSLETTER = 'nl'

    NOTIFICATION_CHOICES = (
        (NEWSLETTER, _('Subscribe to our Newsletter')),
    )

    NOTIFICATION_CHOICES_DICT = collections.OrderedDict(NOTIFICATION_CHOICES)

    email = models.EmailField()
    title = models.CharField(max_length=200, null=True)
    avatar = models.ImageField(upload_to=get_file_path, blank=True)
    birthday = models.DateField(null=True)
    bio = models.TextField(null=True)
    location = models.CharField(max_length=200, null=True)

    available_for_hire = models.BooleanField(default=True)
    email_settings = ArrayField(
        models.CharField(choices=NOTIFICATION_CHOICES, max_length=2, default=NEWSLETTER),
        size=len(NOTIFICATION_CHOICES),
        default=list,
    )

    email_confirmation_token = models.CharField(max_length=64, editable=False, null=True)
    reset_password_token = models.CharField(max_length=64, editable=False, null=True)
    reset_password_request_date = models.DateTimeField(null=True)

    skills = models.ManyToManyField(Skill, blank=True)

    def generate_password_request_date(self):
        self.reset_password_request_date = timezone.now()

    def can_request_password_reset(self) -> bool:
        if not self.reset_password_request_date:
            return True
        return timezone.now() - self.reset_password_request_date > timezone.timedelta(minutes=5)

    def can_reset_password(self) -> bool:
        return timezone.now() - self.reset_password_request_date <= timezone.timedelta(minutes=5)

    def get_email_settings(self):
        email_settings = []
        for key, notification in self.NOTIFICATION_CHOICES:
            setting = dict(
                notification_type=key,
                notification_text=notification,
                enabled=False,
            )

            if key in self.email_settings:
                setting['enabled'] = True

            email_settings.append(setting)

        return email_settings

    @staticmethod
    def generate_token() -> str:
        return secrets.token_urlsafe()


class SocialConnection(models.Model):
    GOOGLE = 'google'
    FACEBOOK = 'facebook'

    PROVIDERS = (
        (GOOGLE, 'Google'),
        (FACEBOOK, 'Facebook'),
    )

    provider = models.CharField(max_length=2, choices=PROVIDERS)
    provider_id = models.CharField(max_length=32, unique=True)

    user = models.OneToOneField(User, on_delete=models.CASCADE)
