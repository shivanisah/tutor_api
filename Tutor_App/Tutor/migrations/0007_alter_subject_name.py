# Generated by Django 4.2 on 2023-05-19 02:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Tutor', '0006_teacher_class_subjects'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subject',
            name='name',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]