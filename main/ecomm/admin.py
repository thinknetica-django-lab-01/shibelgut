from django.contrib import admin
from django.contrib.flatpages.models import FlatPage
from django.contrib.flatpages.admin import FlatPageAdmin as FlatPageAdminOriginal
from django.contrib.flatpages.admin import FlatpageForm as FlatpageFormOriginal

from django import forms
from ckeditor.widgets import CKEditorWidget


class FlatpageForm(FlatpageFormOriginal):
    content = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = FlatPage
        fields = '__all__'


class FlatPageAdmin(FlatPageAdminOriginal):
    form = FlatpageForm


admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageAdmin)


