from datetime import date
from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _


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
