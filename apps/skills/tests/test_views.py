import pytest

from django.urls import reverse

from skills.factories import SkillFactory, TopicFactory


@pytest.mark.django_db
def test_skill_list(client):
    SkillFactory.create_batch(5)
    response = client.get(reverse('skills:skill-list'))
    assert response.status_code == 200

    response = response.json()

    assert len(response['results']) == 5
    assert 'name' in response['results'][0]


@pytest.mark.django_db
def test_skill_detail(client):
    skill = SkillFactory.create()
    response = client.get(reverse('skills:skill-detail', kwargs={'pk': skill.pk}))
    assert response.status_code == 200

    response = response.json()

    assert 'name' in response


@pytest.mark.django_db
def test_topic_list(client):
    skill = SkillFactory.create()
    TopicFactory.create_batch(5, skill=skill)
    response = client.get('{}?skill_slug={}'.format(reverse('skills:topic-list'), skill.slug))
    assert response.status_code == 200

    response = response.json()

    assert len(response) == 5
    assert 'name' in response[0]


@pytest.mark.django_db
def test_topic_detail(client):
    skill = SkillFactory.create()
    topic = TopicFactory.create(skill=skill)
    response = client.get(
        '{}?skill_slug={}'.format(reverse('skills:topic-detail', kwargs={'pk': topic.pk}), skill.slug)
    )
    assert response.status_code == 200

    response = response.json()

    assert 'name' in response
