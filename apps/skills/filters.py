from django_filters import rest_framework as filters

from .models import Topic

__all__ = (
    'TopicFilter',
)


class TopicFilter(filters.FilterSet):
    skill_slug = filters.CharFilter(field_name='skill__slug', required=True)

    class Meta:
        model = Topic
        fields = ['skill_slug']
