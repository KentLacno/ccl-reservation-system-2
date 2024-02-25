# Generated by Django 5.0 on 2024-01-17 12:40

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forms', '0016_order_form_order_submitted_at_alter_form_created_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='form',
        ),
        migrations.AlterField(
            model_name='form',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 17, 20, 40, 0, 565861)),
        ),
        migrations.AlterField(
            model_name='order',
            name='submitted_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 17, 20, 40, 0, 566860)),
        ),
    ]