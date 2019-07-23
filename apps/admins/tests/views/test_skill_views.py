import json

import pytest

from django.urls import reverse

from skills.factories import CategoryFactory, SkillFactory


@pytest.mark.django_db
def test_skill_create(logged_in_admin, image_file):
    category = CategoryFactory()
    payload = dict(
        name='JavaScript',
        logo=image_file('logo.png'),
        cover=image_file('cover.png'),
        categories=[category.pk]
    )
    response = logged_in_admin.client.post(
        reverse('admins:skill-list'),
        payload,
    )

    assert response.status_code == 201

    skill = response.json()
    assert skill['name'] == payload['name']
    assert skill['categories'] == [category.pk]
    assert skill['logo'].endswith('.png')
    assert skill['cover'].endswith('.png')


@pytest.mark.django_db
def test_skill_update(logged_in_admin, image_file):
    skill = SkillFactory()
    payload = dict(
        name='JavaScript',
    )
    response = logged_in_admin.client.put(
        reverse('admins:skill-detail', kwargs={'pk': skill.pk}),
        json.dumps(payload),
        content_type='application/json',
    )
    skill.refresh_from_db()

    assert response.status_code == 200
    assert skill.name == payload['name']


@pytest.mark.django_db
def test_skill_retrieve_list(logged_in_admin):
    skill = SkillFactory()
    response = logged_in_admin.client.get(reverse('admins:skill-detail', kwargs={'pk': skill.pk}))

    assert response.status_code == 200
    assert response.json()['name'] == skill.name

    SkillFactory.create_batch(10)

    response = logged_in_admin.client.get(reverse('admins:skill-list'))

    assert response.status_code == 200
    assert len(response.json()) == 11
