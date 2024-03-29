# Generated by Django 5.0 on 2024-01-17 10:04

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forms', '0006_form_friday_form_thursday_form_tuesday_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='form',
            name='active',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='form',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 17, 18, 4, 37, 36127)),
        ),
        migrations.CreateModel(
            name='Option',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weekday', models.CharField(choices=[('mon', 'Monday'), ('tue', 'Tuesday'), ('wed', 'Wednesday'), ('thu', 'Thursday'), ('fri', 'Friday')], max_length=3)),
                ('form', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='forms.form')),
            ],
        ),
        migrations.AddField(
            model_name='fooditem',
            name='options',
            field=models.ManyToManyField(to='forms.option'),
        ),
    ]
