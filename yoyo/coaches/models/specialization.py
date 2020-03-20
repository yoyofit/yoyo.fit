from django.db import models
from django.utils.translation import gettext_lazy as _


class Specialization(models.Model):
    name = models.CharField(_('Name'), max_length=160)

    class Meta:
        verbose_name = _('Specialization')
        verbose_name_plural = _('Specializations')
        ordering = ['name']

    def __str__(self):
        return self.name
