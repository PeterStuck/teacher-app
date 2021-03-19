from django.forms import Form
from django.forms import PasswordInput, CharField, TextInput


REQUIRED_INFO = 'To pole jest wymagane.'


class LoginForm(Form):
    email = CharField(
        label='Email',
        widget=TextInput(attrs={
            'class': 'form-control form__field form__field--dark',
        }),
        error_messages={
            'required': REQUIRED_INFO
        },
        required=True)

    password = CharField(
        label='Hasło',
        widget=PasswordInput(attrs={
            'class': 'form-control form__field form__field--dark'
        }),
        error_messages={
            'required': REQUIRED_INFO
        },
        required=True)


class ChangePasswordForm(Form):
    old_password = CharField(
        label='Stare hasło',
        widget=PasswordInput(attrs={'class': 'form-control form__field form__field--dark'}),
        required=True)

    new_password = CharField(
        label='Nowe hasło',
        widget=PasswordInput(attrs={'class': 'form-control form__field form__field--dark'}),
        required=True)