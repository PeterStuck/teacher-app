from django import forms
from django.forms import CharField


class TopicSearchForm(forms.Form):
    keyword = CharField(
        label='',
        error_messages={
            'required': 'To pole jest wymagane.'
        })