from rest_framework import serializers

from .models import Option, Question

__all__ = (
    'OptionSerializer',
    'QuestionSerializer',
)


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ('id', 'option', )


class QuestionSerializer(serializers.ModelSerializer):
    options = OptionSerializer(source='option_set', many=True)

    class Meta:
        model = Question
        fields = ('question', 'options', )
