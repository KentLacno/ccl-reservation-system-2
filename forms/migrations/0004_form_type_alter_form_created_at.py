# Generated by Django 4.2.16 on 2024-11-18 13:18

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forms', '0003_alter_form_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='form',
            name='type',
            field=models.CharField(default='lunch', max_length=10),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='form',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 11, 18, 13, 18, 8, 977707)),
        ),
    ]
