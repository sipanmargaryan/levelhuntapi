import json

import parse
import pytest

from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from core.testing import create_image
from skills.factories import SkillFactory
from users.models import User


@pytest.mark.django_db
def test_user_retrieve(logged_in):
    response = logged_in.client.get(reverse('users:user'))

    assert response.status_code == 200

    response = response.json()

    assert logged_in.user.username == response['username']
    assert 'title' in response


@pytest.mark.django_db
def test_user_update(logged_in):
    skill = SkillFactory()

    payload = dict(
        first_name='John',
        last_name='Doe',
        title='QA',
        available_for_hire=True,
        email_notification_settings=[
            dict(
                notification_type=User.NEWSLETTER,
                enabled=True,
            )
        ],
        skills_ids=[skill.id]
    )

    response = logged_in.client.put(reverse('users:user'), json.dumps(payload), content_type='application/json')

    assert response.status_code == 200

    response = response.json()

    assert payload['first_name'] == response['first_name']
    assert payload['last_name'] == response['last_name']
    assert payload['title'] == response['title']
    assert payload['available_for_hire'] == response['available_for_hire']
    assert response['email_notification_settings'][0]['enabled'] is True


@pytest.mark.django_db
def test_change_password(logged_in, mailoutbox, settings):
    payload = dict(
        old_password='password',
        new_password='$2017$levelhunt%',
    )

    response = logged_in.client.patch(
        reverse('users:change_password'), json.dumps(payload), content_type='application/json',
    )

    assert response.status_code == 200

    assert len(mailoutbox) == 1

    msg = mailoutbox[0]

    assert msg.subject == 'Your {site_name} password has been changed'.format(
        site_name=settings.SITE_NAME
    )
    assert msg.to == [logged_in.user.email]

    match = parse.search(
        '''Your password has been changed!''',
        msg.body,
    )
    assert match is not None


@pytest.mark.django_db
def test_change_password_invalid(logged_in):
    payload = dict(
        old_password='wrong',
        new_password='$2017$levelhunt%',
    )

    response = logged_in.client.patch(
        reverse('users:change_password'), json.dumps(payload), content_type='application/json',
    )

    assert response.status_code == 400

    payload['old_password'] = 'password'
    payload['new_password'] = 'password'

    response = logged_in.client.patch(
        reverse('users:change_password'), json.dumps(payload), content_type='application/json',
    )

    assert response.status_code == 400


@pytest.mark.django_db
def test_change_avatar(logged_in):
    avatar = create_image()
    avatar_file = SimpleUploadedFile('avatar.png', avatar.getvalue(), content_type='image/png')
    payload = dict(
        avatar=avatar_file
    )

    response = logged_in.client.post(reverse('users:change_avatar'), payload)
    logged_in.user.refresh_from_db()

    assert response.status_code == 200

    response = response.json()

    assert logged_in.user.avatar.url in response['avatar']


@pytest.mark.django_db
def test_change_avatar_delete(logged_in):
    response = logged_in.client.post(reverse('users:change_avatar'))

    assert response.status_code == 200

    response = response.json()

    assert response['avatar'] is None
