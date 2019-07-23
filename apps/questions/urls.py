from rest_framework.routers import DefaultRouter

from django.urls import include, path

from .views import QuestionViewSet

router = DefaultRouter()
router.register(r'questions', QuestionViewSet, basename='question')


app_name = 'questions'
urlpatterns = [
    path('', include(router.urls)),
]
