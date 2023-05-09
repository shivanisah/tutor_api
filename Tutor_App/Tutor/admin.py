from django import forms
from django.contrib import admin
from .models import  Teacher,Student

# Register your models here.

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['id','full_name','email','phone_number','gender','image','address']

# def display_subjects(self, obj):
#         # Retrieve the subjects based on the selected teaching_grades
#         subjects = obj.subjects.filter(classes__class_number=obj.teaching_grades)
#         return ", ".join([subject.name for subject in subjects])
# class TeacherAdminForm(forms.ModelForm):
#     class Meta:
#         model = Teacher
#         fields = '__all__'

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['subjects'].queryset = Subject.objects.none()

#         if self.instance and self.instance.teaching_grades:
#             selected_class = self.instance.teaching_grades
#             self.fields['subjects'].queryset = Subject.objects.filter(classes__class_number=selected_class.class_number)


# class TeacherAdmin(admin.ModelAdmin):
#     form = TeacherAdminForm
#     list_display = ['id', 'full_name', 'email', 'phone_number', 'gender', 'image', 'address', 'teaching_grades', 'display_subjects']

#     def display_subjects(self, obj):
#         subjects = obj.subjects.all()
#         return ", ".join([subject.name for subject in subjects])

#     class Media:
#         js = ('js/teacher_admin.js',)


# admin.site.register(Teacher, TeacherAdmin)

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['id','full_name','email','phone_number','gender','image','address','grade','subjects']
    

