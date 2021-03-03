from ckeditor.widgets import CKEditorWidget
from django import forms
from django.contrib import admin
from django.contrib.flatpages.admin import FlatPageAdmin as FlatPageAdminOriginal
from django.contrib.flatpages.admin import FlatpageForm as FlatpageFormOriginal
from django.contrib.flatpages.models import FlatPage

from ecomm.models import Characteristic, Category, CustomUser, Good, Image, Tag, Seller


class FlatpageForm(FlatpageFormOriginal):
    content = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = FlatPage
        fields = '__all__'


class FlatPageAdmin(FlatPageAdminOriginal):
    form = FlatpageForm


def make_published(modeladmin, request, queryset):
    for obj in queryset:
        if not obj.available:
            obj.available = True
        obj.save()


make_published.short_description = 'Make selected goods as published'


def make_saved_in_archive(modeladmin, request, queryset):
    for obj in queryset:
        if obj.available:
            obj.available = False
        obj.save()


make_published.short_description = 'Make selected goods as saved in archive'


class GoodAdmin(admin.ModelAdmin):
    date_hierarchy = 'pub_date'
    list_display = ('title', 'price', 'quantity', 'is_available', 'issue_date', 'tag')
    list_display_links = ('title', 'tag')
    list_editable = ('price', 'issue_date')
    list_filter = ('tag', )
    search_fields = ('title', )
    actions = [make_published, make_saved_in_archive]


admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageAdmin)
admin.site.register(Good, GoodAdmin)
