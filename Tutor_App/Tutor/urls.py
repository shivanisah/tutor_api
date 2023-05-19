from . import views
from django.urls import path
from .models import Teacher, Student
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('teacher/',views.TeacherList.as_view(),name='teacher'),
    path('student/',views.StudentList.as_view(),name='student'),

    path('teachersignup/',views.TeacherSignupView.as_view(),name='teachersign'),
    path('studentsignup/',views.StudentSignupView.as_view(),name='studentsign'),
    # path('activate/<uidb64>/<token>/<model>/', ActivateAccount.as_view(model=Teacher), name='teacher_activate'),
    # path('activate/<uidb64>/<token>/<model>/', ActivateAccount.as_view(model=Student), name='student_activate'),
    path('activate/<uidb64>/<token>/',
         views.ActivateAccount.as_view(), name='activate'),
    path('activate_student/<uidb64>/<token>/',
         views.ActivateAccountStudent.as_view(), name='activate_student'),

    path('login/', views.LoginView.as_view(), name='login'),
    path('profile/', views.TeacherProfileView.as_view(), name='profile'),
    path('find_teachers/', views.find_teachers, name='find_teachers'),

#     path('api/teachers/search/',views.TeacherSearchView.as_view(), name='teacher-search'),

    
]
