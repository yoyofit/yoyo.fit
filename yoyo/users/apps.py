from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class YoYoUsersConfig(AppConfig):
    name = 'yoyo.users'
    label = 'yoyo_users'
    verbose_name = _('Auth')
