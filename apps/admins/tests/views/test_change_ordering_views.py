import pytest

from django.urls import reverse

from skills.factories import SkillFactory, TopicFactory


@pytest.mark.django_db
def test_change_ordering_view(logged_in_admin):
    skill1 = SkillFactory()
    skill2 = SkillFactory()
    payload = dict(
        item_id=skill1.pk,
        item_type='skill',
        ordering_number=2,
    )

    response = logged_in_admin.client.post(reverse('admins:change_ordering'), payload)
    skill1.refresh_from_db()
    skill2.refresh_from_db()

    assert response.status_code == 204
    assert skill1.ordering_number == 2
    assert skill2.ordering_number == 1

    topic1 = TopicFactory(skill=skill1)
    topic2 = TopicFactory(skill=skill1)

    payload = dict(
        item_id=topic1.pk,
        item_type='topic',
        ordering_number=2,
    )

    response = logged_in_admin.client.post(reverse('admins:change_ordering'), payload)
    topic1.refresh_from_db()
    topic2.refresh_from_db()

    assert response.status_code == 204
    assert topic1.ordering_number == 2
    assert topic2.ordering_number == 1


@pytest.mark.django_db
def test_change_ordering_view_not_found(logged_in_admin):
    payload = dict(
        item_id=1,
        item_type='skill',
        ordering_number=2,
    )

    response = logged_in_admin.client.post(reverse('admins:change_ordering'), payload)

    assert response.status_code == 400
    assert response.json()['non_field_errors'] == ['Item not found!']
