from django import forms
from django.forms import ChoiceField, CharField
from django.core.validators import RegexValidator
from django.contrib.auth.models import User

from base.models import Department, PresenceSymbol
from .models import IndividualLessonPaymentType, RevalidationStudent

DEPARTMENTS = [[department.name, department.full_name] for department in Department.objects.all()]
DEPARTMENTS.insert(0, [0, '---'])
PAYMENT_TYPES = [[payment_type.id, payment_type.type] for payment_type in IndividualLessonPaymentType.objects.all()]
PRESENCE_SYMBOLS = [[symbol.symbol, symbol.full_name] for symbol in PresenceSymbol.objects.all()]

REQUIRED_ERROR_INFO = 'To pole jest wymagane.'


class IndividualLessonForm(forms.Form):
    department = ChoiceField(
        label='Szkoła',
        choices=DEPARTMENTS,
        error_messages= {
            'invalid_choice': 'Wybierz szkołę.'
        }
    )
    students = ChoiceField(
        label='Wybierz ucznia',
        choices=[[0, '---']],
        error_messages= {
            'required': REQUIRED_ERROR_INFO,
            'invalid_choice': 'Wybierz właściwego ucznia.'
        }
    )
    date = CharField(
        label='Data spotkania',
        validators=[
            RegexValidator(regex='^[0-9]{2}\.[0-9]{2}\.[0-9]{4}$', message='Data musi być w formacie DD.MM.RRRR')],
        error_messages= {
            'required': REQUIRED_ERROR_INFO
        },
        required=True)
    topic = CharField(label='Temat lekcji', error_messages= {
            'required': REQUIRED_ERROR_INFO
        }, required=True)
    comments = CharField(label='Uwagi', error_messages= {
            'required': REQUIRED_ERROR_INFO
        }, required=True)
    payment_type = ChoiceField(label='Typ płatności', choices=PAYMENT_TYPES)
    num_of_hours = CharField(label='Liczba godzin', error_messages= {
            'required': REQUIRED_ERROR_INFO
        }, required=True)
    presence_symbol = ChoiceField(label='Status obecności', choices=PRESENCE_SYMBOLS)

    def __init__(self, user: User, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if 'students' in self.data:
            try:
                department_name = self.data.get('department')
                self.fields['students'].choices = \
                    [[student.id, student.name] for student in RevalidationStudent.objects
                        .filter(department__name=department_name)
                        .filter(teacher=user)
                        .order_by('name')]
            except (ValueError, TypeError) as e:
                print("ERROR", e)
                pass


