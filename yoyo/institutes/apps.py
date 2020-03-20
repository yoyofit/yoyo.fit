from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class YoYoInstitutesConfig(AppConfig):
    name = 'yoyo.institutes'
    label = 'yoyo_institutes'
    verbose_name = _('Institutes')

    def ready(self):
        import yoyo.institutes.signals
