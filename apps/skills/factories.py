import factory

from .models import Category, Skill, Topic


class CategoryFactory(factory.DjangoModelFactory):
    name = factory.Sequence(lambda n: 'category-{}'.format(n))

    class Meta:
        model = Category


class SkillFactory(factory.DjangoModelFactory):
    name = factory.Sequence(lambda n: 'skill-{}'.format(n))

    class Meta:
        model = Skill


class TopicFactory(factory.DjangoModelFactory):
    name = factory.Sequence(lambda n: 'topic-{}'.format(n))
    skill = factory.SubFactory(SkillFactory)

    class Meta:
        model = Topic
