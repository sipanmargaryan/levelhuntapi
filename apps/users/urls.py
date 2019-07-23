from rest_framework_simplejwt.views import TokenRefreshView

from django.urls import include, path

from .views import auth, user

auth_patterns = [
    path('login/', auth.LogInAPIView.as_view(), name='login'),
    path('signup/', auth.SignupAPIView.as_view(), name='signup'),
    path('confirm-email/', auth.ConfirmEmailAPIView.as_view(), name='confirm_email_address'),
    path('forgot-password/', auth.ForgotPasswordAPIView.as_view(), name='forgot_password'),
    path('reset-password/', auth.ResetPasswordAPIView.as_view(), name='reset_password'),
    path('refresh-token/', TokenRefreshView.as_view()),
    path('social-connect/', auth.SocialConnectAPIView.as_view(), name='social_connect'),
]

profile_patterns = [
    path(
        '',
        user.UserViewSet.as_view({
            'get': 'retrieve',
            'put': 'update',
        }),
        name='user'
    ),
    path('change-password/', user.ChangePasswordAPIView.as_view(), name='change_password'),
    path(
        'change-avatar/',
        user.ChangeAvatarViewSet.as_view({
            'post': 'update',
        }),
        name='change_avatar'
    ),
]

app_name = 'users'
urlpatterns = [
    path('auth/', include(auth_patterns)),
    path('profile/', include(profile_patterns)),
]
