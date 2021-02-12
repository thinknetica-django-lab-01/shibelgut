from django.contrib import admin
from django.contrib.flatpages.models import FlatPage
from django.contrib.flatpages.admin import FlatPageAdmin as FlatPageAdminOriginal
from django.contrib.flatpages.admin import FlatpageForm as FlatpageFormOriginal
from django.contrib.auth.models import Group, User
from django.db.models.signals import post_save
from django.dispatch import receiver

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


@receiver(post_save, sender=User)
def create_user(sender, instance, **kwargs):
    common_users_group, created = Group.objects.get_or_create(name='Common Users')
    common_users_group.user_set.add(instance)
