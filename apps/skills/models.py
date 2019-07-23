from django_extensions.db.fields import AutoSlugField
from django_extensions.db.models import TimeStampedModel

from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models.models import *  # noqa
from core.utils import get_file_path

__all__ = (
    'Category',
    'Skill',
    'Topic',
)


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    @property
    def skills(self):
        return self.skill_set.count()

    class Meta:
        verbose_name_plural = _('Categories')


class Skill(AbstractStatusModel, AbstractOrderingModel):
    name = models.CharField(max_length=100, unique=True)
    slug = AutoSlugField(populate_from='name', editable=True)
    description = models.TextField(null=True, blank=True)
    keywords = models.TextField(null=True, blank=True)

    categories = models.ManyToManyField(Category, blank=True)

    # images
    logo = models.ImageField(upload_to=get_file_path)
    cover = models.ImageField(upload_to=get_file_path)

    def __str__(self):  # pragma: no cover
        return self.name


class Topic(AbstractStatusModel, AbstractOrderingModel, TimeStampedModel):
    name = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from='name', editable=True)
    documentation = models.TextField(null=True, blank=True)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)

    def __str__(self):  # pragma: no cover
        return self.name
