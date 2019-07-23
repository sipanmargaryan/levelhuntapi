import json

import pytest

from django.urls import reverse

from universities.factories import UniversityFactory


@pytest.mark.django_db
def test_university_create(logged_in_admin):
    payload = dict(name='NPUA')
    response = logged_in_admin.client.post(
        reverse('admins:university-list'),
        payload,
    )

    assert response.status_code == 201

    university = response.json()
    assert university['name'] == payload['name']

    response = logged_in_admin.client.post(
        reverse('admins:university-list'),
        payload,
    )

    assert response.status_code == 400
    assert 'name' in response.json().keys()


@pytest.mark.django_db
def test_university_update(logged_in_admin):
    university = UniversityFactory(keywords='test')
    payload = dict(name='NPUA', keywords=None)
    response = logged_in_admin.client.put(
        reverse('admins:university-detail', kwargs={'pk': university.pk}),
        json.dumps(payload),
        content_type='application/json',
    )
    university.refresh_from_db()

    assert response.status_code == 200
    assert university.name == payload['name']
    assert university.keywords == payload['keywords']
    assert response.json()['name'] == payload['name']
    assert response.json()['keywords'] == payload['keywords']


@pytest.mark.django_db
def test_university_retrieve_list(logged_in_admin):
    university = UniversityFactory()
    response = logged_in_admin.client.get(reverse('admins:university-detail', kwargs={'pk': university.pk}))

    assert response.status_code == 200
    assert response.json()['name'] == university.name

    UniversityFactory.create_batch(10)

    response = logged_in_admin.client.get(reverse('admins:university-list'))

    assert response.status_code == 200
    assert len(response.json()['results']) == 11
