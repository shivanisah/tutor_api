import logging
from multiprocessing import AuthenticationError
from telnetlib import AUTHENTICATION
from django.conf import settings
from django.http import HttpResponse, JsonResponse, StreamingHttpResponse
from .serializers import ClassSerializer, ClassSubjectSerializer, EnrollmentSerializer, StudentRegisterSerializer, StudentSerializer, SubjectSerializer,Class, TeacherDetailSerializer, TeacherSerializer,TeacherRegisterSerializer,LoginSerializer, TeacherUpdateSerializer, TimeSlotSerializer
from rest_framework import generics,status
from rest_framework.generics import ListAPIView
from .models import ClassSubject, EnrollmentForm, Student, Subject, Teacher, TimeSlot
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




# Create your views here.

class TeacherSignupView(generics.CreateAPIView):
    serializer_class = TeacherRegisterSerializer

    def create(self,request,*args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            # user = serializer.save()
            user = serializer.save()  # Create user instance but don't save it yet
            user.is_active = False  # Mark the user as inactive

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

from django.contrib.auth import authenticate
class LoginView(generics.CreateAPIView):
    serializer_class = LoginSerializer
    success_url = reverse_lazy('login')

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            

            admin = authenticate(request,email = email,password = password)
            
            if admin is not None:
                login(request,admin)
                return Response({'message': 'Admin logged in successfully'})
            else:
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
                    else:
                        response_data = {'refresh': str(token),
                                        'access': str(token.access_token),
                                        'user_id': student.id,
                                        'user_type': 'student'}
                    return Response(response_data, status=status.HTTP_200_OK)
                else:
                    return Response({'error': 'Please verify your account'}, status=status.HTTP_401_UNAUTHORIZED)
            
# @method_decorator(login_required, name='dispatch')


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
        enrollment_forms = EnrollmentForm.objects.filter(tutor_id=teacher_id,confirmation=True,cancellation = False)
        serializer = EnrollmentSerializer(enrollment_forms, many=True)
        return Response(serializer.data)
    
class RejectedStudentsEnrollmentListView(APIView):
    def get(self, request, teacher_id):
        enrollment_forms = EnrollmentForm.objects.filter(tutor_id=teacher_id,cancellation = True)
        serializer = EnrollmentSerializer(enrollment_forms, many=True)
        return Response(serializer.data)

from datetime import datetime  
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
    
# class TeacherList(ListAPIView):
#     queryset= Teacher.objects.all()
#     serializer_class = TeacherSerializer

# class TeacherList(ListAPIView):
#     queryset = Teacher.objects.all()
#     serializer_class = TeacherSerializer

#     def get(self,request,*args,**kwargs):
#         response = super().get(request,*args,**kwargs)
#         teachers = response.data 

#         for teacher in teachers:
#             teacher_id = teacher['id']
#             time_slots = TimeSlot.objects.filter(teacherId=teacher_id)
#             serializer = TimeSlotSerializer(time_slots,many = True) 
#             teacher['time_slots'] = serializer.data 

#         return response 

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

                
            return Response({'message': 'Teacher verified successfully.'})
        except EnrollmentForm.DoesNotExist:
            return Response({'message': 'Teacher not found.'})    

class RegisteredStudentList(APIView):
    def get(self,request):
        student = Student.objects.all()
        serializer = StudentSerializer(student,many = True)
        return Response(serializer.data)

from django.http import JsonResponse
from math import radians, sin, cos, sqrt, atan2
from .models import Teacher
from django.views.decorators.csrf import csrf_exempt

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
        for teacher in teachers:
            teacher_latitude = teacher.latitude
            teacher_longitude = teacher.longitude
            teacher_class = teacher.grade
            teacher_subjects = teacher.subjects.split(',')
            distance = calculate_distance(latitude, longitude, teacher_latitude, teacher_longitude)
            if distance <= 3 and selectedClass==teacher_class and any(subject in selectedSubjects for subject in teacher_subjects): 
            # and selectedClass == teacher_class and any(subject in teacher_subjects for subject in selectedSubjects):
                nearby_teachers.append(teacher)

        # Return the list of nearby teachers
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
                         'gender':teacher.gender

                         
                         }
                        for teacher in nearby_teachers]
        # print(teacher_data)
        # print(teacher.full_name)
        # print(teacher_data)
        # print(teacher_class)
        # print(teacher_subjects)
        response = {
            'teachers': teacher_data
        }

        return JsonResponse(response)
    return HttpResponse('Method not allowed', status=405)