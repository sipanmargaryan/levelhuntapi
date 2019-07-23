from django.apps import apps
from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache
from django.core.validators import MinValueValidator
from django.db import models, transaction
from django.db.models import F
from django.utils.translation import gettext_lazy as _

__all__ = (
    'AbstractStatusModel',
    'AbstractOrderingModel',
)


class AbstractOrderingModelManager(models.Manager):

    @staticmethod
    def get_parent_orderable(obj):
        for field in obj._meta.model._meta.get_fields():
            if field.related_model and issubclass(field.related_model, AbstractOrderingModel):
                return {field.name: getattr(obj, field.name, None)}
        return {}

    def move(self, item, ordering_number):
        filters = self.get_parent_orderable(item)
        queryset = (
            self.get_queryset()
                .filter(**filters)
                .exclude(pk=item.pk)
        )

        if queryset.filter(ordering_number=ordering_number).exists():
            with transaction.atomic():
                if item.ordering_number > int(ordering_number):
                    queryset.filter(
                        ordering_number__lt=item.ordering_number,
                        ordering_number__gte=ordering_number,
                    ).update(
                        ordering_number=F('ordering_number') + 1,
                    )
                elif item.ordering_number < int(ordering_number):
                    queryset.filter(
                        ordering_number__lte=ordering_number,
                        ordering_number__gt=item.ordering_number,
                    ).update(
                        ordering_number=F('ordering_number') - 1,
                    )
                item.ordering_number = ordering_number
                item.save()

    def create(self, **kwargs):
        instance = self.model(**kwargs)
        with transaction.atomic():
            filters = self.get_parent_orderable(instance)
            instance.ordering_number = self.filter(**filters).count() + 1
            instance.save()
            return instance


class AbstractStatusModel(models.Model):
    ACTIVE = 'active'
    INACTIVE = 'inactive'
    PENDING = 'pending'
    STATUSES = (
        (ACTIVE, _('Active')),
        (INACTIVE, _('Inactive')),
        (PENDING, _('Pending')),
    )

    status = models.CharField(max_length=16, choices=STATUSES, default=INACTIVE)

    class Meta:
        abstract = True


class AbstractOrderingModel(models.Model):
    CHOICES_CACHE_SECONDS = 60 * 60 * 60 * 24

    ordering_number = models.IntegerField(default=1, validators=[MinValueValidator(1)])

    objects = AbstractOrderingModelManager()

    class Meta:
        abstract = True

    def delete(self, *args, **kwargs):
        with transaction.atomic():
            self._meta.model.objects.filter(
                ordering_number__gt=self.ordering_number,
            ).update(
                ordering_number=F('ordering_number') - 1,
            )
            super(AbstractOrderingModel, self).delete(*args, **kwargs)

    @classmethod
    def as_choices(cls):
        choices = cache.get('orderable_choices')
        if not choices:
            choices = []
            for content_type in ContentType.objects.all():
                try:
                    model_class = apps.get_model(content_type.app_label, content_type.model, require_ready=False)
                    if issubclass(model_class, cls):
                        choices.append((content_type.model, model_class))
                except LookupError:
                    pass
            cache.set('orderable_choices', choices, cls.CHOICES_CACHE_SECONDS)
        return choices
