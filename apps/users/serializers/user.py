from rest_framework import serializers

from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _

import users.fields
import users.models
import users.utils
from skills.models import Skill

__all__ = (
    'UserSerializer',
    'ChangePasswordSerializer',
    'ChangeAvatarSerializer',
)


class UserSkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ('id', 'name',)


class UserSerializer(serializers.ModelSerializer):
    email_notification_settings = users.fields.EmailSettingsField(source='*')
    skills = UserSkillSerializer(many=True, read_only=True)
    skills_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Skill.objects.all(),
        source='skills', write_only=True,
    )

    class Meta:
        model = users.models.User
        fields = (
            'username', 'first_name', 'last_name',
            'title', 'birthday', 'bio', 'available_for_hire',
            'email_notification_settings', 'skills', 'skills_ids',
        )
        extra_kwargs = {
            'username': {
                'read_only': True
            }
        }

    def update(self, instance, validated_data):

        instance.first_name = self.value_or_none(validated_data, 'first_name')
        instance.last_name = self.value_or_none(validated_data, 'last_name')
        instance.title = self.value_or_none(validated_data, 'title')
        instance.birthday = self.value_or_none(validated_data, 'birthday')
        instance.bio = self.value_or_none(validated_data, 'bio')
        instance.available_for_hire = validated_data.get('available_for_hire', False)
        instance.email_settings = validated_data.get('email_settings')
        instance.skills.set(validated_data.get('skills', []))
        instance.save()

        return instance

    @staticmethod
    def value_or_none(data, key):
        return data.get(key, None) or None


# noinspection PyAbstractClass
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField()

    def validate_old_password(self, value):
        if not self.context['user'].check_password(value):
            raise serializers.ValidationError(_('Invalid password.'))

        return value

    def validate_new_password(self, value):
        validate_password(value, self.context['user'])
        return value

    def change_password(self, password):
        user = self.context['user']
        user.set_password(password)
        user.save()

        users.utils.emails.send_change_password(user)

        return {
            'msg': _('Your password updated.')
        }


# noinspection PyAbstractClass
class ChangeAvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = users.models.User
        fields = ('avatar',)
