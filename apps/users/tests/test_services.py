import pydash
import pytest

import users.services
from core.testing import response


def test_fb_retrieve_user(monkeypatch):
    access_token = 'token'
    api_response = {
        'id': '1',
        'picture': {'url': 'test'},
        'email': 'email@example.com',
        'first_name': 'John',
        'last_name': 'Doe',
    }

    def test_url(generated_url):
        facebook_url = users.services.FACEBOOK_API_URL
        facebook_url += 'me?fields=id,first_name,last_name,email,picture{url}'
        facebook_url += f'&access_token={access_token}'

        assert generated_url == facebook_url

        return response(200, api_response)

    monkeypatch.setattr('requests.get', test_url)

    user = users.services.fb_retrieve_user(access_token)

    assert user.get('provider_id') == api_response['id']
    assert user.get('email') == api_response['email']
    assert user.get('first_name') == api_response['first_name']
    assert user.get('last_name') == api_response['last_name']


def test_fb_retrieve_user_invalid(monkeypatch):
    monkeypatch.setattr(
        'requests.get',
        lambda url: response(400, {'error': {'message': 'Access Token is invalid!'}})
    )

    user = users.services.fb_retrieve_user('token')

    assert user.get('error') == 'Access Token is invalid!'


def test_go_retrieve_user(monkeypatch):
    access_token = 'token'
    api_response = {
        'id': '1',
        'picture': 'test',
        'email': 'email@example.com',
        'given_name': 'John',
        'family_name': 'Doe',
    }

    def test_url(generated_url, **kwargs):

        google_url = users.services.GOOGLE_API_URL
        google_url += 'oauth2/v2/userinfo'

        assert generated_url == google_url
        assert pydash.get(kwargs, 'headers.Authorization') == f'Bearer {access_token}'

        return response(200, api_response)

    monkeypatch.setattr('requests.get', test_url)

    user = users.services.go_retrieve_user(access_token)

    assert user.get('provider_id') == api_response['id']
    assert user.get('avatar_url') == api_response['picture']
    assert user.get('email') == api_response['email']
    assert user.get('first_name') == api_response['given_name']
    assert user.get('last_name') == api_response['family_name']


@pytest.mark.fuck
def test_go_retrieve_user_invalid(monkeypatch):
    monkeypatch.setattr(
        'requests.get',
        lambda url, **kwargs: response(400, {'error_description': 'Access Token is invalid!'})
    )

    user = users.services.go_retrieve_user('token')

    assert user.get('error') == 'Access Token is invalid!'
