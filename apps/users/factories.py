import factory

from django.contrib.auth import get_user_model

from users.models import SocialConnection


class UserFactory(factory.DjangoModelFactory):
    username = factory.Sequence(lambda n: 'user{}'.format(n))
    email = factory.LazyAttribute(lambda o: '{}@example.com'.format(o.username))
    is_active = True
    is_staff = False
    is_superuser = False

    class Meta:
        model = get_user_model()


class SocialConnectionFactory(factory.DjangoModelFactory):
    provider_id = factory.Sequence(lambda n: n)
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = SocialConnection
