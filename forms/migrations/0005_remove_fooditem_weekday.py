# Generated by Django 5.0 on 2024-01-16 13:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forms', '0004_rename_question_fooditem_weekday_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fooditem',
            name='weekday',
        ),
    ]
