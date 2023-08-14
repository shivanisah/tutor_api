from . import views
from django.urls import path
from .models import Teacher, Student
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('reset-password', views.ResetPasswordView.as_view(), name='reset-password'),
    path('reset-password-verify', views.ResetPasswordVerifyView.as_view(),
         name='reset-password-verify'),
    path('change-password', views.ChangePasswordView.as_view(), name='change-password'),
    path('change-password-verify', views.ChangePasswordVerifyView.as_view(),
         name='change-password-verify'),
     

    path('teacher/',views.TeacherList.as_view(),name='teacher'),
    path('student/',views.StudentList.as_view(),name='student'),

    path('classSubject/',views.ClassSubjectAPIView.as_view(),name='classSubject'),
    path('class/',views.ClassList.as_view(),name='class'),
    path('Subject/',views.SubjectList.as_view(),name='Subject'),


    path('teachersignup/',views.TeacherSignupView.as_view(),name='teachersign'),
    path('addteacher/',views.AddTeacherView.as_view(),name='addteacher'),

    path('studentsignup/',views.StudentSignupView.as_view(),name='studentsign'),
    path('adminsignup/',views.AdminSignupView.as_view(),name='adminsign'),

    path('enrollment/',views.EnrollmentFormView.as_view(),name='enrollment'),
    path('students/<int:teacher_id>/', views.StudentEnrollmentListView.as_view(), name='students-enrollments'),
    path('confirmstudents/<int:teacher_id>/', views.ConfirmStudentEnrollmentListView.as_view(), name='confirmstudents-enrollments'),
    path('rejectedstudents/<int:teacher_id>/', views.RejectedStudentsEnrollmentListView.as_view(), name='rejectedstudents-enrollments'),

    path('timeslot/',views.TimeSlotView.as_view(),name='timeslot'),
    path('timeslotList/<int:teacher_id>',views.TimeSlotListAPIView.as_view(),name='timeslotList'),
    path('timeslotListavailable/<int:teacher_id>',views.TimeSlotAvailableListAPIView.as_view(),name='timeslotListavailable'),
    path('timeslotListoccupied/<int:teacher_id>',views.TimeSlotOccupiedListAPIView.as_view(),name='timeslotListoccupied'),

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
    path('activate_admin/<uidb64>/<token>/',
         views.ActivateAccountAdmin.as_view(), name='activate_admin'),

    path('login/', views.LoginView.as_view(), name='login'),
    path('profile/', views.TeacherProfileView.as_view(), name='profile'),
    path('find_teachers/', views.find_teachers, name='find_teachers'),

#     path('api/teachers/search/',views.TeacherSearchView.as_view(), name='teacher-search'),
# admin
    path('registeredTeacherList/',views.RegisteredTeacherList.as_view(),name='registeredTeacherList'),
    path('verifiedTeacherList/',views.VerifiedTeacherList.as_view(),name='verifiedTeacherList'),
    path('registered_teachers/<int:teacher_id>/verification/', views.RegisteredTeacherVerificationView.as_view(), name='teacher-verification'),
    path('registered_teachers/<int:teacher_id>/preview-certificate/', views.RegisteredTeacherPreviewCertificateView.as_view(), name='teacher-certificate'),
    path('registeredStudentList/',views.RegisteredStudentList.as_view(),name='registeredStudentList'),
    path('blockUser/<int:user_id>',views.BlockUserView.as_view(),name='blockUser'),
    path('UnblockUser/<int:user_id>',views.UnBlockUserView.as_view(),name='unblockUser'),

#student
    path('student-history/<int:student_id>', views.StudentHistoryAPIView.as_view(),name = 'student-history'),  
    path('student-notification/<int:student_id>', views.StudentNotificationAPIView.as_view(),name = 'student-notification'),  
    path('seen-notification/<int:student_id>', views.SeenNotificationAPIView.as_view(),name = 'seen-notification'), 
    path('studentprofile/<int:pk>/', views.StudentProfileView.as_view(), name='student-profile'),
    path('studentProfileGet/<int:student_id>',views.StudentProfileGetAPIView.as_view(),name='studentProfileGet'),
    path('studentprofileUpdate/<int:studentId>', views.StudentProfileUpdateView.as_view(),name = 'studentprofileUpdate'),  

 

#teacher
    path('teacherprofileUpdate/<int:teacherId>', views.TeacherProfileUpdateView.as_view(),name = 'teacherprofileUpdate'),  
    path('teacherteachingInfoUpdate/<int:teacherId>', views.TeacherTeachingInfoUpdateView.as_view(),name = 'teacherprofileUpdate'),  
    path('teachercertificateUpdate/<int:teacherId>', views.TeacherCertificateUpdateView.as_view(),name = 'teachercertificateUpdate'),
    path('teacher-notification/<int:teacher_id>', views.TeacherNotificationAPIView.as_view(),name = 'teacher-notification'),  
    path('teacherseen-notification/<int:teacher_id>', views.TeacherSeenNotificationAPIView.as_view(),name = 'teacherseen-notification'),  


]
