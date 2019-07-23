from rest_framework_swagger.views import get_swagger_view

from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

schema_view = get_swagger_view(title='LevelHunt API')


urlpatterns = [
    path('skills/', include('skills.urls', namespace='skills')),
    path('questions/', include('questions.urls', namespace='questions')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('users/', include('users.urls', namespace='users')),
    path('universities/', include('universities.urls', namespace='universities')),
    path('admins/', include('admins.urls', namespace='admins')),
]

if settings.DEBUG:
    urlpatterns.insert(0, path('', schema_view))
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.ENABLE_DEBUG_TOOLBAR:
    import debug_toolbar

    urlpatterns += [
        path('__debug__', include(debug_toolbar.urls)),
    ]
