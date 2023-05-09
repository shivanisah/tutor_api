from django.db import models 
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


from django.contrib.auth.models import Group,Permission
from django.db.models.signals import post_save
from django.dispatch import receiver

CLASS_CHOICES = (
    (1, 'Class 1'),
    (2, 'Class 2'),
    (3, 'Class 3'),
    (4, 'Class 4'),
    (5, 'Class 5'),
    (6, 'Class 6'),
    (7, 'Class 7'),
    (8, 'Class 8'),
    (9, 'Class 9'),
    (10, 'Class 10'),
)

SUBJECT_CHOICES = (
    ('science', 'Science'),
    ('maths', 'Maths'),
    ('nepali', 'Nepali'),
    ('english', 'English'),
    ('social', 'Social'),
)


class MyUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email).lower()
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)
   

class Teacher(AbstractBaseUser, PermissionsMixin):
    groups = models.ManyToManyField(
        'auth.Group',
        blank=True,
        related_name='tutor_user_groups',
        verbose_name='groups',
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        blank=True,
        related_name='tutor_user_permissions',
        verbose_name='user permissions',
        help_text='Specific permissions for this user.',
    )

    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=100)
    gender = models.CharField(
        max_length=6,
        choices=[('MALE','MALE'),('FEMALE','FEMALE')],blank=True,null=True
    )
    image = models.ImageField(upload_to='images/',blank=True,null=True)
    address = models.CharField(max_length=100)
    certificate = models.FileField(upload_to = 'certificates/',blank=True,null=True)
    name = models.CharField(max_length=100,null=True,blank=True)
    # teaching_grades = models.ForeignKey(Class, on_delete=models.SET_NULL, null=True, blank=True)
    # subjects = models.ManyToManyField(Subject, related_name='teachers', blank=True)    
    is_active = models.BooleanField(default=False)
    is_teacher=models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name','email','phone_number','address']

    objects = MyUserManager()

    def __str__(self):
        return self.email
    
class Student(AbstractBaseUser):
    # groups = models.ManyToManyField(
    #     'auth.Group',
    #     blank=True,
    #     related_name='tutor_user_groups',
    #     verbose_name='groups',
    #     help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
    # )
    # user_permissions = models.ManyToManyField(
    #     'auth.Permission',
    #     blank=True,
    #     related_name='tutor_user_permissions',
    #     verbose_name='user permissions',
    #     help_text='Specific permissions for this user.',
    # )

    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=100)
    gender = models.CharField(
        max_length=6,
        choices=[('MALE','MALE'),('FEMALE','FEMALE')],blank=True,null=True
    )
    image = models.ImageField(upload_to='images/',blank=True,null=True)
    address = models.CharField(max_length=100)
    grade = models.CharField(max_length=100)
    subjects = models.CharField(max_length=100)
    is_active = models.BooleanField(default=False)
    is_student=models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name','email','phone_number','address','grade','subjects']

    objects = MyUserManager()

    def __str__(self):
        return self.email



