# Generated by Django 3.1.6 on 2021-03-05 21:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('filler', '0006_delete_department'),
    ]

    operations = [
        migrations.DeleteModel(
            name='PolishDays',
        ),
        migrations.DeleteModel(
            name='PresenceSymbol',
        ),
    ]
