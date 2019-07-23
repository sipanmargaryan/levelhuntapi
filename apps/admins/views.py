from rest_framework import (
    filters, generics, parsers, permissions, status, viewsets
)
from rest_framework.response import Response

import skills.models
import universities.models
from admins.serializers import *  # noqa
from core.views.viewsets import MultiSerializerViewSetMixin

__all__ = (
    'CategoryViewSet',
    'UniversityViewSet',
    'SkillViewSet',
    'TopicViewSet',
    'ChangeOrderingAPIView',
)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = skills.models.Category.objects.prefetch_related('skill_set')
    serializer_class = CategorySerializer
    permission_classes = (permissions.IsAdminUser, )
    ordering = ['name']


class UniversityViewSet(viewsets.ModelViewSet):
    queryset = universities.models.University.objects.all()
    serializer_class = UniversitySerializer
    permission_classes = (permissions.IsAdminUser, )
    parser_classes = (parsers.MultiPartParser, parsers.JSONParser)
    ordering = ['name']


class SkillViewSet(MultiSerializerViewSetMixin, viewsets.ModelViewSet):
    queryset = skills.models.Skill.objects.all()
    serializer_class = SkillSerializer
    serializer_action_classes = {
        'list': SkillListSerializer,
    }
    permission_classes = (permissions.IsAdminUser, )
    parser_classes = (parsers.MultiPartParser, parsers.JSONParser)
    filter_backends = (filters.OrderingFilter, )
    ordering = ('ordering_number', )
    pagination_class = None


class TopicViewSet(viewsets.ModelViewSet):
    queryset = skills.models.Topic.objects.select_related('skill')
    serializer_class = TopicSerializer
    permission_classes = (permissions.IsAdminUser, )
    filter_backends = (filters.OrderingFilter,)
    ordering = ('ordering_number', )
    pagination_class = None

    def get_queryset(self):
        return super(TopicViewSet, self).get_queryset().filter(skill=self.kwargs['skill'])

    def get_serializer_context(self):
        context = super(TopicViewSet, self).get_serializer_context()

        if self.kwargs.get('skill'):
            context['skill'] = skills.models.Skill.objects.filter(pk=self.kwargs['skill']).first()

        return context


class ChangeOrderingAPIView(generics.GenericAPIView):
    serializer_class = ChangeOrderingSerializer
    permission_classes = (permissions.IsAdminUser, )

    # noinspection PyUnusedLocal
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)
        serializer.move()

        return Response(status=status.HTTP_204_NO_CONTENT)
