from rest_framework.routers import DefaultRouter

from django.urls import include, path

from .views import *  # noqa

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'universities', UniversityViewSet, basename='university')
router.register(r'skills', SkillViewSet, basename='skill')
router.register(r'skills/(?P<skill>\d+)/topics', TopicViewSet, basename='topic')

app_name = 'admins'
urlpatterns = [
    path('', include(router.urls)),
    path('change-ordering/', ChangeOrderingAPIView.as_view(), name='change_ordering'),
]
