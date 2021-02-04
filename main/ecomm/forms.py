from django import forms
from ecomm.models import User


class ProfileUserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(ProfileUserForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['email'].widget.attrs['readonly'] = True

    def clean_email(self):
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            return instance.email
        else:
            return self.cleaned_data['email']

    def send_email(self):
        pass
