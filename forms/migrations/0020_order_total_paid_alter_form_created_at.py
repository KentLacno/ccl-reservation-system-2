# Generated by Django 5.0 on 2024-01-17 14:44

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forms', '0019_remove_form_friday_remove_form_monday_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='total_paid',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='form',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 17, 22, 44, 58, 376501)),
        ),
    ]