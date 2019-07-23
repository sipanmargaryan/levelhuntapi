import pytest

from django.apps import apps
from django.core.files import File
from django.urls import reverse
from django.utils import timezone

from core.testing import create_image
from core.utils.utils import build_client_absolute_url
from users.factories import SocialConnectionFactory, UserFactory
from users.models import User


@pytest.mark.django_db
def test_auth(client, auth_user):
    payload = dict(
        login=auth_user.username,
        password='password',
    )

    response = client.post(reverse('users:login'), payload)
    assert response.status_code == 200

    response = response.json()
    assert 'access_token' in response
    assert 'refresh_token' in response


@pytest.mark.django_db
def test_auth_invalid(client, auth_user):
    payload = dict(
        login='invalid login',
        password='invalid password',
    )

    response = client.post(reverse('users:login'), payload)
    assert response.status_code == 400

    payload = dict(
        login=auth_user.username,
        password='invalid password',
    )

    response = client.post(reverse('users:login'), payload)
    assert response.status_code == 400


@pytest.mark.django_db
def test_signup(client, mailoutbox, settings, monkeypatch):
    payload = dict(
        first_name='john',
        last_name='doe',
        email='mail@example.com',
        password='$2017$levelhunt%',
    )

    response = client.post(reverse('users:signup'), payload)
    assert response.status_code == 201

    assert len(mailoutbox) == 1

    msg = mailoutbox[0]

    assert msg.subject == 'Confirm your registration at {site_name}'.format(
        site_name=settings.SITE_NAME
    )
    assert msg.to == [payload['email']]

    user = User.objects.filter(email=payload['email']).first()
    email_confirmation_path = '/confirm/{token}'.format(
        token=user.email_confirmation_token
    )
    assert build_client_absolute_url(email_confirmation_path) in msg.body

    assert user.available_for_hire is True


@pytest.mark.django_db
def test_signup_invalid(client, auth_user):
    response = client.post(reverse('users:signup'), dict())
    assert response.status_code == 400
    response = response.json()

    assert response['email'] == ['This field is required.']
    assert response['password'] == ['This field is required.']
    assert response['first_name'] == ['This field is required.']
    assert response['last_name'] == ['This field is required.']

    payload = dict(
        email='invalid',
        password='password',
    )
    response = client.post(reverse('users:signup'), payload)
    assert response.status_code == 400
    response = response.json()

    assert response['password'] == ['This password is too common.']
    assert response['email'] == ['Enter a valid email address.']

    user = UserFactory()
    payload['email'] = user.email
    response = client.post(reverse('users:signup'), payload)
    assert response.status_code == 400
    response = response.json()

    assert response['email'] == ['A user with this email address is already exists.']


@pytest.mark.django_db
def test_email_confirmation(client):
    user = UserFactory(is_active=False, email_confirmation_token=User.generate_token())

    payload = dict(token=user.email_confirmation_token)

    response = client.post(reverse('users:confirm_email_address'), payload)
    user.refresh_from_db()

    assert response.status_code == 200
    response = response.json()
    assert response['user']['pk'] == user.pk
    assert 'access_token' in response
    assert 'refresh_token' in response
    assert user.email_confirmation_token is None
    assert user.is_active is True


@pytest.mark.django_db
def test_email_confirmation_invalid(client):
    UserFactory(is_active=False, email_confirmation_token=User.generate_token())

    payload = dict(token='invalid token')

    response = client.post(reverse('users:confirm_email_address'), payload)
    assert response.status_code == 400


@pytest.mark.django_db
def test_forgot_password(client, mailoutbox, settings):
    user = UserFactory()

    payload = dict(email=user.email)

    response = client.post(reverse('users:forgot_password'), payload)
    assert response.status_code == 200

    assert len(mailoutbox) == 1

    msg = mailoutbox[0]

    assert msg.subject == 'Reset your {site_name} password'.format(
        site_name=settings.SITE_NAME
    )
    assert msg.to == [payload['email']]

    user = User.objects.filter(email=user.email).first()
    reset_password_path = '/reset-password/{token}'.format(
        token=user.reset_password_token
    )

    assert build_client_absolute_url(reset_password_path) in msg.body


@pytest.mark.django_db
def test_forgot_password_invalid(client):
    payload = dict(email='email@example.com')

    response = client.post(reverse('users:forgot_password'), payload)
    assert response.status_code == 200

    user = UserFactory(is_active=False)
    payload = dict(email=user.email)

    response = client.post(reverse('users:forgot_password'), payload)
    assert response.status_code == 200


@pytest.mark.django_db
def test_forgot_password_availability(client):
    user = UserFactory(
        reset_password_token=User.generate_token(),
        reset_password_request_date=timezone.now(),
    )

    payload = dict(email=user.email)

    response = client.post(reverse('users:forgot_password'), payload)
    assert response.status_code == 400


@pytest.mark.django_db
def test_reset_password(client, mailoutbox, settings):
    user = UserFactory(
        is_active=False,
        reset_password_token=User.generate_token(),
        reset_password_request_date=timezone.now(),
    )

    new_password = user.reset_password_token
    payload = dict(
        token=user.reset_password_token,
        password=new_password,
    )

    response = client.post(reverse('users:reset_password'), payload)
    assert response.status_code == 200

    user.refresh_from_db()
    response = response.json()

    assert user.pk == response['user']['pk']
    assert user.is_active is True
    assert user.check_password(new_password) is True
    assert 'access_token' in response
    assert 'refresh_token' in response
    assert len(mailoutbox) == 1

    msg = mailoutbox[0]

    assert msg.subject == 'Your {site_name} password has been changed'.format(
        site_name=settings.SITE_NAME
    )
    assert msg.to == [user.email]


@pytest.mark.django_db
def test_reset_password_expired(client):
    user = UserFactory(
        reset_password_token=User.generate_token(),
        reset_password_request_date=timezone.now() - timezone.timedelta(minutes=5),
    )

    payload = dict(
        token=user.reset_password_token,
        password='password',
    )

    response = client.post(reverse('users:reset_password'), payload)
    assert response.status_code == 400


@pytest.mark.django_db
def test_reset_password_invalid_token(client):
    UserFactory(
        reset_password_token=User.generate_token(),
        reset_password_request_date=timezone.now(),
    )

    payload = dict(
        token='token',
        password='password',
    )

    response = client.post(reverse('users:reset_password'), payload)
    assert response.status_code == 400


@pytest.mark.django_db
def test_social_connect(client, monkeypatch):
    user = dict(
        provider_id=1,
        email='email@example.com',
        first_name='John',
        last_name='Doe',
        avatar_url='http://example.com',
    )
    monkeypatch.setattr('users.services.fb_retrieve_user', lambda token: user)
    monkeypatch.setattr('users.serializers.SocialConnectSerializer.save_avatar', lambda a, b, c: None)
    payload = dict(
        provider='facebook',
        access_token='token',
    )

    response = client.post(reverse('users:social_connect'), payload)
    assert response.status_code == 200

    response = response.json()
    assert 'access_token' in response
    assert 'refresh_token' in response
    assert response['user']['email'] == user['email']
    assert response['user']['first_name'] == user['first_name']
    assert response['user']['last_name'] == user['last_name']

    social_connection = apps.get_model('users', 'SocialConnection').objects.filter(
        provider_id=user['provider_id'], provider=user['provider'],
    )

    assert social_connection.count() == 1
    assert response['user']['email'] == social_connection.first().user.email


@pytest.mark.django_db
def test_social_connect_existing_email(client, monkeypatch):
    user = dict(
        provider_id=1,
        email='email@example.com',
        first_name='John',
        last_name='Doe',
        avatar_url='http://example.com',
    )
    UserFactory(email=user['email'])
    monkeypatch.setattr('users.services.fb_retrieve_user', lambda token: user)
    payload = dict(
        provider='facebook',
        access_token='token',
    )

    response = client.post(reverse('users:social_connect'), payload)
    assert response.status_code == 200

    response = response.json()
    assert 'access_token' in response
    assert 'refresh_token' in response
    assert response['user']['email'] == user['email']

    social_connection = apps.get_model('users', 'SocialConnection').objects.filter(
        provider_id=user['provider_id'], provider=user['provider'],
    )

    assert social_connection.count() == 1
    assert response['user']['email'] == social_connection.first().user.email


@pytest.mark.django_db
def test_social_connect_login(client, monkeypatch):
    social_connection = SocialConnectionFactory(provider='fb')
    user = dict(
        provider_id=social_connection.provider_id,
        email='email@example.com',
        first_name='John',
        last_name='Doe',
        avatar_url='http://example.com',
    )
    monkeypatch.setattr('users.services.fb_retrieve_user', lambda token: user)
    payload = dict(
        provider=social_connection.provider,
        access_token='token',
    )

    response = client.post(reverse('users:social_connect'), payload)
    assert response.status_code == 200

    response = response.json()
    assert 'access_token' in response
    assert 'refresh_token' in response
    assert response['user']['email'] == social_connection.user.email


@pytest.mark.django_db
def test_social_connect_invalid_data(client, monkeypatch):
    monkeypatch.setattr('users.services.fb_retrieve_user', lambda token: dict(error='test'))
    payload = dict(
        provider='facebook',
        access_token='token',
    )

    response = client.post(reverse('users:social_connect'), payload)
    assert response.status_code == 400

    assert response.json()['non_field_errors'] == ['test']


@pytest.mark.django_db
def test_social_connect_avatar(client, monkeypatch):
    user = dict(
        provider_id='test',
        email='email@example.com',
        first_name='John',
        last_name='Doe',
        avatar_url='http://example.com',
    )
    monkeypatch.setattr('users.services.fb_retrieve_user', lambda token: user)
    monkeypatch.setattr('core.utils.get_image_from_url', lambda url: File(create_image(), name='avatar.jpeg'))
    payload = dict(
        provider='facebook',
        access_token='token',
    )

    response = client.post(reverse('users:social_connect'), payload)
    assert response.status_code == 200
    assert response.json()['user']['avatar'].split('.')[-1] == 'jpeg'


@pytest.mark.django_db
def test_social_connect_avatar_without_extension(client, monkeypatch):
    user = dict(
        provider_id='test',
        email='email@example.com',
        first_name='John',
        last_name='Doe',
        avatar_url='http://example.com',
    )
    monkeypatch.setattr('users.services.fb_retrieve_user', lambda token: user)
    monkeypatch.setattr('core.utils.get_image_from_url', lambda url: File(create_image(), name='avatar'))
    payload = dict(
        provider='facebook',
        access_token='token',
    )

    response = client.post(reverse('users:social_connect'), payload)
    assert response.status_code == 200
    assert response.json()['user']['avatar'].split('.')[-1] == 'jpeg'
