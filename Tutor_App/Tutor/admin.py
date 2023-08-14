from django import forms
from django.contrib import admin
from .models import   EnrollmentForm, Student_Notification, Subject, Teacher,Student,ClassSubject,Class, Teacher_Notification, TeacherClass, TimeSlot,  User_Admin

# Register your models here.
class ClassAdmin(admin.ModelAdmin):
    list_display = ['name']

admin.site.register(Class, ClassAdmin)

class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name']

admin.site.register(Subject, SubjectAdmin)

class ClassSubjectAdmin(admin.ModelAdmin):
    list_display = ['id','class_name_id','class_name','subject_id', 'subject']

admin.site.register(ClassSubject, ClassSubjectAdmin)


class TeacherClassAdmin(admin.ModelAdmin):
    list_display = ['id','class_name','subject_name','teacher']

    def class_name(self,obj):
        return obj.class_subject.class_name.name
    def subject_name(self,obj):
        return obj.class_subject.subject.name
    
admin.site.register(TeacherClass, TeacherClassAdmin)

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['id', 'full_name', 'email', 'phone_number', 'gender', 'image', 'address', 'grade','subjects','verification_status']




@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['id','email']

@admin.register(User_Admin)
class User_AdminAdmin(admin.ModelAdmin):
    list_display = ['id','email']

@admin.register(EnrollmentForm)
class EnrollmentFormAdmin(admin.ModelAdmin):
    list_display = ['id','tutor','student','parents_name','parents_number','students_name','students_number','gender',
                    'grade','subjects','address','preffered_teaching_location','date_joined','confirmation',
                    'cancellation','time','confirmedDate','cancelledDate','selected_tuitionjoining_date','startTime','endTime','finishedTeachingDate'
                    ]


@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ['id','teacherId','startTime','endTime','disable']


@admin.register(Student_Notification)
class Student_NotificationAdmin(admin.ModelAdmin):
    list_display = ['id','student_id','teacher_id','message','date','seen']

@admin.register(Teacher_Notification)
class Teacher_NotificationAdmin(admin.ModelAdmin):
    list_display = ['id','teacher_id','message','date','seen']    