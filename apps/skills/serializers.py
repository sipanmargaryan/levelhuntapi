from rest_framework import serializers

from .models import Skill, Topic

__all__ = (
    'SkillSerializer',
    'TopicSerializer',
)


class SkillSerializer(serializers.ModelSerializer):

    class Meta:
        model = Skill
        fields = ('name', 'slug', 'logo', 'cover', )


class TopicSerializer(serializers.ModelSerializer):

    class Meta:
        model = Topic
        fields = ('name', 'slug', )
