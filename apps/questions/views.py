from django_filters import rest_framework as filters
from rest_framework import viewsets

from .filters import QuestionFilter
from .models import Question
from .serializers import QuestionSerializer

__all__ = (
    'QuestionViewSet',
)


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    pagination_class = None

    filter_backends = (filters.DjangoFilterBackend, )
    filterset_class = QuestionFilter
