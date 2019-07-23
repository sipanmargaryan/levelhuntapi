import json

import pytest

from django.urls import reverse

from skills.factories import SkillFactory, TopicFactory


@pytest.mark.django_db
def test_topic_create(logged_in_admin):
    skill = SkillFactory()
    payload = dict(
        name='Functions',
    )
    response = logged_in_admin.client.post(
        reverse('admins:topic-list', kwargs={'skill': skill.pk}),
        payload,
    )

    assert response.status_code == 201

    topic = response.json()
    assert topic['skill_name'] == skill.name
    assert topic['name'] == payload['name']


@pytest.mark.django_db
def test_topic_update(logged_in_admin):
    topic = TopicFactory()
    payload = dict(
        name='Functions',
    )
    response = logged_in_admin.client.put(
        reverse('admins:topic-detail', kwargs={'skill': topic.skill.pk, 'pk': topic.pk}),
        json.dumps(payload),
        content_type='application/json',
    )
    topic.refresh_from_db()

    assert response.status_code == 200
    assert topic.name == payload['name']


@pytest.mark.django_db
def test_topic_retrieve_list(logged_in_admin):
    topic = TopicFactory()
    response = logged_in_admin.client.get(
        reverse('admins:topic-detail', kwargs={'skill': topic.skill.pk, 'pk': topic.pk})
    )

    assert response.status_code == 200
    assert response.json()['name'] == topic.name

    skill = SkillFactory()
    TopicFactory.create_batch(10, skill=skill)
    TopicFactory.create_batch(10)

    response = logged_in_admin.client.get(reverse('admins:topic-list', kwargs={'skill': skill.pk}))

    assert response.status_code == 200
    assert len(response.json()) == 10
