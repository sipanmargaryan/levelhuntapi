import types
import os
import shutil

import pytest

from django.core.files.uploadedfile import SimpleUploadedFile

from core.testing import create_image
from users.factories import UserFactory


@pytest.fixture
def auth_user() -> UserFactory:
    """
    User with simple password.
    :return: UserFactory
    """
    user = UserFactory()
    user.set_password('password')
    user.save()

    return user


@pytest.fixture
def auth_admin() -> UserFactory:
    """
    SuperUser with simple password.
    :return: UserFactory
    """
    user = UserFactory(is_superuser=True, is_staff=True)
    user.set_password('password')
    user.save()

    return user


@pytest.fixture
def logged_in(client, auth_user) -> types.SimpleNamespace:
    """
    Client with already logged in user to make authenticated requests.
    :param client:
    :param auth_user:
    :return: dict
    """
    client.login(username=auth_user.username, password='password')

    result = types.SimpleNamespace()
    result.client = client
    result.user = auth_user

    return result


@pytest.fixture
def logged_in_admin(client, auth_admin) -> types.SimpleNamespace:
    """
    Client with already logged in user to make authenticated requests.
    :param client:
    :param auth_admin:
    :return: dict
    """
    client.login(username=auth_admin.username, password='password')

    result = types.SimpleNamespace()
    result.client = client
    result.user = auth_admin

    return result


@pytest.fixture
def image_file() -> callable:
    def create_image_file(filename='image.png'):
        image = create_image()
        return SimpleUploadedFile(filename, image.getvalue(), content_type='image/png')

    return create_image_file


def pytest_sessionfinish(session, exitstatus):
    shutil.rmtree(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'media/test'), ignore_errors=True)
