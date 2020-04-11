from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.utils.translation import ngettext
from .models import Coach, Specialization
from .forms import CoachAdminForm


@admin.register(Coach)
class CoachAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'get_bord_with_age', 'city')
    search_fields = ('first_name', 'second_name', 'last_name', 'city__alternate_names')
    autocomplete_fields = ['city']
    filter_horizontal = ('documents', 'specializations')
    fieldsets = (
        (_('Full name'), {
            'fields': ('last_name', 'first_name', 'second_name'),
        }),
        (_('Bio'), {
            'fields': ('born', 'city', 'specializations', 'hero_photo', 'main_photo'),
        }),
        (_('Documents'), {
            'fields': ('documents',),
        })
    )
    form = CoachAdminForm

    def get_bord_with_age(self, obj: Coach):
        age_label = ngettext('year', 'years', obj.age)
        born_date = str(obj.born)
        return f'{born_date} ({obj.age} {age_label})'
    get_bord_with_age.short_description = _('Born date')

    def get_full_name(self, obj: Coach):
        return obj.full_name
    get_full_name.short_description = _('Full name')


@admin.register(Specialization)
class SpecializationAdmin(admin.ModelAdmin):
    pass
