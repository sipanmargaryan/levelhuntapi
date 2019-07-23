import pydash
import requests

FACEBOOK_API_URL = 'https://graph.facebook.com/v3.2/'
GOOGLE_API_URL = 'https://www.googleapis.com/'


__all__ = (
    'fb_retrieve_user',
    'go_retrieve_user',
)


def fb_retrieve_user(access_token: str) -> dict:
    """
    Retrieve facebook user information
    :param access_token:
    :return: dict
    """
    fields = 'id', 'first_name', 'last_name', 'email', 'picture{url}'
    endpoint = 'me?fields={}'.format(','.join(fields))
    endpoint += f'&access_token={access_token}'

    response = requests.get(FACEBOOK_API_URL + endpoint)

    if response.status_code == 200:
        user = response.json()
        result = dict(
            provider_id=user['id'],
            email=user.get('email', f'{user["id"]}@facebook.com'),
            avatar_url=f'https://graph.facebook.com/{user["id"]}/picture?width=250',
            first_name=user['first_name'],
            last_name=user['last_name'],
        )
    else:
        result = dict(error=pydash.get(response.json(), 'error.message'))

    return result


def go_retrieve_user(access_token: str) -> dict:
    """
    Retrieve google user information
    :param access_token:
    :return: dict
    """
    endpoint = 'oauth2/v2/userinfo'

    response = requests.get(
        GOOGLE_API_URL + endpoint,
        headers={'Authorization': f'Bearer {access_token}'},
    )

    if response.status_code == 200:
        user = response.json()
        result = dict(
            provider_id=user['id'],
            email=user['email'],
            avatar_url=user['picture'],
            first_name=user['given_name'],
            last_name=user['family_name'],
        )
    else:
        result = dict(error=response.json().get('error_description', None))

    return result
