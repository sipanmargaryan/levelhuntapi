from rest_framework import (
    filters, generics, parsers, permissions, status, viewsets, views
)
from rest_framework.response import Response

import skills.models
import universities.models
import questions.models
from admins.serializers import *  # noqa
from core.views.viewsets import MultiSerializerViewSetMixin

__all__ = (
    'CategoryViewSet',
    'UniversityViewSet',
    'SkillViewSet',
    'TopicViewSet',
    'ChangeOrderingAPIView',
    'QuestionAPIView',
    'AddQuestionAPIView',
    'EditQuestionAPIView',
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


class QuestionAPIView(views.APIView):
    permission_classes = (permissions.IsAdminUser, )

    # noinspection PyUnusedLocal
    def get(self, request):
        return Response({
            'levels': questions.models.Question.LEVELS,
            'skill': skills.models.Skill.objects.all().values('pk', 'name'),
        })


class AddQuestionAPIView(generics.GenericAPIView):
    serializer_class = QuestionCreateSerializer
    permission_classes = (permissions.IsAdminUser, )

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        question = serializer.save()
        data = serializer.validated_data
        questions.models.Option.attach_to_question(question, data['option_set'])
        return Response({'question_id': question.pk}, status=status.HTTP_201_CREATED)


class EditQuestionAPIView(generics.GenericAPIView):
    queryset = questions.models.Question.objects.all()
    serializer_class = QuestionCreateSerializer
    permission_classes = (permissions.IsAdminUser, )

    def put(self, request, *args, **kwargs):
        question = self.get_object()
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        question = serializer.update(question, serializer.validated_data)
        options = serializer.validated_data['option_set']

        old_options = questions.models.Option.objects.filter(question=question)
        existing_images = []
        for option in options:
            if 'option_id' in option:
                existing_images.append(option['option_id'])
                (
                    questions.models.Option.objects
                        .filter(pk=option['option_id'])
                        .update(option=option['option'], is_correct=option['is_correct'])
                )

        old_options.exclude(pk__in=existing_images).delete()

        new_options = [option for option in options if 'option_id' not in option]
        if len(new_options):
            questions.models.Option.attach_to_question(question, new_options)

        return Response({'question_id': question.pk}, status=status.HTTP_200_OK)