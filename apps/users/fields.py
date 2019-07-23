from rest_framework import serializers

from users.models import User


class EmailSettingsField(serializers.Field):

    def to_representation(self, obj):
        return obj.get_email_settings()

    def to_internal_value(self, settings):
        settings = filter(lambda s: s is not None, {self.process_setting(s) for s in settings})

        return {
            'email_settings': list(settings)
        }

    @staticmethod
    def process_setting(setting):
        if type(setting) is not dict:
            return None

        notification_type = setting.get('notification_type', None)
        enabled = setting.get('enabled', False)

        if not notification_type:
            return None

        if notification_type not in User.NOTIFICATION_CHOICES_DICT:
            return None

        if enabled:
            return notification_type
