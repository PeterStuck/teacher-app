from django.contrib.auth.models import User
from django.forms import Form
from django.forms import ChoiceField, Select, PasswordInput, CharField


all_users = User.objects.all()
usernames = [[user.username, user.get_full_name()] for user in all_users if not user.is_superuser]


class LoginForm(Form):
    username = ChoiceField(
        label='Zaloguj jako',
        choices=usernames,
        widget=Select(attrs={
            'class': 'form-control form__field form__field--dark',
        }))

    password = CharField(
        label='Hasło',
        widget=PasswordInput(attrs={
            'class': 'form-control form__field form__field--dark'
        }),
        required=True)


class ChangePasswordForm(Form):
    old_passw = CharField(
        label='Stare hasło',
        widget=PasswordInput(attrs={'class': 'form-control form__field form__field--dark'}),
        required=True)

    passw = CharField(
        label='Nowe hasło',
        widget=PasswordInput(attrs={'class': 'form-control form__field form__field--dark'}),
        required=True)