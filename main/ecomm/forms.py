from django import forms
from ecomm.models import User, Good, Image, Characteristic
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.forms.models import inlineformset_factory

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset


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


class LoginForm(forms.ModelForm):

    email = forms.EmailInput()
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email', 'password']

    # widgets = {
    #     'email': forms.TextInput(attrs={'class': 'form-control'}),
    #     'password': forms.PasswordInput(attrs={'class': 'form-control'}),
    # }


class GoodCreateForm(forms.ModelForm):
    validate_numeric = RegexValidator(regex='^[0-9]*$', message='Use only digits')
    validate_alpha = RegexValidator(regex='^[a-zA-Z]*$', message='Use only letters')

    price = forms.DecimalField(required=True, validators=[validate_numeric])
    brand = forms.CharField(required=True, validators=[validate_alpha])
    quantity = forms.IntegerField(min_value=0, required=True, validators=[validate_numeric])
    issue_date = forms.DateField(required=True)
    vendor_code = forms.CharField(required=True, validators=[validate_numeric, validate_alpha])
    # tag = forms.ComboField()

    price.widget.attrs.update({'class': 'form-control'})
    brand.widget.attrs.update({'class': 'form-control'})
    quantity.widget.attrs.update({'class': 'form-control'})
    issue_date.widget.attrs.update({'class': 'form-control'})
    vendor_code.widget.attrs.update({'class': 'form-control'})

    # tag.widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Good
        exclude = ['pub_date', 'seller', 'rating']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            # 'brand': forms.TextInput(attrs={'class': 'form-control'}),
            # 'quantity': forms.TextInput(attrs={'class': 'form-control'}),
            # 'issue_date': forms.DateField(attrs={'class': 'form-control'}),
            # 'vendor_code': forms.TextInput(attrs={'class': 'form-control'}),
            # 'tag': forms.TextInput(attrs={'class': 'form-control'}),
        }

    @property
    def helper(self):
        helper = FormHelper()
        helper.form_tag = False

        helper.layout = Layout(Fieldset('Create a new good', 'title', 'price', 'description', 'brand', 'quantity',
                                        'issue_date', 'vendor_code', 'tag'), )

        return helper


class CharacteristicFormHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(CharacteristicFormHelper, self).__init__(*args, **kwargs)
        self.form_tag = False
        self.layout = Layout(Fieldset('Add the good characteristics', 'color', 'size', 'length', 'width', 'height'), )


class ImageFormHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(ImageFormHelper, self).__init__(*args, **kwargs)
        self.form_tag = False
        self.layout = Layout(Fieldset('Add the good images', 'image_1', 'image_2', 'image_3', 'image_4', 'image_5'), )


CharacteristicFormset = inlineformset_factory(Good, Characteristic, exclude=('good', ), can_delete=False, extra=1)
ImageFormset = inlineformset_factory(Good, Image, exclude=('good', ), can_delete=False, extra=1)


class GoodUpdateForm(forms.ModelForm):
    class Meta:
        model = Good
        exclude = ['seller', 'rating']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'brand': forms.TextInput(attrs={'class': 'form-control'}),
            'quantity': forms.TextInput(attrs={'class': 'form-control'}),
            # 'issue_date': forms.DateField(attrs={'class': 'form-control'}),
            'vendor_code': forms.TextInput(attrs={'class': 'form-control'}),
            # 'tag': forms.TextInput(attrs={'class': 'form-control'}),
        }


class ImageUpdateForm(forms.ModelForm):
    class Meta:
        model = Image
        exclude = ['good', ]

        # widgets = {
        #     'image_1': forms.TextInput(attrs={'class': 'form-control'}),
        #     'image_2': forms.TextInput(attrs={'class': 'form-control'}),
        #     'image_3': forms.FileInput(attrs={'class': 'form-control'}),
        #     'image_4': forms.TextInput(attrs={'class': 'form-control'}),
        #     'image_5': forms.TextInput(attrs={'class': 'form-control'}),
        # }


class CharacteristicUpdateForm(forms.ModelForm):
    class Meta:
        model = Characteristic
        exclude = ['good', ]

        # widgets = {
        #     'color': forms.TextInput(attrs={'class': 'form-control'}),
        #     'size': forms.TextInput(attrs={'class': 'form-control'}),
        #     'length': forms.TextInput(attrs={'class': 'form-control'}),
        #     'width': forms.TextInput(attrs={'class': 'form-control'}),
        #     'height': forms.TextInput(attrs={'class': 'form-control'}),
        # }


