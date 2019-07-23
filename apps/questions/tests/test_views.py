import pytest

from django.urls import reverse

from questions.factories import QuestionFactory
from skills.factories import SkillFactory


@pytest.mark.django_db
def test_question_list(client):
    skill = SkillFactory()
    QuestionFactory.create_batch(5, skill=skill)
    response = client.get(f'{reverse("questions:question-list")}?skill_slug={skill.slug}')

    assert response.status_code == 200
    assert len(response.json()) == 5
