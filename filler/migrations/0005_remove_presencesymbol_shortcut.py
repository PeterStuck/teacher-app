# Generated by Django 3.1.6 on 2021-02-18 22:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('filler', '0004_presencesymbol'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='presencesymbol',
            name='shortcut',
        ),
    ]
