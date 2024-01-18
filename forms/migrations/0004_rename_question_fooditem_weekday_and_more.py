# Generated by Django 5.0 on 2024-01-16 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forms', '0003_profile'),
    ]

    operations = [
        migrations.RenameField(
            model_name='fooditem',
            old_name='question',
            new_name='weekday',
        ),
        migrations.RemoveField(
            model_name='weekday',
            name='year_in_school',
        ),
        migrations.AddField(
            model_name='form',
            name='active',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='form',
            name='monday',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='form',
            name='week',
            field=models.CharField(default='', max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='weekday',
            name='weekday',
            field=models.CharField(choices=[('mon', 'Monday'), ('tue', 'Tuesday'), ('wed', 'Wednesday'), ('thu', 'Thursday'), ('fri', 'Friday')], default='mon', max_length=3),
        ),
    ]
