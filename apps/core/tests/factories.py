import factory

from .testing_models import Child, Parent


class ParentFactory(factory.DjangoModelFactory):
    class Meta:
        model = Parent


class ChildFactory(factory.DjangoModelFactory):
    parent = factory.SubFactory(ParentFactory)

    class Meta:
        model = Child
