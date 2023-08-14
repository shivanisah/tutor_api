# Generated by Django 4.2 on 2023-07-06 05:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Tutor', '0033_timeslot_occupy'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='groups',
        ),
        migrations.RemoveField(
            model_name='user',
            name='user_permissions',
        ),
        migrations.RemoveField(
            model_name='enrollmentform',
            name='teaching_time',
        ),
        migrations.RemoveField(
            model_name='teacher',
            name='cancellation',
        ),
        migrations.RemoveField(
            model_name='teacher',
            name='confirmation',
        ),
        migrations.RemoveField(
            model_name='timeslot',
            name='enable',
        ),
        migrations.RemoveField(
            model_name='timeslot',
            name='occupy',
        ),
        migrations.DeleteModel(
            name='Admin',
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]