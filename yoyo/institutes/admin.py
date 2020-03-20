from django.contrib import admin
from .models import Institute, Doc


@admin.register(Institute)
class InstituteAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'type')
    list_filter = ('type',)
    search_fields = ('name',)
    autocomplete_fields = ('city',)


@admin.register(Doc)
class DocAdmin(admin.ModelAdmin):
    list_display = ('number', 'doc_type', 'institute', 'date_of_issue', 'added_at', 'added_by')
    list_filter = ('institute', 'doc_type')
    search_fields = ('number',)
    autocomplete_fields = ('institute',)
