from django_filters import rest_framework as filters

from django.contrib.postgres.search import SearchVector
from django.db.models import QuerySet

from universities.models import University


class UniversityFilter(filters.FilterSet):
    q = filters.CharFilter(method='search', label='Search query', field_name='name')

    class Meta:
        model = University
        fields = ('name', )

    # noinspection PyMethodMayBeStatic
    def search(self, queryset: QuerySet, field_name: str, value: str) -> QuerySet:
        return queryset.annotate(search=SearchVector(field_name, 'keywords')).filter(search=value)
