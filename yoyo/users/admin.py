from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'full_name', 'joined_on', 'joined_from_ip')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'second_name')

    def full_name(self, obj: User):
        return obj.get_full_name
    full_name.short_description = _('Full name')
