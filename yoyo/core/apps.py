from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class YoYoCoreConfig(AppConfig):
    name = 'yoyo.core'
    label = 'yoyo_core'
    verbose_name = _('YoYo Core')
