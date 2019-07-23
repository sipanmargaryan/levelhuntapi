from typing import Optional

from django_filters import rest_framework as filters

from django.db.models import QuerySet

from .models import Question

__all__ = (
    'QuestionFilter',
)


class QuestionFilter(filters.FilterSet):
    skill_slug = filters.CharFilter(field_name='skill__slug', required=True)
    topic_slug = filters.CharFilter(method='topic_filter', required=False)

    # noinspection PyMethodMayBeStatic
    def topic_filter(self, queryset: QuerySet, value: Optional[str]) -> QuerySet:
        if value:
            return queryset.filter(topics__slug=value)

        return queryset

    class Meta:
        model = Question
        fields = ['skill_slug', 'topic_slug']
