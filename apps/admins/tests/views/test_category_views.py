import json

import pytest

from django.urls import reverse

from skills.factories import CategoryFactory


@pytest.mark.django_db
def test_category_create(logged_in_admin):
    payload = dict(name='Database')
    response = logged_in_admin.client.post(
        reverse('admins:category-list'),
        payload,
    )

    assert response.status_code == 201

    category = response.json()
    assert category['name'] == payload['name']
    assert category['skills'] == 0

    response = logged_in_admin.client.post(
        reverse('admins:category-list'),
        payload,
    )

    assert response.status_code == 400
    assert 'name' in response.json().keys()


@pytest.mark.django_db
def test_category_update(logged_in_admin):
    category = CategoryFactory()
    payload = dict(name='Database')
    response = logged_in_admin.client.put(
        reverse('admins:category-detail', kwargs={'pk': category.pk}),
        json.dumps(payload),
        content_type='application/json',
    )
    category.refresh_from_db()

    assert response.status_code == 200
    assert category.name == payload['name']
    assert response.json()['name'] == payload['name']


@pytest.mark.django_db
def test_category_retrieve_list(logged_in_admin):
    category = CategoryFactory()
    response = logged_in_admin.client.get(reverse('admins:category-detail', kwargs={'pk': category.pk}))

    assert response.status_code == 200
    assert response.json()['name'] == category.name

    CategoryFactory.create_batch(10)

    response = logged_in_admin.client.get(reverse('admins:category-list'))

    assert response.status_code == 200
    assert len(response.json()['results']) == 11
