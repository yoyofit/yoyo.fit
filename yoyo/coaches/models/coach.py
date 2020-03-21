from PIL import Image
from datetime import date
from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from django.utils.translation import ngettext
from django.urls import reverse
from ..uploader import upload_hero_photo, upload_main_photo

class CoachManager(models.Manager):
    def filter_by_fio(self, fio: list):
        if len(fio) == 3:
            queryset = self.filter(
                last_name__istartswith=fio[0],
                first_name__istartswith=fio[1],
                second_name__istartswith=fio[2]
            )
            if not queryset.exists():
                queryset = self.filter(
                    last_name__istartswith=fio[0],
                    first_name__istartswith=fio[1],
                    second_name__istartswith=fio[2]
                )
                if not queryset.exists():
                    queryset = self.filter(
                        Q(first_name__istartswith=fio[0]) |
                        Q(last_name__istartswith=fio[0]) |
                        Q(second_name__istartswith=fio[0]) |
                        Q(first_name__istartswith=fio[1]) |
                        Q(last_name__istartswith=fio[1]) |
                        Q(second_name__istartswith=fio[1]) |
                        Q(first_name__istartswith=fio[2]) |
                        Q(last_name__istartswith=fio[2]) |
                        Q(second_name__istartswith=fio[2])
                    )
        elif len(fio) == 2:
            queryset = self.filter(last_name__istartswith=fio[0], first_name__istartswith=fio[1])
            if not queryset.exists():
                queryset = self.filter(last_name__istartswith=fio[1], first_name__istartswith=fio[0])
                if not queryset.exists():
                    queryset = self.filter(
                        Q(first_name__istartswith=fio[0]) |
                        Q(last_name__istartswith=fio[0]) |
                        Q(second_name__istartswith=fio[0]) |
                        Q(first_name__istartswith=fio[1]) |
                        Q(last_name__istartswith=fio[1]) |
                        Q(second_name__istartswith=fio[1])
                    )
        else:
            queryset = self.filter(
                Q(first_name__istartswith=fio[0]) |
                Q(last_name__istartswith=fio[0]) |
                Q(second_name__istartswith=fio[0])
            )
        return queryset.order_by('city__alternate_names', 'last_name', 'first_name', 'second_name')


class Coach(models.Model):
    first_name = models.CharField(_('First name'), max_length=60)
    last_name = models.CharField(_('Last name'), max_length=120)
    second_name = models.CharField(_('Second name'), max_length=60, null=True, blank=True)

    born = models.DateField(_('Born date'), null=True, blank=True)
    city = models.ForeignKey(
        'cities_light.City', on_delete=models.SET_NULL, blank=True, null=True, verbose_name=_('City')
    )

    specializations = models.ManyToManyField(
        'yoyo_coaches.Specialization', verbose_name=_('Specialization'), blank=True)
    documents = models.ManyToManyField('yoyo_institutes.Doc', verbose_name=_('Documents'), blank=True)

    hero_photo = models.ImageField(
        _('Big cover photo'),
        help_text=_('This photo does have a 1080x720px'),
        upload_to=upload_hero_photo,
        blank=True,
        null=True
    )
    main_photo = models.ImageField(
        _('Main photo'),
        upload_to=upload_main_photo,
        blank=True,
        null=True
    )

    objects = CoachManager()

    class Meta:
        verbose_name = _('Coach')
        verbose_name_plural = _('Coaches')

    def __str__(self):
        return self.full_name

    @property
    def full_name(self) -> str:
        full_name = []
        if self.second_name:
            full_name.append(self.second_name)
        if self.first_name:
            full_name.insert(0, self.first_name)
        if self.last_name:
            full_name.insert(0, self.last_name)
        return ' '.join(full_name)

    @property
    def age(self) -> int:
        today = date.today()
        return today.year - self.born.year - ((today.month, today.day) < (self.born.month, self.born.day))

    def get_age_display(self) -> str:
        text = ngettext('year', 'years', self.age)
        return '{} {}'.format(self.age, text)

    @property
    def city_name(self) -> str:
        return self.city.alternate_names.split(';')[-1]

    @property
    def city_name_with_region(self) -> str:
        city_name = self.city_name
        region_name = self.city.region.alternate_names.split(';')[-1]
        if city_name != region_name:
            return f'г. {city_name}, {region_name}'
        return f'г. {city_name}'

    def get_absolute_url(self) -> str:
        return reverse('yoyo:detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.hero_photo:
            img = Image.open(self.hero_photo.path)

            if img.width > 1080 or img.height > 720:
                new_image = (1080, 720)
                img.thumbnail(new_image)
                img.save(self.hero_photo.path)

        if self.main_photo:
            img = Image.open(self.main_photo.path)

            if img.width > 128 or img.height > 128:
                new_image = (128, 128)
                img.thumbnail(new_image)
                img.save(self.main_photo.path)
