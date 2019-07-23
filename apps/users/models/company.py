from django_extensions.db.fields import AutoSlugField

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.utils import get_file_path

__all__ = (
    'Company',
    'CompanyMember',
)


class Company(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = AutoSlugField(populate_from='name', unique=True)
    logo = models.ImageField(upload_to=get_file_path)

    class Meta:
        verbose_name_plural = _('Companies')

    def __str__(self):  # pragma: no cover
        return self.name


class CompanyMember(models.Model):
    is_active = models.BooleanField(default=True)

    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    member = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
