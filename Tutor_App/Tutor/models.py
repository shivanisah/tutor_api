from django.utils import timezone
from django.db import models 
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


from django.contrib.auth.models import Group,Permission
from django.db.models.signals import post_save
from django.dispatch import receiver

class Class(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Subject(models.Model):
    name = models.CharField(max_length=50,unique=True)

    def __str__(self):
        return self.name

class ClassSubject(models.Model):
    class_name = models.ForeignKey(Class, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey('Teacher', on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self):
        return f'{self.class_name_id} - {self.subject_id}'
    
Teaching_Location = (
    ('Student Home','Student Home'),
    ('Tutor Place','Tutor Place'),
    ('Both','Both'),
)

Teaching_Experience = (
    ('Not Yet','Not Yet'),
    ('1 Year','1 Year'), 
    ('2 Years','2 Years'),
    ('3 Years','3 Years'),
    ('4 Years','4 Years'),
    ('5 Years','5 Years'),
    ('6 Years','6 Years'),
    ('7 Years','7 Years'),
    ('8 Years','8 Years'),
    ('9 Years','9 Years'),
    ('10 Years','10 Years'),
    ('10+ Years','10+ Years'),

)

Education = (
    ('Secondary level','Secondary level'),
    ('Higher Secondary level(Pursuing)','Higher Secondary level(Pursuing)'),
    ('Higher Secondary level(Completed)','Higher Secondary level(Completed)'),
    ('Bachelors Degree(Pursuing)','Bachelors Secondary level(Pursuing)'),
    ('Bachelors Degree(Completed)','Bachelors Degree(Completed)'),
    ('Masters Degree(Pursuing)','Masters Degree(Pusuing)'),
    ('Masters Degree(Completed)','Masters Degree(Completed)'),

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
        choices=[('Male','Male'),('Female','Female')],blank=True,null=True
    )
    image = models.ImageField(upload_to='images/',blank=True,null=True)
    address = models.CharField(max_length=100,blank=True,null=True)
    certificate = models.FileField(upload_to = 'certificates/',blank=True,null=True)

    teaching_location = models.CharField(max_length  = 100,choices=Teaching_Location,null=True,blank=True)
    teaching_experience = models.CharField(max_length =100,choices=Teaching_Experience,null=True,blank=True)
    education = models.CharField(max_length=100,choices=Education,null=True,blank=True)
    # class_name = models.ForeignKey(Class, on_delete=models.CASCADE,null=True,blank=True)
    # class_subjects = models.ManyToManyField(Subject, through=ClassSubject,blank=True)

    grade = models.CharField(max_length=100,null=True,blank=True)
    subjects = models.TextField(null=True,blank=True)
    latitude = models.DecimalField(max_digits=20, decimal_places=12,null=True,blank=True)
    longitude = models.DecimalField(max_digits=20, decimal_places=12,null=True,blank=True)
    about_me = models.TextField(null=True,blank=True)

    is_active = models.BooleanField(default=False)
    is_teacher=models.BooleanField(default=True)

    verification_status = models.BooleanField(default = False)
    date_joined         = models.DateField(default = timezone.now)
    verification_date   = models.DateTimeField(null=True,blank=True)

    confirmation = models.BooleanField(default=False)
    cancellation = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name','email','phone_number']

    objects = MyUserManager()

    def __str__(self):
        return self.email
    

       
    
class Student(AbstractBaseUser):

    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=False)
    is_student=models.BooleanField(default=True)
    date_joined = models.DateField(default = timezone.now)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['email']

    objects = MyUserManager()

    def __str__(self):
        return self.email
    

class User(AbstractUser):
    email = models.EmailField(unique=True)
    username=None
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = MyUserManager() 

    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='custom_user_set',  
        related_query_name='custom_user'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='custom_user_set', 
        related_query_name='custom_user'
    )

class Admin(models.Model):
    admin = models.OneToOneField(User,on_delete=models.CASCADE)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.email


class EnrollmentForm(models.Model):
    tutor = models.ForeignKey(Teacher,on_delete=models.CASCADE,null=True,blank=True)
    student = models.ForeignKey(Student,on_delete=models.CASCADE,null=True,blank=True)
    
    parents_name = models.CharField(max_length=100)
    parents_number = models.CharField(max_length=100)
    students_name = models.CharField(max_length=100)
    students_number = models.CharField(max_length=100)
    gender = models.CharField(
        max_length=6,
        choices=[('Male','Male'),('Female','Female')],blank=True,null=True
    )
    address = models.CharField(max_length=100,null=True,blank=True)
    grade = models.CharField(max_length=100,null=True,blank=True)
    subjects = models.CharField(max_length=100,null=True,blank=True)
    preffered_teaching_location = models.CharField(max_length=100,choices = Teaching_Location,null=True,blank=True)
    teaching_time = models.CharField(max_length = 100,null=True,blank=True)
    date_joined = models.DateField(default=timezone.now)
    time = models.TimeField(auto_now = True)
    confirmation = models.BooleanField(default = False)
    cancellation = models.BooleanField(default=False)
    confirmedDate = models.DateTimeField(null=True,blank=True)
    cancelledDate = models.DateTimeField(null=True,blank=True)
    selected_tuitionjoining_date = models.CharField(max_length = 100,null = True, blank = True)
    startTime = models.TimeField(null=True,blank=True)
    endTime = models.TimeField(null=True,blank=True)
    finishedTeachingDate = models.CharField(max_length = 100,null = True, blank = True)
    


class TimeSlot(models.Model): 
    teacherId = models.ForeignKey(Teacher,on_delete = models.CASCADE, null=True,blank=True)
    startTime = models.TimeField()
    endTime =  models.TimeField()
    disable = models.BooleanField(default = False)
    enable = models.BooleanField(default = False)








