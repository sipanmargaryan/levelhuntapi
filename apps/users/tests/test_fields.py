import pytest

from users.fields import EmailSettingsField


@pytest.mark.parametrize(
    'arg, return_value', [
        (None, None),
        (str(), None),
        (dict(), None),
        (dict(notification_type='invalid'), None),
    ]
)
def test_email_settings_field(arg, return_value):
    field = EmailSettingsField()

    assert field.process_setting(arg) is return_value
