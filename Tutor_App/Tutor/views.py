from multiprocessing import AuthenticationError
from telnetlib import AUTHENTICATION
from django.conf import settings
from django.http import HttpResponse, JsonResponse, StreamingHttpResponse
from .serializers import StudentRegisterSerializer, StudentSerializer, TeacherSerializer,TeacherRegisterSerializer,LoginSerializer
from rest_framework import generics,status
from rest_framework.generics import ListAPIView
from .models import Student, Teacher
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


class LoginView(generics.CreateAPIView):
    serializer_class = LoginSerializer
    success_url = reverse_lazy('login')

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
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
                                    'name':teacher.full_name,
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
class TeacherProfileView(APIView):
    def get(self, request):
        user = request.user
        serializer = TeacherSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class TeacherList(ListAPIView):
    queryset= Teacher.objects.all()
    serializer_class = TeacherSerializer
    
class StudentList(ListAPIView):
    queryset= Student.objects.all()
    serializer_class = StudentSerializer

# class TeacherSearchView(APIView):
#     def get(self,request):
#         classes = Class.objects.all()
#         class_numbers = [class_obj.class_number for class_obj in classes]

#         return Response({'classes': class_numbers})

#     def post(self, request):
#         class_number = request.data.get('class_number')
#         subject_ids = request.data.get('subjects', [])

#         try:
#             class_obj = Class.objects.get(class_number=class_number)
#             subjects = Subject.objects.filter(id__in=subject_ids, classes=class_obj)
#             teachers = Teacher.objects.filter(teaching_grades=class_obj, subject__in=subjects)
#             serializer = TeacherSerializer(teachers, many=True)
#             return Response(serializer.data)
#         except Class.DoesNotExist:
#             return Response({"error": "Invalid class number"}, status=400)
