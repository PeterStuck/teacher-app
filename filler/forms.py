from django.core.validators import RegexValidator, ValidationError
from django.forms import Form
from django.forms import TextInput, FileField, ChoiceField, DateTimeField, Select, BooleanField, CheckboxInput, \
    FileInput, CharField, PasswordInput

from base.models import Department, PolishDays, PresenceSymbol
from .plain_classes.vulcan_data import FillerVulcanData

all_departments = Department.objects.all()
DEPARTMENTS = [[department.name, department.full_name] for department in all_departments]

all_polish_days = PolishDays.objects.all()
DAYS = [[day.name, day.name] for day in all_polish_days]

all_presence_status = PresenceSymbol.objects.all()
PRESENCE_SYMBOLS = [[presence.symbol, presence.full_name] for presence in all_presence_status]

REQUIRED_FIELD_INFO = 'To pole jest wymagane.'


class FillerForm(Form):
    teams_file = FileField(label="Podaj plik z Teams", widget=FileInput(attrs={'class': 'form__field'}), required=False)
    lesson = ChoiceField(
        label='Lekcja',
        choices=[[lesson, lesson] for lesson in range(1, 10)],
        widget=Select(attrs={
            'class': 'form-control form__field form__field--dark',
        })
    )
    departments = ChoiceField(
        label='Szkoła',
        choices=DEPARTMENTS,
        widget=Select(attrs={
            'class': 'form-control form__field form__field--dark',
        })
    )
    day = ChoiceField(
        label='Wybierz dzień',
        choices=DAYS,
        widget=Select(attrs={
            'class': 'form-control form__field form__field--dark',
        }),
        validators=[

        ],
    )
    date = CharField(
        label='Data',
        widget=TextInput(attrs={'class': 'form-control form__field form__field--dark'}),
        validators=[
            RegexValidator(regex='[0-9]{4}-[0-9]{2}-[0-9]{2}', message="Zachowaj datę w podanym formacie, tj. RRRR-MM-DD.")
        ],
        error_messages={
            'required': REQUIRED_FIELD_INFO,
        },
        required=True
    )
    absent_symbol = ChoiceField(
        label='Co wpisać nieobecnym?',
        choices=PRESENCE_SYMBOLS,
        widget=Select(attrs={
            'class': 'form-control form__field form__field--dark',
        })
    )
    file_not_loaded = BooleanField(
        label='Wpisz wszystkim jednakową obecność, którą ustawię poniżej.',
        widget=CheckboxInput(attrs={'class': 'form_check form__checkfield'}),
        required=False)
    is_double_lesson = BooleanField(
        label='Dwie lekcje pod rząd z tą samą obecnością.',
        widget=CheckboxInput(attrs={'class': 'form_check form__checkfield'}),
        required=False)

    use_required_attribute = True
    field_order = ['teams_file', 'file_not_loaded', 'departments', 'day', 'date', 'lesson_number', 'is_double_lesson', 'absent_symbol']
    auto_id = 'field_%s'

    def parse_to_vulcan_data(self):
        form_fields = dict()
        for field in self.fields:
            form_fields[field] = self.cleaned_data.get(field)

        vd = FillerVulcanData(**form_fields)
        vd = self.determine_filename(vd, form_fields)

        return vd

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get('file_not_loaded') and cleaned_data.get('teams_file') is None:
            raise ValidationError("Musisz wgrać plik lub wybrać opcję jednakowej obecności, aby program mógł przystąpić do działania.")

        return super().clean()

    def determine_filename(self, vd, form_fields):
        if not vd.file_not_loaded and vd.teams_file is not None:
            vd.filename = form_fields['date'] + '-' + form_fields['departments'] + '-' + form_fields['lesson'] + '.csv'
        else:
            vd.filename = None
        return vd


class WebdriverSettingsForm(Form):
    vulcan_url = CharField(label='URL do strony Vulcan', widget=TextInput(attrs={'class': 'form-control form__field'}), required=True)


class ArchiveSettingsForm(Form):
    path = CharField(label='Ścieżka absolutna do archiwum', widget=TextInput(attrs={'class': 'form-control form__field'}), required=True)