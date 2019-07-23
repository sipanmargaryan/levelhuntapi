from django_filters import rest_framework as filters

from core.views.viewsets import SafeModelViewSet

from .filters import TopicFilter
from .models import Skill, Topic
from .serializers import SkillSerializer, TopicSerializer

__all__ = (
    'SkillViewSet',
    'TopicViewSet',
)


class SkillViewSet(SafeModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer


class TopicViewSet(SafeModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    pagination_class = None

    filter_backends = (filters.DjangoFilterBackend, )
    filterset_class = TopicFilter
