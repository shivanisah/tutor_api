from . import views
from django.urls import path
from .models import Teacher, Student
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('teacher/',views.TeacherList.as_view(),name='teacher'),
    path('student/',views.StudentList.as_view(),name='student'),

    path('classSubject/',views.ClassSubjectAPIView.as_view(),name='classSubject'),
    path('class/',views.ClassList.as_view(),name='class'),
    path('Subject/',views.SubjectList.as_view(),name='Subject'),


    path('teachersignup/',views.TeacherSignupView.as_view(),name='teachersign'),
    path('studentsignup/',views.StudentSignupView.as_view(),name='studentsign'),
    path('enrollment/',views.EnrollmentFormView.as_view(),name='enrollment'),
    path('students/<int:teacher_id>/', views.StudentEnrollmentListView.as_view(), name='students-enrollments'),
    path('confirmstudents/<int:teacher_id>/', views.ConfirmStudentEnrollmentListView.as_view(), name='confirmstudents-enrollments'),
    path('rejectedstudents/<int:teacher_id>/', views.RejectedStudentsEnrollmentListView.as_view(), name='rejectedstudents-enrollments'),

    path('timeslot/',views.TimeSlotView.as_view(),name='timeslot'),
    path('timeslotList/<int:teacher_id>',views.TimeSlotListAPIView.as_view(),name='timeslotList'),
    path('timeslotdisable/<int:slot_id>',views.TimeSlotDisableAPIView.as_view(),name='timeslotdisable'),
    path('timeslotenable/<int:slot_id>',views.TimeSlotEnableAPIView.as_view(),name='timeslotenable'),

    path('teacherProfileGet/<int:teacher_id>',views.TeacherProfileAPIView.as_view(),name='teacherProfileGet'),



    path('enrollments/<int:enrollment_id>/confirm/', views.EnrollmentConfirmationView.as_view(), name='enrollment-confirmation'),
    path('enrollments/<int:enrollment_id>/cancel/', views.EnrollmentCancelView.as_view(), name='enrollment-cancellation'),
    path('enrollments/<int:enrollment_id>/finishedteaching/', views.EnrollmentTuitionFinishedTeachingView.as_view(), name='enrollment-finishedteaching'),

    path('teachersUpdate/<int:pk>/', views.TeacherUpdateView.as_view(), name='teacher-update'),


    path('activate/<uidb64>/<token>/',
         views.ActivateAccount.as_view(), name='activate'),
    path('activate_student/<uidb64>/<token>/',
         views.ActivateAccountStudent.as_view(), name='activate_student'),

    path('login/', views.LoginView.as_view(), name='login'),
    path('profile/', views.TeacherProfileView.as_view(), name='profile'),
    path('find_teachers/', views.find_teachers, name='find_teachers'),

#     path('api/teachers/search/',views.TeacherSearchView.as_view(), name='teacher-search'),
# admin
    path('registeredTeacherList/',views.RegisteredTeacherList.as_view(),name='registeredTeacherList'),
    path('verifiedTeacherList/',views.VerifiedTeacherList.as_view(),name='verifiedTeacherList'),
    path('registered_teachers/<int:teacher_id>/verification/', views.RegisteredTeacherVerificationView.as_view(), name='teacher-verification'),
    path('registeredStudentList/',views.RegisteredStudentList.as_view(),name='registeredStudentList'),

    
]
