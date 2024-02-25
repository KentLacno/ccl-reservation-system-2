# Generated by Django 5.0 on 2024-01-17 10:30

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forms', '0011_rename_food_item_option_food_items_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='option',
            name='form',
        ),
        migrations.AddField(
            model_name='form',
            name='options',
            field=models.ManyToManyField(to='forms.option'),
        ),
        migrations.AlterField(
            model_name='form',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 17, 18, 30, 33, 794086)),
        ),
    ]