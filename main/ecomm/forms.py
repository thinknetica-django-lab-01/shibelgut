from django import forms
from ecomm.models import User, Good, Image, Characteristic, Seller, Subscriber
from django.core.exceptions import ValidationError
from django.forms.models import inlineformset_factory
from django.core.validators import RegexValidator

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset


class ProfileUserForm(forms.ModelForm):

    # validate_numeric = RegexValidator(regex='^[0-9]*$', message='Use only digits')
    # age = forms.CharField(max_length=3, required=True, validators=[validate_numeric])

    age = forms.IntegerField(min_value=18, max_value=120, required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

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


class SubscriptionForm(forms.ModelForm):

    is_subscribed = forms.BooleanField(label='Subscribe to new goods')

    class Meta:
        model = Subscriber
        fields = ['is_subscribed']


class GoodCreateForm(forms.ModelForm):
    class Meta:
        model = Good
        exclude = ['pub_date', 'rating']

    @property
    def helper(self):
        helper = FormHelper()
        helper.form_tag = False

        helper.layout = Layout(Fieldset('Create a new good', 'title', 'price', 'description', 'brand', 'quantity',
                                        'issue_date', 'vendor_code', 'tag', 'seller'), )

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


class ImageUpdateForm(forms.ModelForm):
    class Meta:
        model = Image
        exclude = ['good', ]


class CharacteristicUpdateForm(forms.ModelForm):
    class Meta:
        model = Characteristic
        exclude = ['good', ]


class SellerCreateForm(forms.ModelForm):
    class Meta:
        model = Seller
        exclude = ['user', ]

