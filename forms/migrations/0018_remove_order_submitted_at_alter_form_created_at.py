# Generated by Django 5.0 on 2024-01-17 12:40

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forms', '0017_remove_order_form_alter_form_created_at_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='submitted_at',
        ),
        migrations.AlterField(
            model_name='form',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 17, 20, 40, 28, 327209)),
        ),
    ]
