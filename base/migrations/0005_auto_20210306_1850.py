# Generated by Django 3.1.6 on 2021-03-06 17:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_lessontopic'),
    ]

    operations = [
        migrations.RenameField(
            model_name='lessontopic',
            old_name='is_invidual',
            new_name='is_individual',
        ),
    ]