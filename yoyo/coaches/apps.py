from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class YoYoCoachesConfig(AppConfig):
    name = 'yoyo.coaches'
    label = 'yoyo_coaches'
    verbose_name = _('Coaches')
