import re
from django.core.exceptions import ValidationError
from django.core.validators import validate_email as validate_email_content
from django.contrib.auth import get_user_model
from django.conf import settings
from django.utils.translation import ngettext, gettext_lazy as _

USERNAME_RE = re.compile(r'^[0-9a-z_]+$', re.IGNORECASE)

User = get_user_model()


# Username validators
def validate_username(value, exclude=None):
    validate_username_length(value)
    validate_username_content(value)
    validate_username_available(value, exclude)


def validate_username_available(value, exclude=None):
    try:
        user = User.objects.get_by_username(value)
        if not exclude or user.pk != exclude.pk:
            raise ValidationError(_('This username is not available.'))
    except User.DoesNotExist:
        pass


def validate_username_content(value):
    if not USERNAME_RE.match(value):
        raise ValidationError(
            _('Username can only contain latin alphabet letter, digits and low dash.')
        )


def validate_username_length(value):
    if len(value) < settings.YOYO_USERNAME['LENGTH']['MIN']:
        message = ngettext(
            'Username must be at least %(limit_value)s character long.',
            'Username must be at least %(limit_value)s characters long.',
            settings.YOYO_USERNAME['LENGTH']['MIN'],
        )
        raise ValidationError(message % {'limit_value': settings.YOYO_USERNAME['LENGTH']['MIN']})

    if len(value) > settings.YOYO_USERNAME['LENGTH']['MAX']:
        message = ngettext(
            'Username cannot be longer than %(limit_value)s characters.',
            'Username cannot be longer than %(limit_value)s characters.',
            settings.YOYO_USERNAME['LENGTH']['MAX']
        )
        raise ValidationError(message % {'limit_value': settings.YOYO_USERNAME['LENGTH']['MAX']})


# E-mail validators
def validate_email(value, exclude=None):
    validate_email_content(value)
    validate_username_available(value, exclude)


def validate_email_available(value, exclude=None):
    try:
        user = User.objects.get_by_email(value)
        if not exclude or user.pk != exclude.pk:
            raise ValidationError(_('This e-mail address is not available.'))
    except User.DoesNotExist:
        pass

