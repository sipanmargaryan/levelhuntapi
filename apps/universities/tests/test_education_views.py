import pytest
from factory.fuzzy import FuzzyText

from django.apps import apps
from django.urls import reverse

from universities.factories import EducationFactory, UniversityFactory


@pytest.mark.django_db
def test_education_list(logged_in):
    EducationFactory.create_batch(10)
    EducationFactory.create_batch(10, user=logged_in.user)
    response = logged_in.client.get(reverse('universities:education'))

    assert response.status_code == 200

    response = response.json()
    fields = {'id', 'start_year', 'end_year', 'degree', 'field_of_study', 'university'}

    assert len(response) == 10
    assert set(response[0]) == fields


@pytest.mark.django_db
def test_education_detail(logged_in):
    EducationFactory.create_batch(10)
    education = EducationFactory.create(user=logged_in.user)
    response = logged_in.client.get(reverse('universities:education_detail', kwargs={'pk': education.pk}))

    assert response.status_code == 200

    response = response.json()
    fields = {'id', 'start_year', 'end_year', 'degree', 'field_of_study', 'description', 'university'}

    assert set(response) == fields


@pytest.mark.django_db
def test_education_create(logged_in):
    payload = dict(
        university_name=FuzzyText().fuzz(),
        start_year=1996,
        end_year=2000,
        degree='phd',
        field_of_study=FuzzyText().fuzz(),
        description=FuzzyText(length=500).fuzz(),
    )
    response = logged_in.client.post(reverse('universities:education'), payload)

    assert response.status_code == 201

    response = response.json()

    assert response['start_year'] == payload['start_year']
    assert response['end_year'] == payload['end_year']
    assert response['degree'] == payload['degree']
    assert response['field_of_study'] == payload['field_of_study']
    assert response['description'] == payload['description']

    assert apps.get_model('universities', 'Education').objects.filter(user=logged_in.user).count() == 1
    assert apps.get_model('universities', 'University').objects.filter(name=payload['university_name']).count() == 1


@pytest.mark.django_db
def test_education_put(logged_in):
    education = EducationFactory(user=logged_in.user)
    university = UniversityFactory()

    payload = dict(
        university_name=university.name,
        start_year=1996,
        end_year=2000,
        degree='phd',
        field_of_study=FuzzyText().fuzz(),
        description=FuzzyText(length=500).fuzz(),
    )

    response = logged_in.client.put(
        reverse('universities:education_detail', kwargs={'pk': education.pk}),
        data=payload,
        content_type='application/json',
    )
    education.refresh_from_db()

    assert response.status_code == 200

    assert education.university.pk == university.pk
    assert education.start_year == payload['start_year']
    assert education.end_year == payload['end_year']
    assert education.degree == payload['degree']
    assert education.field_of_study == payload['field_of_study']
    assert education.description == payload['description']


@pytest.mark.django_db
def test_education_delete(logged_in):
    education = EducationFactory(user=logged_in.user)

    response = logged_in.client.delete(reverse('universities:education_detail', kwargs={'pk': education.pk}))

    assert response.status_code == 204
    assert apps.get_model('universities', 'Education').objects.filter(user=logged_in.user).count() == 0
