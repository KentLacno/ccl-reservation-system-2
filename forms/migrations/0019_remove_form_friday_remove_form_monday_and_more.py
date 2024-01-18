# Generated by Django 5.0 on 2024-01-17 14:17

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forms', '0018_remove_order_submitted_at_alter_form_created_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='form',
            name='friday',
        ),
        migrations.RemoveField(
            model_name='form',
            name='monday',
        ),
        migrations.RemoveField(
            model_name='form',
            name='thursday',
        ),
        migrations.RemoveField(
            model_name='form',
            name='tuesday',
        ),
        migrations.RemoveField(
            model_name='form',
            name='wednesday',
        ),
        migrations.AddField(
            model_name='order',
            name='form',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='forms.form'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='paid',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='form',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 17, 22, 16, 49, 357889)),
        ),
    ]
