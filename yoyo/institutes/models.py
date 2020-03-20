from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .uploader import upload_logo


class Institute(models.Model):
    COLLEGE = 1
    VOCATIONAL = 2
    COURSES = 3

    TYPES_CHOICES = (
        (COLLEGE, _('College/Academy')),
        (VOCATIONAL, _('Vocational school')),
        (COURSES, _('Courses')),
    )

    name = models.CharField(_('Name'), max_length=255)
    logo = models.ImageField(_('Logo'), upload_to=upload_logo, null=True, blank=True)
    city = models.ForeignKey(
        'cities_light.City', on_delete=models.SET_NULL, blank=True, null=True, verbose_name=_('City')
    )
    type = models.PositiveSmallIntegerField(_('Type of institution'), choices=TYPES_CHOICES, default=COLLEGE)

    class Meta:
        verbose_name = _('Institute')
        verbose_name_plural = _('Institutes')

    def __str__(self):
        return self.name


class Doc(models.Model):
    DIPLOMA = 1
    CERTIFICATE = 2

    DOC_TYPES_CHOICES = (
        (DIPLOMA, _('Diploma')),
        (CERTIFICATE, _('Certificate'))
    )

    number = models.CharField(_('Document number'), max_length=60, null=True, blank=True)
    institute = models.ForeignKey(Institute, on_delete=models.CASCADE, verbose_name=_('Institute'))
    doc_type = models.PositiveSmallIntegerField(_('Document type'), choices=DOC_TYPES_CHOICES, default=DIPLOMA)
    annotate = models.TextField(_('Document annotate'), null=True, blank=True)
    date_of_issue = models.DateField(_('Date of issue'))
    added_at = models.DateTimeField(_('Added at'), default=timezone.now)
    added_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='+',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('Added by')
    )

    class Meta:
        verbose_name = _('Document')
        verbose_name_plural = _('Documents')
        ordering = ['-added_at']

    def __str__(self):
        issue_by = str(self.date_of_issue)
        return f'{self.get_doc_type_display()} #{self.number} issue by {issue_by}'
