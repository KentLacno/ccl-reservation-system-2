# Generated by Django 5.0 on 2024-01-17 12:06

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forms', '0012_remove_option_form_form_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='email',
        ),
        migrations.AlterField(
            model_name='form',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 17, 20, 6, 52, 872393)),
        ),
        migrations.AlterField(
            model_name='option',
            name='weekday',
            field=models.CharField(choices=[('1', 'monday'), ('2', 'tuesday'), ('3', 'wednesday'), ('4', 'thursday'), ('5', 'friday')], max_length=3),
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weekday', models.CharField(choices=[('1', 'monday'), ('2', 'tuesday'), ('3', 'wednesday'), ('4', 'thursday'), ('5', 'friday')], max_length=3)),
                ('food_items', models.ManyToManyField(to='forms.fooditem')),
            ],
        ),
        migrations.AddField(
            model_name='profile',
            name='reservations',
            field=models.ManyToManyField(to='forms.reservation'),
        ),
    ]