from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import JSONField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from core.utils import get_file_path

__all__ = (
    'University',
    'Education',
)


class University(models.Model):
    name = models.CharField(max_length=255, unique=True)
    logo = models.ImageField(upload_to=get_file_path, null=True)
    logo_url = models.URLField(null=True)
    is_verified = models.BooleanField(default=False)
    keywords = models.TextField(null=True, help_text=_('Country, Unicode name of University, etc...'))
    additional_data = JSONField(null=True)

    class Meta:
        verbose_name_plural = _('Universities')


class Education(models.Model):
    YEAR_VALIDATORS = (
        MinValueValidator(1900),
        MaxValueValidator(timezone.now().year),
    )

    BACHELOR = 'bachelor'
    MASTER = 'master'
    PHD = 'phd'
    DEGREES = (
        (BACHELOR, _('Bachelor')),
        (MASTER, _('Master')),
        (PHD, _('PHD')),
    )

    start_year = models.IntegerField(validators=YEAR_VALIDATORS)
    end_year = models.IntegerField(validators=YEAR_VALIDATORS, null=True)
    degree = models.CharField(max_length=16, choices=DEGREES, default=BACHELOR)
    field_of_study = models.CharField(max_length=255, null=True)
    description = models.TextField(null=True)

    university = models.ForeignKey(University, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
