from django import forms
from django.contrib import admin
from .models import  Subject, Teacher,Student,ClassSubject,Class

# Register your models here.
class ClassAdmin(admin.ModelAdmin):
    list_display = ['name']

admin.site.register(Class, ClassAdmin)

class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name']

admin.site.register(Subject, SubjectAdmin)

class ClassSubjectAdmin(admin.ModelAdmin):
    list_display = ['class_name', 'subject', 'teacher']

admin.site.register(ClassSubject, ClassSubjectAdmin)


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['id', 'full_name', 'email', 'phone_number', 'gender', 'image', 'address', 'grade','subjects','latitude','longitude']


# class ClassSubjectInline(admin.TabularInline):
#     model = ClassSubject
#     extra = 1


# @admin.register(Teacher)
# class TeacherAdmin(admin.ModelAdmin):
#     list_display = ['id', 'full_name', 'email', 'phone_number', 'gender', 'image', 'address', 'class_name','display_class_subjects']
#     inlines = [ClassSubjectInline]
#     def display_class_subjects(self, obj):
#         return ", ".join(obj.class_subjects.values_list('name', flat=True))
#     display_class_subjects.short_description = 'Class Subjects'

#     fieldsets = (
#         (None, {
#             'fields': ('full_name', 'email', 'phone_number', 'gender', 'image', 'address', 'class_name','class_subjects')
#         }),
#     )

# @admin.register(Teacher)
# class TeacherAdmin(admin.ModelAdmin):
#     list_display = ['id', 'full_name', 'email', 'phone_number', 'gender', 'image', 'address', 'display_class_name', 'display_class_subjects']
#     inlines = [ClassSubjectInline]

#     def display_class_name(self, obj):
#         return obj.class_name.name if obj.class_name else None
#     display_class_name.short_description = 'Class Name'

#     def display_class_subjects(self, obj):
#         return ", ".join(obj.class_subjects.values_list('name', flat=True))
#     display_class_subjects.short_description = 'Class Subjects'

#     fieldsets = (
#         (None, {
#             'fields': ('full_name', 'email', 'phone_number', 'gender', 'image', 'address')
#         }),
#     )
# @admin.register(Teacher)
# class TeacherAdmin(admin.ModelAdmin):
#     list_display = ['id', 'full_name', 'email', 'phone_number', 'gender', 'image', 'address', 'display_class_name', 'display_class_subjects']
#     inlines = [ClassSubjectInline]

#     def display_class_name(self, obj):
#         if obj.class_name:
#             return obj.class_name.name
#         else:
#             return None
#     display_class_name.short_description = 'Class Name'

#     def display_class_subjects(self, obj):
#         return ", ".join(obj.class_subjects.values_list('name', flat=True))
#     display_class_subjects.short_description = 'Class Subjects'

#     fieldsets = (
#         (None, {
#             'fields': ('full_name', 'email', 'phone_number', 'gender', 'image', 'address')
#         }),
#     )


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['id','full_name','email','phone_number','gender','image','address','grade','subjects']
    


from django.db.models import Q


# class TeacherForm(forms.ModelForm):
#     class Meta:
#         model = Teacher
#         fields = ('full_name', 'email', 'phone_number', 'gender', 'image', 'address', 'class_name', 'class_subjects')

#     class_subjects = forms.ModelMultipleChoiceField(
#         queryset=Subject.objects.none(),
#         widget=forms.CheckboxSelectMultiple,
#         required=False
#     )

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         if self.instance.pk:
#             self.fields['class_subjects'].initial = self.instance.class_subjects.values_list('pk', flat=True)

#         if 'class_name' in self.data:
#             class_id = self.data['class_name']
#             self.fields['class_subjects'].queryset = ClassSubject.objects.filter(class_name_id=class_id).values_list('subject__name', flat=True)

#     def save(self, commit=True):
#         teacher = super().save(commit=commit)
#         if commit:
#             class_name = self.cleaned_data.get('class_name')
#             class_subjects = self.cleaned_data.get('class_subjects')
#             if class_name and class_subjects:
#                 # Clear existing class subjects for the teacher
#                 ClassSubject.objects.filter(class_name_id=class_name, teacher=teacher).delete()
#                 # Create new class subjects for the teacher
#                 for subject_name in class_subjects:
#                     subject = Subject.objects.get(name=subject_name)
#                     ClassSubject.objects.create(class_name_id=class_name, subject=subject, teacher=teacher)
#         return teacher


# class TeacherAdmin(admin.ModelAdmin):
#     form = TeacherForm

#     def get_form(self, request, obj=None, **kwargs):
#         form = super().get_form(request, obj, **kwargs)
#         form.base_fields['class_subjects'].queryset = Subject.objects.none()
#         if obj and obj.class_name:
#             form.base_fields['class_subjects'].queryset = ClassSubject.objects.filter(class_name=obj.class_name).values_list('subject__name', flat=True)
#         return form

#     def formfield_for_foreignkey(self, db_field, request, **kwargs):
#         if db_field.name == 'class_name':
#             kwargs['queryset'] = Class.objects.all()
#         return super().formfield_for_foreignkey(db_field, request, **kwargs)


# admin.site.register(Teacher, TeacherAdmin)


