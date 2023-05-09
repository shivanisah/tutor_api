# Generated by Django 4.2 on 2023-05-09 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('full_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone_number', models.CharField(max_length=100)),
                ('gender', models.CharField(blank=True, choices=[('MALE', 'MALE'), ('FEMALE', 'FEMALE')], max_length=6, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('address', models.CharField(max_length=100)),
                ('grade', models.CharField(max_length=100)),
                ('subjects', models.CharField(max_length=100)),
                ('is_active', models.BooleanField(default=False)),
                ('is_student', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('full_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone_number', models.CharField(max_length=100)),
                ('gender', models.CharField(blank=True, choices=[('MALE', 'MALE'), ('FEMALE', 'FEMALE')], max_length=6, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('address', models.CharField(max_length=100)),
                ('certificate', models.FileField(blank=True, null=True, upload_to='certificates/')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('is_active', models.BooleanField(default=False)),
                ('is_teacher', models.BooleanField(default=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='tutor_user_groups', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='tutor_user_permissions', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]