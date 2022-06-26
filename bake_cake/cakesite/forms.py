from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


from .models import Cake, Order, CustomUser


class CreateUserForm(UserCreationForm):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone = forms.CharField(validators=[phone_regex], max_length=12)
    username = forms.CharField(max_length=20)
    communication_contact = forms.CharField(label='Link to your social network',
                                            max_length=50,
                                            required=False)
    address = forms.CharField(label='Delivery address',
                              max_length=50)
    consent_to_processing_db = forms.BooleanField(label='Consent to the processing of personal data')

    class Meta:
        model = CustomUser
        fields = ['username',
                  'password1',
                  'password2',
                  'phone',
                  'first_name',
                  'last_name',
                  'email',
                  'communication_contact',
                  'address',
                  'consent_to_processing_db'
                  ]


class LoginForm(forms.Form):
    username = forms.CharField(label='Логин')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)


class CakeForm(forms.ModelForm):
    inscription = forms.CharField(label='Надпись',
                                      required=False,
                                      help_text='Мы можем разместить на торте любую надпись, например: «С днем рождения!»')

    class Meta:
        model = Cake
        fields = ('levels_count', 'cake_form', 'topping', 'berries',
                  'decor', 'promocode')


class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ('address', 'deliver_to')

    def clean_deliver_to(self):
        deliver_to = self.cleaned_data['deliver_to']
        if deliver_to < timezone.now():
            return ValidationError('Время доставки не может быть меньше текущего времени')
        return deliver_to


class CommentForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ('comment',)
