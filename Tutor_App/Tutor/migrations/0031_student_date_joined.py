# Generated by Django 4.2 on 2023-06-30 07:31

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Tutor', '0030_teacher_verification_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='date_joined',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
