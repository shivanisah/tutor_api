# Generated by Django 4.2 on 2023-07-05 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Tutor', '0032_user_admin'),
    ]

    operations = [
        migrations.AddField(
            model_name='timeslot',
            name='occupy',
            field=models.BooleanField(default=False),
        ),
    ]
