import factory

from questions.models import Question
from skills.factories import SkillFactory


class QuestionFactory(factory.DjangoModelFactory):
    skill = factory.SubFactory(SkillFactory)

    class Meta:
        model = Question
