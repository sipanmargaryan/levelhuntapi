from django.urls import path

from . import views

app_name = 'universities'
urlpatterns = [
    path('', views.UniversityAPIView.as_view(), name='universities'),
    path(
        'education/',
        views.EducationViewSet.as_view({
            'get': 'list',
            'post': 'create',
        }),
        name='education'
    ),
    path(
        'education/<int:pk>/',
        views.EducationViewSet.as_view({
            'get': 'retrieve',
            'put': 'update',
            'delete': 'destroy',
        }),
        name='education_detail'
    ),
]
