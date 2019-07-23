import pytest

from django.urls import reverse

from universities.factories import UniversityFactory


@pytest.mark.django_db
def test_universities(logged_in):
    UniversityFactory.create_batch(11, is_verified=False)
    UniversityFactory.create_batch(12, is_verified=True)
    response = logged_in.client.get(reverse('universities:universities'))

    assert response.status_code == 200
    response = response.json()

    assert response['count'] == 12
    assert len(response['results']) == 12


@pytest.mark.django_db
def test_universities_filter(logged_in):
    UniversityFactory(name='Engineering University of Armenia', is_verified=True, keywords='Armenia Հայաստան')
    UniversityFactory(name='American University of Armenia', is_verified=True, keywords='Armenia Հայաստան')
    UniversityFactory(name='Medical Institute of Armenia', is_verified=True, keywords='Armenia Հայաստան')

    response = logged_in.client.get('{}?q={}'.format(reverse('universities:universities'), 'հայաստան'))

    assert response.status_code == 200
    response = response.json()

    assert len(response['results']) == 3

    response = logged_in.client.get('{}?q={}'.format(reverse('universities:universities'), 'medical'))
    response = response.json()

    assert len(response['results']) == 1

    response = logged_in.client.get('{}?q={}'.format(
        reverse('universities:universities'),
        'Engineering University of Armenia',
    ))
    response = response.json()

    assert len(response['results']) == 1
