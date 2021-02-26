from django.forms import Form
from django.forms import TextInput, FileField, ChoiceField, DateTimeField, Select, BooleanField, CheckboxInput, FileInput, CharField, PasswordInput
from django.core.validators import RegexValidator, ValidationError
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

from filler.models import Department, PolishDays, PresenceSymbol

all_departments = Department.objects.all()
DEPARTMENTS = [[department.name, department.full_name] for department in all_departments]

all_polish_days = PolishDays.objects.all()
DAYS = [[day.name, day.name] for day in all_polish_days]

all_presence_status = PresenceSymbol.objects.all()
PRESENCE_SYMBOLS = [[presence.symbol, presence.full_name] for presence in all_presence_status]


class FillerStartForm(Form):
    file = FileField(label="Podaj plik z Teams", widget=FileInput(attrs={'class': 'form_field'}), required=False)
    lesson_number = ChoiceField(
        label='Wybierz lekcję',
        choices=[[lesson, lesson] for lesson in range(1, 10)],
        widget=Select(attrs={
            'class': 'form-control form_field',
        })
    )
    departments = ChoiceField(
        label='Wybierz instytucję',
        choices=DEPARTMENTS,
        widget=Select(attrs={
            'class': 'form-control form_field',
        })
    )
    day = ChoiceField(
        label='Podaj dzień',
        choices=DAYS,
        widget=Select(attrs={
            'class': 'form-control form_field',
        }),
        validators=[

        ],
    )
    date = DateTimeField(
        label='Data',
        widget=TextInput(attrs={'class': 'form-control form_field'}),
        validators=[
            RegexValidator(regex='[0-9]{4}-[0-9]{2}-[0-9]{2}', message="Zachowaj datę w podanym formacie, tj. RRRR-MM-DD.")
        ],
        input_formats=['%Y-%m-%d']
    )
    absent_symbol = ChoiceField(
        label='Co wpisać nieobecnym?',
        choices=PRESENCE_SYMBOLS,
        widget=Select(attrs={
            'class': 'form-control form_field',
        })
    )
    file_not_loaded = BooleanField(
        label='Wpisz wszystkim jednakową obecność, którą ustawię poniżej.',
        widget=CheckboxInput(attrs={'class': 'form_check'}),
        required=False)
    is_double_lesson = BooleanField(
        label='Dwie lekcje pod rząd z tą samą obecnością.',
        widget=CheckboxInput(attrs={'class': 'form_check'}),
        required=False)

    use_required_attribute = True
    field_order = ['file', 'file_not_loaded', 'departments', 'day', 'date', 'lesson_number', 'is_double_lesson', 'absent_symbol']
    auto_id = 'field_%s'


class WebdriverSettingsForm(Form):
    path = CharField(label='Ścieżka absolutna do chromedriver.exe', widget=TextInput(attrs={'class': 'form-control form_field'}), required=True)
    vulcan_url = CharField(label='URL do strony Vulcan', widget=TextInput(attrs={'class': 'form-control form_field'}), required=True)


class ChangePasswordForm(Form):
    old_passw = CharField(label='Stare hasło', widget=PasswordInput(attrs={'class': 'form-control form_field'}), required=True)
    passw = CharField(label='Nowe hasło', widget=PasswordInput(attrs={'class': 'form-control form_field'}), required=True)


class ArchiveSettingsForm(Form):
    path = CharField(label='Ścieżka absolutna do archiwum', widget=TextInput(attrs={'class': 'form-control form_field'}), required=True)


all_users = User.objects.all()
usernames = [[user.username, user.get_full_name()] for user in all_users if not user.is_superuser]


class LoginForm(Form):
    username = ChoiceField(
        label='Zaloguj jako',
        choices=usernames,
        widget=Select(attrs={
            'class': 'form-control form_field',
        }))
    password = CharField(
        label='Hasło',
        widget=PasswordInput(attrs={
            'class': 'form-control form_field'
        }),
        required=True)