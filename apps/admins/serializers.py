from rest_framework import serializers

from django.db import models
from django.utils.functional import lazy

import skills.models
import universities.models
from core.models.models import AbstractOrderingModel

__all__ = (
    'CategorySerializer',
    'UniversitySerializer',
    'SkillListSerializer',
    'SkillSerializer',
    'TopicSerializer',
    'ChangeOrderingSerializer',
)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = skills.models.Category
        fields = ('pk', 'name', 'skills', )
        read_only_fields = ('pk', 'skills', )


class UniversitySerializer(serializers.ModelSerializer):
    class Meta:
        model = universities.models.University
        fields = '__all__'
        read_only_fields = ('additional_data', )
        extra_kwargs = {
            'logo_url': {'allow_null': True},
            'keywords': {'allow_null': True},
        }


class SkillListSerializer(serializers.ModelSerializer):
    class Meta:
        model = skills.models.Skill
        fields = ('pk', 'name', 'slug', 'logo')


class SkillSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super(SkillSerializer, self).__init__(*args, **kwargs)
        if self.instance and not kwargs.get('partial'):
            self.fields['logo'].required = False
            self.fields['cover'].required = False

    class Meta:
        model = skills.models.Skill
        fields = '__all__'
        extra_kwargs = {
            'description': {'allow_null': True},
            'keywords': {'allow_null': True},
        }


class TopicSerializer(serializers.ModelSerializer):
    skill_name = serializers.CharField(source='skill.name', read_only=True)

    class Meta:
        model = skills.models.Topic
        exclude = ('slug', 'skill', )

    def validate(self, attrs):
        if not self.context['skill']:
            raise serializers.ValidationError('Skill not found.')
        return attrs

    def create(self, validated_data):
        validated_data['skill'] = self.context['skill']
        return self.Meta.model.objects.create(**validated_data)


# noinspection PyAbstractClass
class ChangeOrderingSerializer(serializers.Serializer):
    ordering_number = serializers.IntegerField(min_value=1)
    item_id = serializers.IntegerField()
    item_type = serializers.ChoiceField(
        choices=lazy(AbstractOrderingModel.as_choices, tuple)(),
    )

    def validate(self, attrs):
        attrs['model'] = self.fields['item_type'].choices.get(attrs['item_type'])

        try:
            attrs['item'] = attrs['model'].objects.get(pk=attrs['item_id'])
        except models.ObjectDoesNotExist:
            raise serializers.ValidationError('Item not found!')

        return attrs

    def move(self):
        item = self.validated_data.get('item')
        model = self.validated_data['model']
        model.objects.move(
            item=item,
            ordering_number=self.validated_data['ordering_number'],
        )
