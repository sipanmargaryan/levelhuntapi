import random

import factory

from django.utils import timezone

from users.factories import UserFactory

from .models import Education, University


class UniversityFactory(factory.DjangoModelFactory):
    name = factory.Sequence(lambda n: f'university-{n}')

    class Meta:
        model = University


class EducationFactory(factory.DjangoModelFactory):
    start_year = factory.LazyFunction(lambda: random.choice(range(1900, timezone.now().year)))
    university = factory.SubFactory(UniversityFactory)
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = Education
