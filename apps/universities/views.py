from django_filters import rest_framework as filters
from rest_framework import generics, permissions, viewsets

from universities.filters import UniversityFilter
from universities.models import Education, University
from universities.serializers import EducationSerializer, UniversitySerializer

__all__ = (
    'UniversityAPIView',
    'EducationViewSet',
)


class UniversityAPIView(generics.ListAPIView):
    serializer_class = UniversitySerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = UniversityFilter

    def get_queryset(self):
        return University.objects.filter(is_verified=True)


class EducationViewSet(viewsets.ModelViewSet):
    queryset = Education.objects.all()
    serializer_class = EducationSerializer
    permission_classes = (permissions.IsAuthenticated, )
    pagination_class = None

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
