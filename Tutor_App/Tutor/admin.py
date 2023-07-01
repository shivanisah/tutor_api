from django import forms
from django.contrib import admin
from .models import  Admin, EnrollmentForm, Subject, Teacher,Student,ClassSubject,Class, TimeSlot, User

# Register your models here.
class ClassAdmin(admin.ModelAdmin):
    list_display = ['name']

admin.site.register(Class, ClassAdmin)

class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name']

admin.site.register(Subject, SubjectAdmin)

class ClassSubjectAdmin(admin.ModelAdmin):
    list_display = ['id','class_name_id','class_name','subject_id', 'subject', 'teacher']

admin.site.register(ClassSubject, ClassSubjectAdmin)


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['id', 'full_name', 'email', 'phone_number', 'gender', 'image', 'address', 'grade','subjects','latitude','longitude','verification_status']




@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['id','email']

@admin.register(Admin)  
class AdminAdmin(admin.ModelAdmin):
    list_display = ['id','admin','email'] 

@admin.register(User) 
class AdminUser(admin.ModelAdmin):
    list_display = ['id','email']   

@admin.register(EnrollmentForm)
class EnrollmentFormAdmin(admin.ModelAdmin):
    list_display = ['id','tutor','student','parents_name','parents_number','students_name','students_number','gender',
                    'grade','subjects','address','preffered_teaching_location','teaching_time','date_joined','confirmation',
                    'cancellation','time','confirmedDate','cancelledDate','selected_tuitionjoining_date','startTime','endTime','finishedTeachingDate'
                    ]


@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ['id','teacherId','startTime','endTime','disable']


