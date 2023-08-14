import logging
from multiprocessing import AuthenticationError
from telnetlib import AUTHENTICATION
from django.conf import settings
from django.http import HttpResponse, JsonResponse, StreamingHttpResponse
from .serializers import AddTeacherSerializer, AdminRegisterSerializer, ChangePasswordSerializer, ChangePasswordVerifySerializer, ClassSerializer, ClassSubjectSerializer, EnrollmentSerializer, ResetPasswordSerializer, ResetPasswordVerifySerializer, StudentNotificationSerializer, StudentProfileSerializer, StudentRegisterSerializer, StudentSerializer, SubjectSerializer,Class, TeacherDetailSerializer, TeacherNotificationSerializer, TeacherSerializer,TeacherRegisterSerializer,LoginSerializer, TeacherUpdateSerializer, TimeSlotSerializer
from rest_framework import generics,status
from rest_framework.generics import ListAPIView
from .models import ChangePasswordVerify, ClassSubject, EnrollmentForm, ResetPassword, ResetPasswordVerify, Student, Student_Notification, Subject, Teacher, Teacher_Notification, TimeSlot, User_Admin
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from .tokens import account_activation_token
from django.template.loader import render_to_string
from django.core.mail import send_mail
from rest_framework.response import Response
from django.views import View
from django.contrib import messages
from rest_framework.exceptions import NotFound, ValidationError
from django.contrib.auth import login
from rest_framework_simplejwt.tokens import RefreshToken
from django.urls import reverse_lazy
from django.shortcuts import redirect
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import RedirectView
import random
import string
from rest_framework.generics import get_object_or_404




# Create your views here.

class TeacherSignupView(generics.CreateAPIView):
    serializer_class = TeacherRegisterSerializer

    def create(self,request,*args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            # user = serializer.save()
            user = serializer.save()  
            user.is_active = False  

            context={
                'user':user,
                'domain':"127.0.0.1:8000",
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            }

            subject = 'Activation Message'
            from_email = settings.EMAIL_HOST_USER
            recipient_list = (serializer.validated_data['email'],)
            html= render_to_string('users/user_verify.html',context=context)
            send_mail(subject=subject,message=None,from_email=from_email,recipient_list=recipient_list,html_message=html) 
            # return HttpResponse(data={'message': 'Please confirm your email address to complete the registration.'})
            # return HttpResponse("Please confirm your email address to complete the registration.")
 
            return Response(
                {
                    "success":"Please confirm your email address to complete the registration."},

                    status=status.HTTP_201_CREATED           
            ) 

import secrets

class AddTeacherView(generics.CreateAPIView):
    serializer_class = AddTeacherSerializer

    def create(self,request,*args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            # user = serializer.save()
            user = serializer.save()
            generated_password = str(secrets.randbelow(10**8)).zfill(8)  
            user.set_password(generated_password)
            user.is_active = False
            user.save()  

            context={
                'user':user,
                'password':generated_password,
                'domain':"127.0.0.1:8000",
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            }

            subject = 'Activation Message'
            from_email = settings.EMAIL_HOST_USER
            recipient_list = (serializer.validated_data['email'],)
            html= render_to_string('users/addTeacher.html',context=context)
            send_mail(subject=subject,message=None,from_email=from_email,recipient_list=recipient_list,html_message=html) 
            # return HttpResponse(data={'message': 'Please confirm your email address to complete the registration.'})
            # return HttpResponse("Please confirm your email address to complete the registration.")
 
            return Response(
                {
                    "success":"Please confirm your email address to complete the registration."},

                    status=status.HTTP_201_CREATED           
            ) 

        
class StudentSignupView(generics.CreateAPIView):
    serializer_class = StudentRegisterSerializer

    def create(self,request,*args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()

            context={
                'user':user,
                'domain':"127.0.0.1:8000",
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            }

            subject = 'Activation Message'
            from_email = settings.EMAIL_HOST_USER
            recipient_list = (serializer.validated_data['email'],)
            html= render_to_string('users/student_verify.html',context=context)
            send_mail(subject=subject,message=None,from_email=from_email,recipient_list=recipient_list,html_message=html) 
            # return HttpResponse(data={'message': 'Please confirm your email address to complete the registration.'})
            # return HttpResponse("Please confirm your email address to complete the registration.")
 
            return Response(
                {
                    "success":"Please confirm your email address to complete the registration."},

                    status=status.HTTP_201_CREATED           
            ) 

class AdminSignupView(generics.CreateAPIView):
    serializer_class = AdminRegisterSerializer

    def create(self,request,*args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()

            context={
                'user':user,
                'domain':"127.0.0.1:8000",
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            }

            subject = 'Activation Message'
            from_email = settings.EMAIL_HOST_USER
            recipient_list = (serializer.validated_data['email'],)
            html= render_to_string('users/admin_verify.html',context=context)
            send_mail(subject=subject,message=None,from_email=from_email,recipient_list=recipient_list,html_message=html) 
 
            return Response(
                {
                    "success":"Please confirm your email address to complete the registration."},

                    status=status.HTTP_201_CREATED           
            ) 


class ActivateAccount(View):

    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid_bytes = urlsafe_base64_decode(uidb64)
            uid = uid_bytes.decode('utf-8')
            # uid = str(urlsafe_base64_decode(uidb64))
            user = Teacher.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, Teacher.DoesNotExist):
            user = None
        if user is not None and  account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)

            messages.success(request, 'Your account have been confirmed.')
            print("Your account have been confirmed")
            return redirect('login')

        else:
            messages.warning(
                request, 'The confirmation link was invalid, possibly because it has already been used.')
            return redirect('teachersign')
        
class ActivateAccountStudent(View):

    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid_bytes = urlsafe_base64_decode(uidb64)
            uid = uid_bytes.decode('utf-8')
            # uid = str(urlsafe_base64_decode(uidb64))
            user = Student.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, Student.DoesNotExist):
            user = None
        if user is not None and  account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)

            messages.success(request, 'Your account have been confirmed.')
            print("Your account have been confirmed")
            return redirect('login')

        else:
            messages.warning(
                request, 'The confirmation link was invalid, possibly because it has already been used.')
            return redirect('studentsign')

class ActivateAccountAdmin(View):

    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid_bytes = urlsafe_base64_decode(uidb64)
            uid = uid_bytes.decode('utf-8')
            # uid = str(urlsafe_base64_decode(uidb64))
            user = User_Admin.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User_Admin.DoesNotExist):
            user = None
        if user is not None and  account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)

            messages.success(request, 'Your account have been confirmed.')
            print("Your account have been confirmed")
            return redirect('login')

        else:
            messages.warning(
                request, 'The confirmation link was invalid, possibly because it has already been used.')
            return redirect('adminsign')

from django.contrib.auth import authenticate
class LoginView(generics.CreateAPIView):
    serializer_class = LoginSerializer
    success_url = reverse_lazy('login')

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            try:
                admin = User_Admin.objects.get(email=serializer.validated_data['email'])
                user = admin
                user_type = 'admin'
            except User_Admin.DoesNotExist:
            # admin = authenticate(request,email = email,password = password)
            
            # if admin is not None:
            #     login(request,admin)
            #     return Response({'message': 'Admin logged in successfully'})
            # else:
  
                try:
                    teacher = Teacher.objects.get(email=serializer.validated_data['email'])
                    user = teacher
                    user_type = 'teacher'
                except Teacher.DoesNotExist:
                    try:
                        student = Student.objects.get(email=serializer.validated_data['email'])
                        user = student
                        user_type = 'student'
                    except Student.DoesNotExist:
                        raise NotFound({'email': ['User with provided email does not exist']})

            if not user.check_password(serializer.validated_data['password']):
                    raise ValidationError({'password': ["incorrect password"]})
            token = RefreshToken.for_user(user)
            if user.is_active:
                login(request, user)
                if user_type == 'teacher':
                    image_url = ''
                    if teacher.image:
                        image_url = settings.MEDIA_URL + str(teacher.image)
                    response_data = {'refresh': str(token),
                                    'access': str(token.access_token),
                                    'user_id': teacher.id,
                                    'full_name':teacher.full_name,
                                    'image':image_url,
                                    'user_type': 'teacher'}
                    return Response(response_data, status=status.HTTP_200_OK)
                elif user_type == 'admin':
                    response_data = {'refresh': str(token),
                                    'access': str(token.access_token),
                                    'user_id': admin.id,
                                    'user_type': 'admin'}
                                        
                    return Response(response_data, status=status.HTTP_200_OK)                
                else :
                    response_data = {'refresh': str(token),
                                    'access': str(token.access_token),
                                    'user_id': student.id,
                                    'user_type': 'student'}
                    return Response(response_data, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Please verify your account'}, status=status.HTTP_401_UNAUTHORIZED)
            
class ResetPasswordAPIView(generics.CreateAPIView):
    serializer_class = ResetPasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email'].lower()
        try:
            user = Teacher.objects.get(email=email)
            code = ''.join(
                random.choices(string.ascii_uppercase + string.digits, k=4)) 
            user_password_reset = ResetPassword.objects.create(
                pw_reset_user=user, code=code)
            context = {
                'user': user.email,
                'code': user_password_reset.code
            }
            subject = "Password Reset Code for TutorApp"
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [user.email]
            send_mail(
                subject=subject,
                message=f'Greetings, Hope you are doing well.Following is the code of {user} for password reset: {code} for the TutorApp',
                from_email=from_email,
                recipient_list=recipient_list)
            return Response("Please check your email to reset your password.", status=status.HTTP_201_CREATED)
        except Teacher.DoesNotExist:
            return Response({"errors": {"User does not exist."}}, status=status.HTTP_404_NOT_FOUND)


class ResetPasswordVerifyAPIView(generics.GenericAPIView):
    serializer_class = ResetPasswordVerifySerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        reset_code = serializer.validated_data['reset_code']
        try:
            user_for_pw_reset = ResetPassword.objects.get(code=reset_code)

            if reset_code == user_for_pw_reset.code:
                user_for_pw_reset.pw_reset_user.set_password(
                    serializer.validated_data["new_password"])
                user_for_pw_reset.pw_reset_user.save()
                user_for_pw_reset.delete()
                return Response(f'Password for {user_for_pw_reset.pw_reset_user} is changed successfully')
        except ResetPassword.DoesNotExist:
            raise NotFound(
                f'Please re-check your email. Reset code expired or incorrect.')
#Testing
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType

class ResetPasswordView(generics.CreateAPIView):
    serializer_class = ResetPasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email'].lower()
        try:
            user_model = None
            user = None

            teacher_model = Teacher.objects.filter(email=email).first()
            student_model = Student.objects.filter(email = email).first()
            user_admin_model = User_Admin.objects.filter(email = email).first()

            if teacher_model:
                user_model = Teacher
                user = teacher_model

            elif student_model:
                user_model = Student
                user = student_model
            elif user_admin_model:
                user_model = User_Admin
                user = user_admin_model

            else:
                return Response({"errors":{"User doest not exist."}},status=status.HTTP_404_NOT_FOUND)            

            code = ''.join(
                random.choices(string.ascii_uppercase + string.digits, k=4)) 
            content_type = ContentType.objects.get_for_model(user_model)
            user_password_reset = ResetPasswordVerify.objects.create(
                content_type = content_type,object_id = user.id, code=code)
            context = {
                'user': user.email,
                'code': user_password_reset.code
            }
            subject = "Password Reset Code for TutorApp"
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [user.email]
            send_mail(
                subject=subject,
                message=f'Greetings, Hope you are doing well.Following is the code of {user} for password reset: {code} for the TutorApp',
                from_email=from_email,
                recipient_list=recipient_list)
            return Response("Please check your email to reset your password.", status=status.HTTP_201_CREATED)
        except Teacher.DoesNotExist:
            return Response({"errors": {"User does not exist."}}, status=status.HTTP_404_NOT_FOUND)


class ResetPasswordVerifyView(generics.GenericAPIView):
    serializer_class = ResetPasswordVerifySerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        reset_code = serializer.validated_data['reset_code']
        try:
            user_for_pw_reset = ResetPasswordVerify.objects.get(code=reset_code)

            if reset_code == user_for_pw_reset.code:
                user_for_pw_reset.pw_reset_user.set_password(
                    serializer.validated_data["new_password"])
                user_for_pw_reset.pw_reset_user.save()
                user_for_pw_reset.delete()
                return Response(f'Password for {user_for_pw_reset.pw_reset_user} is changed successfully')
        except ResetPasswordVerify.DoesNotExist:
            raise NotFound(
                f'Please re-check your email. Reset code expired or incorrect.')

#Change Password
from django.contrib.auth.hashers import check_password

class ChangePasswordView(generics.CreateAPIView):
    serializer_class = ChangePasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email'].lower()

        old_password = serializer.validated_data['old_password']
        new_password = serializer.validated_data['new_password']

        current_user = self.request.user

        # if not check_password(old_password, current_user.password):
        #     return Response({"errors":{"Your password didnt match."}},status=status.HTTP_400_BAD_REQUEST)
        try:
            user_model = None
            user = None

            teacher_model = Teacher.objects.filter(email=email).first()
            student_model = Student.objects.filter(email = email).first()
            user_admin_model = User_Admin.objects.filter(email = email).first()

            if teacher_model:
                user_model = Teacher
                user = teacher_model

            elif student_model:
                user_model = Student
                user = student_model
            elif user_admin_model:
                user_model = User_Admin
                user = user_admin_model

            else:
                return Response({"errors":{"User doest not exist."}},status=status.HTTP_404_NOT_FOUND)            

            if not check_password(old_password,user.password):
                return Response({"errors":{"Your password didnt match."}},status = 400)
            code = ''.join(
                random.choices(string.ascii_uppercase + string.digits, k=4)) 
            content_type = ContentType.objects.get_for_model(user_model)
            user_password_reset = ChangePasswordVerify.objects.create(
                content_type = content_type,object_id = user.id, code=code,new_password=new_password)
            context = {
                'user': user.email,
                'code': user_password_reset.code
            }
            subject = "Password Reset Code for TutorApp"
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [user.email]
            send_mail(
                subject=subject,
                message=f'Greetings, Hope you are doing well.Following is the code of {user} for password reset: {code} for the TutorApp',
                from_email=from_email,
                recipient_list=recipient_list)
            return Response("Please check your email to reset your password.", status=status.HTTP_201_CREATED)
        except Teacher.DoesNotExist:
            return Response({"errors": {"User does not exist."}}, status=status.HTTP_404_NOT_FOUND)
        

class ChangePasswordVerifyView(generics.GenericAPIView):
    serializer_class = ChangePasswordVerifySerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        reset_code = serializer.validated_data['reset_code']
        try:
            user_for_pw_reset = ChangePasswordVerify.objects.get(code=reset_code)

            if reset_code == user_for_pw_reset.code:
                user_instance = user_for_pw_reset.pw_reset_user
                new_password = user_for_pw_reset.new_password
                user_instance.set_password(new_password)
                user_instance.save()
                user_for_pw_reset.delete()
                return Response(f'Password for {user_for_pw_reset.pw_reset_user} is changed successfully')
        except ChangePasswordVerify.DoesNotExist:
            raise NotFound(
                f'Please re-check your email. Reset code expired or incorrect.')



class EnrollmentFormView(APIView):
    def post(self, request):
        serializer = EnrollmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success":"Enrollment form is successfully submitted"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class StudentEnrollmentListView(APIView):
    def get(self, request, teacher_id):
        enrollment_forms = EnrollmentForm.objects.filter(tutor_id=teacher_id,confirmation = False,cancellation = False)
        serializer = EnrollmentSerializer(enrollment_forms, many=True)
        return Response(serializer.data)
    

class ConfirmStudentEnrollmentListView(APIView):
    def get(self, request, teacher_id):
        enrollment_forms = EnrollmentForm.objects.filter(tutor_id=teacher_id,confirmation=True)
        serializer = EnrollmentSerializer(enrollment_forms, many=True)
        return Response(serializer.data)
    
class RejectedStudentsEnrollmentListView(APIView):
    def get(self, request, teacher_id):
        enrollment_forms = EnrollmentForm.objects.filter(tutor_id=teacher_id,cancellation = True)
        serializer = EnrollmentSerializer(enrollment_forms, many=True)
        return Response(serializer.data)

class EnrollmentConfirmationView(APIView):
    def post(self, request, enrollment_id):
        try:
            enrollment = EnrollmentForm.objects.get(id=enrollment_id)
            enrollment.confirmation = True
            enrollment.confirmedDate = request.data['confirmedDate']
            enrollment.save()

            if enrollment.student:
                tutor_email = enrollment.tutor.email
                student_email = enrollment.student.email

                tutor_name = enrollment.tutor.full_name
                tutor_number = enrollment.tutor.phone_number
                tutor_gender = enrollment.tutor.gender
                tutor_address = enrollment.tutor.address
                teaching_grade = enrollment.tutor.grade
                teaching_subjects = enrollment.tutor.subjects
                teaching_location =  enrollment.tutor.teaching_location
                teaching_experience = enrollment.tutor.teaching_experience
                tutor_education = enrollment.tutor.education
                teachingstart_timeSlot = enrollment.startTime
                teachingend_timeSlot = enrollment.endTime

                email_body = f'Dear student, your enrollment has been confirmed.Teacher DetailsName:{tutor_name},{tutor_gender}Contact Number{tutor_number}',

                send_mail(
                    'Enrollment Confirmation',
                    f'Dear student, your enrollment has been confirmed.\nTeacher Details\nName:{tutor_name},{tutor_gender}\nContact Number{tutor_number}',                    
                    tutor_email,
                    [student_email],
                    fail_silently=False,
                )
            notification_data = {
                'student_id' : enrollment.student.id,
                'teacher_id' :enrollment.tutor.id,
                'date'       :enrollment.confirmedDate,
                'message'    :"Enrollment Confirmed.",
            }
            notification_serializer = StudentNotificationSerializer(data=notification_data)
            if notification_serializer.is_valid():
                notification_serializer.save() 


            return Response({'message': 'Enrollment confirmed and email sent to the student.'})
        except EnrollmentForm.DoesNotExist:
            return Response({'message': 'Enrollment not found.'}) 
        # except Exception as e:
        #     logging.error(f'Error confirming enrollment: {str(e)}')
        #     return Response({'message': 'An error occurred while confirming enrollment.'})   
        
class EnrollmentCancelView(APIView):
    def post(self, request, enrollment_id):
        try:
            enrollment = EnrollmentForm.objects.get(id=enrollment_id)
            enrollment.cancellation = True
            enrollment.cancelledDate = request.data['cancelledDate']
            enrollment.save()

            if enrollment.student:
                tutor_email = enrollment.tutor.email
                student_email = enrollment.student.email
                send_mail(
                    'Enrollment Cancellation',
                    'Sorry, your enrollment has been cancelled.',
                    tutor_email,
                    [student_email],
                    fail_silently=False,
                )
            notification_data = {
                'student_id' : enrollment.student.id,
                'teacher_id' :enrollment.tutor.id,
                'date'       :enrollment.cancelledDate,
                'message'    :"Enrollment Cancelled.",
            }
            notification_serializer = StudentNotificationSerializer(data=notification_data)
            if notification_serializer.is_valid():
                notification_serializer.save()

            return Response({'message': 'Enrollment cancel and email sent to the student.'})
        except EnrollmentForm.DoesNotExist:
            return Response({'message': 'Enrollment not found.'})    
        
class EnrollmentTuitionFinishedTeachingView(APIView):
    def post(self, request, enrollment_id):
        try:
            enrollment = EnrollmentForm.objects.get(id=enrollment_id)
            enrollment.finishedTeachingDate = request.data['finishedTeachingDate']
            enrollment.save()

            if enrollment.student:
                tutor_email = enrollment.tutor.email
                student_email = enrollment.student.email
                send_mail(
                    'Tuition Finished Teaching Date',
                    f'Tuition will be completed on: {enrollment.finishedTeachingDate} ',
                    tutor_email,
                    [student_email],
                    fail_silently=False,
                )
            notification_data = {
                'student_id' : enrollment.student.id,
                'teacher_id' :enrollment.tutor.id,
                'date'       :enrollment.confirmedDate,
                'message'    :f'Tuition will be completed on: {enrollment.finishedTeachingDate} ',

            }
            notification_serializer = StudentNotificationSerializer(data=notification_data)
            if notification_serializer.is_valid():
                notification_serializer.save()

            return Response({'message': 'Tuition teaching finished date set and email sent to the student.'})
        except EnrollmentForm.DoesNotExist:
            return Response({'message': 'Enrollment not found.'})    

        
class TeacherUpdateView(APIView):
    def put(self, request, pk):
        try:
            teacher = Teacher.objects.get(pk=pk)
            serializer = TeacherUpdateSerializer(teacher, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Teacher updated successfully.'})
            return Response(serializer.errors, status=400)
        except Teacher.DoesNotExist:
            return Response({'message': 'Teacher not found.'}, status=404)        

class TimeSlotView(APIView):
    def post(self,request):
        serializer = TimeSlotSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status = 201)
        print(serializer.errors)
        return Response(serializer.errors,status = 400)

class TimeSlotListAPIView(APIView):
    def get(self,request,teacher_id):
        time_slots = TimeSlot.objects.filter(teacherId = teacher_id)
        serializer = TimeSlotSerializer(time_slots,many = True)
        return Response(serializer.data)
    

class TimeSlotAvailableListAPIView(APIView):
    def get(self,request,teacher_id):
        time_slots = TimeSlot.objects.filter(teacherId = teacher_id)
        enrollment_form = EnrollmentForm.objects.filter(tutor_id = teacher_id,cancellation = False)
        serializer = TimeSlotSerializer(time_slots,many = True)
        matching_time_slots = []
        for time_slot in serializer.data:
                start_time = time_slot['startTime']
                end_time = time_slot['endTime']
                if enrollment_form.filter(startTime=start_time,endTime=end_time).exists():
                    continue
                matching_time_slots.append(time_slot)
        return Response(matching_time_slots)

class TimeSlotOccupiedListAPIView(APIView):
    def get(self,request,teacher_id):
        time_slots = TimeSlot.objects.filter(teacherId = teacher_id)
        enrollment_form = EnrollmentForm.objects.filter(tutor_id = teacher_id,cancellation = False)
        serializer = TimeSlotSerializer(time_slots,many = True)
        matching_time_slots = []
        for time_slot in serializer.data:
                start_time = time_slot['startTime']
                end_time = time_slot['endTime']
                if enrollment_form.filter(startTime=start_time,endTime=end_time).exists():
                    matching_time_slots.append(time_slot)
                continue
        return Response(matching_time_slots)


class TimeSlotDisableAPIView(APIView):
    def post(self,request,slot_id):
        time_slots = TimeSlot.objects.get(id = slot_id)
        time_slots.disable = True
        time_slots.save()
        return Response({'message': 'Time Slot disabled.'})
    
class TimeSlotEnableAPIView(APIView):
    def post(self,request,slot_id):
        time_slots = TimeSlot.objects.get(id = slot_id)
        time_slots.disable = False
        time_slots.save()
        return Response({'message': 'Time Slot enabled.'})


class TeacherProfileAPIView(APIView):
    def get(self,request,teacher_id):
        try:
            teacher = Teacher.objects.get(id = teacher_id)
            serializer = TeacherSerializer(teacher)
            return Response(serializer.data)
        except Teacher.DoesNotExist:
            return Response(
                {
                    'error':'Teacher not found'
                },status=404
            )

class TeacherProfileView(APIView):
    def get(self, request):
        user = request.user
        serializer = TeacherSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class TeacherList(ListAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer

    def get(self,request,*args,**kwargs):
        response = super().get(request,*args,**kwargs)
        teachers = response.data 

        for teacher in teachers:
            teacher_id = teacher['id']
            enrollment_forms = EnrollmentForm.objects.filter(tutor_id=teacher_id,cancellation = False)
            time_slots = TimeSlot.objects.filter(teacherId=teacher_id,disable = False)
            serializer = TimeSlotSerializer(time_slots,many = True) 
            matching_time_slots = []
            for time_slot in serializer.data:
                start_time = time_slot['startTime']
                end_time = time_slot['endTime']
                if enrollment_forms.filter(startTime=start_time,endTime=end_time).exists():
                    continue
                matching_time_slots.append(time_slot)
            teacher['time_slots'] = matching_time_slots
        return response    

    
class StudentList(ListAPIView):
    queryset= Student.objects.all()
    serializer_class = StudentSerializer

class ClassSubjectList(ListAPIView):
    queryset= ClassSubject.objects.all()
    serializer_class = ClassSubjectSerializer

class ClassList(ListAPIView):
    queryset= Class.objects.all()
    serializer_class = ClassSerializer

class SubjectList(ListAPIView):
    queryset= Subject.objects.all()
    serializer_class = SubjectSerializer
    
class ClassSubjectAPIView(APIView):
    def get(self, request):
        class_subjects = ClassSubject.objects.all()
        serializer = ClassSubjectSerializer(class_subjects, many=True)
        data = [item for item in serializer.data if item]
        return Response(data)
    
#Teacher 
class TeacherProfileUpdateView(APIView):
      def put(self,request,teacherId):
          qs = Teacher.objects.all()
          teacher = get_object_or_404(qs,pk=teacherId)
          serializer = TeacherUpdateSerializer(teacher,data = request.data)
          if serializer.is_valid():
              serializer.save()
              return Response({"Success":"Profile Updated Successfully"},status = status.HTTP_200_OK)  
          return Response(status = status.HTTP_400_BAD_REQUEST)

class TeacherTeachingInfoUpdateView(APIView):
      def put(self,request,teacherId):
          qs = Teacher.objects.all()
          teacher = get_object_or_404(qs,pk=teacherId)
          serializer = TeacherUpdateSerializer(teacher,data = request.data)
          if serializer.is_valid():
              serializer.save()
              return Response({"Success":"Profile Updated Successfully"},status = status.HTTP_200_OK)  
          return Response(status = status.HTTP_400_BAD_REQUEST)

class TeacherCertificateUpdateView(APIView):
      def put(self,request,teacherId):
          qs = Teacher.objects.all()
          teacher = get_object_or_404(qs,pk=teacherId)
          serializer = TeacherUpdateSerializer(teacher,data = request.data)
          if serializer.is_valid():
              serializer.save()
              return Response({"Success":"Certificated Uploaded Successfully"},status = status.HTTP_200_OK)  
          return Response(status = status.HTTP_400_BAD_REQUEST)

class TeacherNotificationAPIView(APIView):
    def get(self,request,teacher_id):
        notifications = Teacher_Notification.objects.filter(teacher_id = teacher_id)
        for notification in notifications:
            if not notification.seen:
                notification.seen = True
                notification.save()
        serializer   = TeacherNotificationSerializer(notifications,many = True)
        return Response(serializer.data)
    
class TeacherSeenNotificationAPIView(APIView):
    def get(self,request,teacher_id):
        seen_notifications = Teacher_Notification.objects.filter(teacher_id=teacher_id,seen = False).count()
        response_data = {'notification_count':seen_notifications}
        return Response(response_data)    


#student
class StudentProfileView(APIView):
    def put(self, request, pk):
        try:
            student = Student.objects.get(pk=pk)
            serializer = StudentProfileSerializer(student, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Student profile created successfully.'})
            return Response(serializer.errors, status=400)
        except Teacher.DoesNotExist:
            return Response({'message': 'Student not found.'}, status=404)   

class StudentProfileUpdateView(APIView):
      def put(self,request,studentId):
          qs = Student.objects.all()
          student = get_object_or_404(qs,pk=studentId)
          serializer = StudentProfileSerializer(student,data = request.data)
          if serializer.is_valid():
              serializer.save()
              return Response({"Success":"Profile Updated Successfully"},status = status.HTTP_200_OK)  
          return Response(status = status.HTTP_400_BAD_REQUEST)

class StudentProfileGetAPIView(APIView):
    def get(self,request,student_id):
        try:
            student = Student.objects.get(id = student_id)
            serializer = StudentSerializer(student)
            return Response(serializer.data)
        except Student.DoesNotExist:
            return Response(
                {
                    'error':'Student not found'
                },status=404
            )

class StudentHistoryAPIView(APIView):
    def get(self,request,student_id):
        enrollment_history = EnrollmentForm.objects.filter(student_id = student_id)
        serializer = EnrollmentSerializer(enrollment_history,many = True)
        return Response(serializer.data)

class StudentNotificationAPIView(APIView):
    def get(self,request,student_id):
        notifications = Student_Notification.objects.filter(student_id = student_id)
        for notification in notifications:
            if not notification.seen:
                notification.seen = True
                notification.save()
        serializer   = StudentNotificationSerializer(notifications,many = True)
        return Response(serializer.data)
    
class SeenNotificationAPIView(APIView):
    def get(self,request,student_id):
        seen_notifications = Student_Notification.objects.filter(student_id=student_id,seen = False).count()
        response_data = {'notification_count':seen_notifications}
        return Response(response_data)    

#admin
class RegisteredTeacherList(APIView):
    def get(self,request):
        teachers = Teacher.objects.filter(verification_status = False)
        serializer = TeacherSerializer(teachers,many = True)
        return Response(serializer.data)
    


class VerifiedTeacherList(APIView):
    def get(self,request):
        verified_teacher = Teacher.objects.filter(verification_status = True)
        serializer = TeacherSerializer(verified_teacher,many = True)
        return Response(serializer.data)   

class RegisteredTeacherVerificationView(APIView):
    def post(self, request, teacher_id):
        try:
            teacher = Teacher.objects.get(id=teacher_id)
            teacher.verification_status = True
            teacher.verification_date = request.data['verification_date']
            teacher.save()
            teacher_email = teacher.email
            send_mail(
                    'Your details have been verified', 
                    'Visit the Tutor App',                  
                    'aayushshah99a@gmail.com',
                    [teacher_email],
                    fail_silently=False,
                )
            notification_data = {
                'teacher_id' :teacher_id,
                'date'       :teacher.verification_date,
                'message'    :"Congratulation,Your details have been Verified",
            }
            notification_serializer = TeacherNotificationSerializer(data=notification_data)
            if notification_serializer.is_valid():
                notification_serializer.save() 

                
            return Response({'message': 'Teacher verified successfully.'})
        except Teacher.DoesNotExist:
            return Response({'message': 'Teacher not found.'})    

class RegisteredTeacherPreviewCertificateView(APIView):
    def post(self, request, teacher_id):
        try:
            teacher = Teacher.objects.get(id=teacher_id)
            teacher.preview_certificate = True
            teacher.preview_certificateDate = request.data['preview_certificateDate']

            teacher.save()
            teacher_email = teacher.email
            send_mail(
                    'There might be mistake regarding your details', 
                    'Visit the Tutor App and preview your certificate also if any mistake then re-uplaod it',                  
                    'aayushshah99a@gmail.com',
                    [teacher_email],
                    fail_silently=False,
                )
            notification_data = {
                'teacher_id' :teacher.id,
                'date'       :teacher.preview_certificateDate,
                'message'    :"Please check your educational certificate and re-upload it for further verification process",
                'previewCertificate':True
            }
            notification_serializer = TeacherNotificationSerializer(data=notification_data)
            if notification_serializer.is_valid():
                notification_serializer.save() 

                
            return Response({'message': 'Preview your certificate message has been sent successfully.'})
        except Teacher.DoesNotExist:
            return Response({'message': 'Teacher not found.'})    


class RegisteredStudentList(APIView):
    def get(self,request):
        student = Student.objects.all()
        serializer = StudentSerializer(student,many = True)
        return Response(serializer.data)
    
#block the user

class BlockUserView(APIView):
    def post(self, request, user_id):
        try:
            user_model = None
            user_email = None
            student = Student.objects.filter(id=user_id).first()
            teacher = Teacher.objects.filter(id=user_id).first()
            if teacher:
                user_model = teacher
                user_model.block = True
                user_model.is_active = False
                user_model.save()
                user_email = user_model.email
            elif student:
                user_model = student
                user_model.block = True
                user_model.is_active = False
                user_model.save()
                user_email = user_model.email
            else:
                return Response({"errors":{"User does not exist."}},status=status.HTTP_404_NOT_FOUND)    
            send_mail(
                    'This to inform that', 
                    'Your account on Tutor App has been blocked by Admin.You  can contact at this number: 9812325311',                  
                    settings.EMAIL_HOST_USER,
                    [user_email],
                    fail_silently=False,
                )


            return Response({'message': 'Account on Tutor App has been blocked.'})
        except Teacher.DoesNotExist:
            return Response({'message': 'Teacher not found.'})    


class UnBlockUserView(APIView):
    def post(self, request, user_id):
        try:
            user_model = None
            user_email = None
            student = Student.objects.filter(id=user_id).first()
            teacher = Teacher.objects.filter(id=user_id).first()
            if teacher:
                user_model = teacher
                user_model.block = False
                user_model.is_active = True
                user_model.save()
                user_email = user_model.email
            elif student:
                user_model = student
                user_model.block = False
                user_model.is_active = True
                user_model.save()
                user_email = user_model.email
            else:
                return Response({"errors":{"User does not exist."}},status=status.HTTP_404_NOT_FOUND)    
            send_mail(
                    'This to inform that', 
                    'Your account on Tutor App has been activated by Admin which was blocked.You  can contact at this number: 9812325311',                  
                    settings.EMAIL_HOST_USER,
                    [user_email],
                    fail_silently=False,
                )


            return Response({'message': 'Account on Tutor App has been blocked.'})
        except Teacher.DoesNotExist:
            return Response({'message': 'Teacher not found.'})    

# class BlockUserView(APIView):
#     def post(self, request, user_id):
#         try:
#             teacher = Teacher.objects.get(id=user_id)
#             teacher.block = True
#             teacher.is_active = False 
#             teacher.save()
#             teacher_email = teacher.email
#             send_mail(
#                     'This to inform that', 
#                     'Your account on Tutor App has been blocked by Admin.You  can contact at this number: 9812325311',                  
#                     settings.EMAIL_HOST_USER,
#                     [teacher_email],
#                     fail_silently=False,
#                 )


#             return Response({'message': 'Account on Tutor App has been blocked.'})
#         except Teacher.DoesNotExist:
#             return Response({'message': 'Teacher not found.'})    








from django.http import JsonResponse
from math import radians, sin, cos, sqrt, atan2
from .models import Teacher
from django.views.decorators.csrf import csrf_exempt

# @csrf_exempt
# def find_teachers(request):
#     if request.method == 'POST':
#         latitude = float(request.POST.get('latitude'))
#         longitude = float(request.POST.get('longitude'))
#         selectedClass=request.POST.get('class')
#         selectedSubjects=request.POST.get('subjects')
#         print(".......................................")
#         print(latitude)
#         print(longitude)
#         print(selectedClass)
#         print(selectedSubjects)


#         # Haversine Formula to calculate distance
#         def calculate_distance(lat1, lon1, lat2, lon2):
#             R = 6371  # Radius of the Earth in kilometers
#             dlat = radians(float(lat2) - float(lat1))
#             dlon = radians(float(lon2) - float(lon1))
#             a = sin(dlat / 2) ** 2 + cos(radians(float(lat1))) * cos(radians(float(lat2))) * sin(dlon / 2) ** 2
#             c = 2 * atan2(sqrt(a), sqrt(1 - a))
#             distance = R * c
#             print("......................................................")
#             print(distance)
#             return distance
#         # Find teachers within 3 km radius and along with grade and subjects

#         teachers = Teacher.objects.all()
#         nearby_teachers = []
#         matching_time_slots = []

#         for teacher in teachers:
#             #
#             teacher_id = teacher.id
#             print(teacher_id)
#             enrollment_forms = EnrollmentForm.objects.filter(tutor_id=teacher_id,cancellation = False)
#             time_slots = TimeSlot.objects.filter(teacherId=teacher_id,disable = False)
#             serializer = TimeSlotSerializer(time_slots,many = True) 
#             # matching_time_slots = []
#             for time_slot in serializer.data:
#                 start_time = time_slot['startTime']
                
#                 end_time = time_slot['endTime']
#                 if enrollment_forms.filter(startTime=start_time,endTime=end_time).exists():
#                     continue
#                 matching_time_slots.append(time_slot)
#                 print(matching_time_slots)
#             slots = matching_time_slots    
#             #
#             teacher_latitude = teacher.latitude
#             teacher_longitude = teacher.longitude
#             teacher_class = teacher.grade
#             teacher_subjects = teacher.subjects.split(',')
#             distance = calculate_distance(latitude, longitude, teacher_latitude, teacher_longitude)
#             if distance <= 3 and selectedClass==teacher_class and any(subject in selectedSubjects for subject in teacher_subjects): 
#             # and selectedClass == teacher_class and any(subject in teacher_subjects for subject in selectedSubjects):
#                 nearby_teachers.append(teacher)
#             # print(matching_time_slots)

#         # Return the list of nearby teachers
#         teacher_data = [{'name': teacher.full_name,
#                         'latitude': teacher.latitude, 
#                          'longitude': teacher.longitude,
#                          'grade': teacher.grade,
#                          'subjects': teacher.subjects,
#                          'email':teacher.email,
#                          'phone_number':teacher.phone_number,
#                          'id':teacher.id,
#                          'teaching_location':teacher.teaching_location,
#                          'teaching_experience':teacher.teaching_experience,
#                          'education':teacher.education,
#                          'address':teacher.address,
#                          'gender':teacher.gender,
#                          'image':teacher.image.url if teacher.image else None,
#                          'time_slots':slots
                         

                         
#                          }
#                         for teacher in nearby_teachers]
        

#         # print(teacher.image)
#         # print(teacher_data)
#         # print(teacher.full_name)
#         # print(teacher_data)
#         # print(teacher_class)
#         # print(teacher_subjects)
#         print(matching_time_slots)
#         print(f"Teacher: {teacher.full_name}")
#         for slot in matching_time_slots:
#             print(f"  Start Time: {slot['startTime']}, End Time: {slot['endTime']}")


#         response = {
#             'teachers': teacher_data
#         }

#         return JsonResponse(response)
#     return HttpResponse('Method not allowed', status=405)


#Testing
@csrf_exempt
def find_teachers(request):
    if request.method == 'POST':
        latitude = float(request.POST.get('latitude'))
        longitude = float(request.POST.get('longitude'))
        selectedClass=request.POST.get('class')
        selectedSubjects=request.POST.get('subjects')
        print(".......................................")
        print(latitude)
        print(longitude)
        print(selectedClass)
        print(selectedSubjects)


        # Haversine Formula to calculate distance
        def calculate_distance(lat1, lon1, lat2, lon2):
            R = 6371  # Radius of the Earth in kilometers
            dlat = radians(float(lat2) - float(lat1))
            dlon = radians(float(lon2) - float(lon1))
            a = sin(dlat / 2) ** 2 + cos(radians(float(lat1))) * cos(radians(float(lat2))) * sin(dlon / 2) ** 2
            c = 2 * atan2(sqrt(a), sqrt(1 - a))
            distance = R * c
            print("......................................................")
            print(distance)
            return distance
        # Find teachers within 3 km radius and along with grade and subjects

        teachers = Teacher.objects.all()
        nearby_teachers = []
        matching_slots = {}

        for teacher in teachers:
            #
            teacher_id = teacher.id
            print(teacher_id)
            enrollment_forms = EnrollmentForm.objects.filter(tutor_id=teacher_id,cancellation = False)
            time_slots = TimeSlot.objects.filter(teacherId=teacher_id,disable = False)
            serializer = TimeSlotSerializer(time_slots,many = True) 
            matching_time_slots = []
            for time_slot in serializer.data:
                start_time = time_slot['startTime']
                
                end_time = time_slot['endTime']
                if enrollment_forms.filter(startTime=start_time,endTime=end_time).exists():
                    continue
                matching_time_slots.append(time_slot)
                print(matching_time_slots)
            slots = matching_time_slots    
            #
            teacher_latitude = teacher.latitude
            teacher_longitude = teacher.longitude
            teacher_class = teacher.grade
            teacher_subjects = teacher.subjects.split(',')
            distance = calculate_distance(latitude, longitude, teacher_latitude, teacher_longitude)
            if distance <= 3 and selectedClass==teacher_class and any(subject in selectedSubjects for subject in teacher_subjects): 
            # and selectedClass == teacher_class and any(subject in teacher_subjects for subject in selectedSubjects):
                nearby_teachers.append(teacher)
                matching_slots[teacher] = matching_time_slots

            print(matching_time_slots)

        if not nearby_teachers:
            
            response = {
                'message':"No nearby teachers found",
                'teachers': []
            }
            print(response)
        # Return the list of nearby teachers
        else:
            teacher_data = [{'name': teacher.full_name,
                        'latitude': teacher.latitude, 
                         'longitude': teacher.longitude,
                         'grade': teacher.grade,
                         'subjects': teacher.subjects,
                         'email':teacher.email,
                         'phone_number':teacher.phone_number,
                         'id':teacher.id,
                         'teaching_location':teacher.teaching_location,
                         'teaching_experience':teacher.teaching_experience,
                         'education':teacher.education,
                         'address':teacher.address,
                         'gender':teacher.gender,
                         'image':teacher.image.url if teacher.image else None,
                         'time_slots':matching_slots.get(teacher,[])
                         

                         
                         }
                        for teacher in nearby_teachers]
            response = {
            'teachers': teacher_data
        }

            return JsonResponse(response)


        # print(teacher.image)
        # print(teacher_data)
        # print(teacher.full_name)
        # print(teacher_data)
        # print(teacher_class)
        # print(teacher_subjects)
        print(matching_time_slots)
        print(f"Teacher: {teacher.full_name}")
        for slot in matching_time_slots:
            print(f"  Start Time: {slot['startTime']}, End Time: {slot['endTime']}")


    return HttpResponse('Method not allowed', status=405)