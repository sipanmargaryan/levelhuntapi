from rest_framework.routers import DefaultRouter

from django.urls import include, path

from .views import SkillViewSet, TopicViewSet

router = DefaultRouter()
router.register(r'skills', SkillViewSet, basename='skill')
router.register(r'topics', TopicViewSet, basename='topic')


app_name = 'skills'
urlpatterns = [
    path('', include(router.urls)),
]
