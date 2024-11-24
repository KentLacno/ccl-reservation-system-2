# Generated by Django 4.2.16 on 2024-11-18 13:36

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forms', '0006_fooditem_type_alter_form_created_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='LunchForm',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('forms.form',),
        ),
        migrations.CreateModel(
            name='SnacksForm',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('forms.form',),
        ),
        migrations.RemoveField(
            model_name='form',
            name='type',
        ),
        migrations.AlterField(
            model_name='form',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 11, 18, 13, 36, 24, 123950)),
        ),
    ]
