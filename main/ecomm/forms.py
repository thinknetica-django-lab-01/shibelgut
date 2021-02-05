from django import forms
from ecomm.models import User
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


class ProfileUserForm(forms.ModelForm):

    validate_numeric = RegexValidator(regex='^[0-9]*$', message='Use only digits')

    age = forms.CharField(max_length=2, required=True, validators=[validate_numeric])
    age.widget.attrs.update({'class': 'form-control'})

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

    def clean_age(self):
        new_age = self.cleaned_data['age']
        if int(new_age) < 18:
            raise ValidationError('You must be 18 or older')
        return new_age

    def send_email(self):
        pass
