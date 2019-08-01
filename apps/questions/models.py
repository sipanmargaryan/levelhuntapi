from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models.models import AbstractStatusModel

__all__ = (
    'Question',
    'Option',
)


class Question(AbstractStatusModel):

    EASY = 1000
    L_INTERMEDIATE = 2000
    INTERMEDIATE = 3000
    U_INTERMEDIATE = 4000
    DIFFICULT = 5000

    LEVELS = (
        (EASY, _('Easy')),
        (L_INTERMEDIATE, _('Lower Intermediate')),
        (INTERMEDIATE, _('Intermediate')),
        (U_INTERMEDIATE, _('Upper Intermediate')),
        (DIFFICULT, _('Difficult')),
    )

    question = models.CharField(max_length=200)
    note = models.TextField(null=True)
    description = models.TextField(null=True)
    level = models.IntegerField(choices=LEVELS, default=INTERMEDIATE)

    skill = models.ForeignKey('skills.Skill', on_delete=models.CASCADE)
    submitted_by = models.ForeignKey('users.User', null=True, related_name='submitted_by+', on_delete=models.SET_NULL)
    accepted_by = models.ForeignKey('users.User', null=True, related_name='accepted_by+', on_delete=models.SET_NULL)

    topics = models.ManyToManyField('skills.Topic', blank=True)

    def __str__(self):  # pragma: no cover
        return self.question


class Option(models.Model):
    option = models.TextField()
    is_correct = models.BooleanField(default=False)

    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):  # pragma: no cover
        return self.option

    @classmethod
    def attach_to_question(cls, question, options):
        option_data = dict(
            question=question
        )
        options_list = []
        for option in options:
            for key, value in option.items():
                option_data[key] = value
            options_list.append(cls(**option_data))
        cls.objects.bulk_create(options_list)

