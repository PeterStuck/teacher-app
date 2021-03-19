from django import forms
from django.forms import ChoiceField, CharField, Select, TextInput, Textarea, BooleanField, CheckboxInput
from django.core.validators import RegexValidator
from django.contrib.auth.models import User

from base.models import Department, PresenceSymbol
from .models import IndividualLessonPaymentType, RevalidationStudent
from .plain_classes.vulcan_data import RevalidationVulcanData


PRESENCE_SYMBOLS = [[symbol.symbol, symbol.full_name] for symbol in PresenceSymbol.objects.all()]

REQUIRED_ERROR_INFO = 'To pole jest wymagane.'


class RevalidationLessonForm(forms.Form):
    department = ChoiceField(
        label='Szkoła',
        choices=[],
        error_messages= {
            'invalid_choice': 'Wybierz szkołę.'
        },
        widget=Select(attrs={
            'class': 'form-control form__field form__field--dark'
        })
    )
    student = ChoiceField(
        label='Wybierz ucznia',
        choices=[[0, '---']],
        error_messages= {
            'required': REQUIRED_ERROR_INFO,
            'invalid_choice': 'Wybierz właściwego ucznia.'
        },
        widget=Select(attrs={
            'class': 'form-control form__field form__field--dark'
        })
    )
    date = CharField(
        label='Data spotkania',
        validators=[
            RegexValidator(regex='^[0-9]{2}\.[0-9]{2}\.[0-9]{4}$', message='Data musi być w formacie DD.MM.RRRR')],
        error_messages= {
            'required': REQUIRED_ERROR_INFO
        },
        widget=TextInput(attrs={
            'class': 'form-control form__field form__field--dark'
        }),
        required=True)
    topic = CharField(
        label='Temat lekcji',
        error_messages= {
            'required': REQUIRED_ERROR_INFO
        },
        widget=TextInput(attrs={
            'class': 'form-control form__field form__field--dark'
        }),
        required=True)

    get_saved_topic = BooleanField(
        label='Wykorzystaj jeden z zapisanych (Kliknij tutaj)',
        widget=CheckboxInput(attrs={
            'class': 'form-control form__field',
            'id': 'get_saved_topic',
            'style': 'display: none;',
        }),
        required=False
    )

    comments = CharField(
        label='Uwagi',
        error_messages= {
            'required': REQUIRED_ERROR_INFO
        },
        widget=Textarea(attrs={
            'class': 'form-control form__textarea form__textarea--dark'
        }),
        required=False)
    payment_type = ChoiceField(
        label='Typ płatności',
        choices=[],
        widget=Select(attrs={
            'class': 'form-control form__field form__field--dark'
        })
    )
    num_of_hours = CharField(
        label='Liczba godzin',
        error_messages= {
            'required': REQUIRED_ERROR_INFO
        },
        widget=TextInput(attrs={
            'class': 'form-control form__field form__field--dark',
            'type': 'number',
        }),
        required=True)
    presence_symbol = ChoiceField(
        label='Status obecności',
        choices=PRESENCE_SYMBOLS,
        widget=Select(attrs={
            'class': 'form-control form__field form__field--dark'
        })
    )

    def __init__(self, user: User= None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        departments = [[department.name, department.full_name] for department in Department.objects.all()]
        departments.insert(0, [0, '---'])
        self.fields['department'].choices = departments
        self.fields['payment_type'].choices = [[payment_type.type, payment_type.type] for payment_type in IndividualLessonPaymentType.objects.all()]

        if 'student' in self.data:
            try:
                department_name = self.data.get('department')
                self.fields['student'].choices = \
                    [[student.id, student.name] for student in RevalidationStudent.objects
                        .filter(department__name=department_name)
                        .filter(teacher=user)
                        .order_by('name')]
            except (ValueError, TypeError) as e:
                print("ERROR", e)
                pass

    def parse_to_vulcan_data(self):
        form_fields = dict()
        for field in self.fields:
            form_fields[field] = self.data.get(field)

        vd = RevalidationVulcanData(**form_fields)

        student_id = self.data.get('student')
        student = RevalidationStudent.objects.get(pk=student_id)
        vd.student = student

        return vd


class AddRevalidationStudentForm(forms.ModelForm):
    department = ChoiceField(
        label='Szkoła',
        choices=[],
        error_messages={
            'invalid_choice': 'Wybierz właściwą szkołę.'
        },
        widget=Select(attrs={
            'class': 'form-control form__field form__field--dark'
        })
    )

    class Meta:
        model = RevalidationStudent
        fields = ['name']
        exclude = ['teacher']

        widgets = {
            'name': TextInput(attrs={
                'class': 'form-control form__field form__field--dark',
            }),
        }

        labels = {
            'name': 'Nazwa ucznia (taka jak widnieje na stronie)',
        }

        error_messages = {
            'name': {
                'required': REQUIRED_ERROR_INFO
            },
        }

    def __init__(self, user: User, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance.teacher = user
        self.fields['department'].choices = [[department.name, department.full_name] for department in Department.objects.all()]

    def save(self, department_name, commit=True):
        print("##", self.instance.name)
        self.instance.name = self.instance.name.title()
        print("##", self.instance.name)
        if self.errors:
            raise ValueError(
                "The %s could not be %s because the data didn't validate." % (
                    self.instance._meta.object_name,
                    'created' if self.instance._state.adding else 'changed',
                )
            )
        if commit:
            self.instance.department = Department.objects.filter(name=department_name).first()
            self.instance.save()
        return self.instance



