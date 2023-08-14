from collections import OrderedDict
import json
from django.http import HttpResponse, JsonResponse
from rest_framework import serializers
from .models import ClassSubject, EnrollmentForm, Student, Student_Notification, Subject, Teacher,Class, Teacher_Notification, TimeSlot, User_Admin
from django.contrib.auth import get_user_model,password_validation,authenticate


# Teacher = get_user_model()

class TeacherRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
                style={'input_type': 'password'}

    )
    password_confirmation = serializers.CharField(
        style={'input_type': 'password'}, write_only=True
    )

    class Meta:
        model= Teacher
        fields= ['full_name','email','phone_number','image',
                'address','password','password_confirmation','gender',
                'grade','subjects','latitude','longitude','certificate'
                            
                ]
        read_only_fields = [ 'groups', 'user_permissions']
    

    def create(self, validated_data):
        validated_data.pop('password_confirmation')
        teacher = Teacher.objects.create_user(**validated_data)
        return teacher

    def validate(self, data):
        try:
            password = data["password"]
            password_c = data["password_confirmation"]
        except KeyError as e:
            print(e)
        else:
            if password != password_c:
                raise serializers.ValidationError(
                    "Doesn't match. Please confirm your password.")
            password_validation.validate_password(password)
            return data

class AddTeacherSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
                style={'input_type': 'password'},read_only=True

    )

    class Meta:
        model= Teacher
        fields= ['full_name','email','phone_number','image',
                'address','password','gender',
                'grade','subjects','latitude','longitude','certificate'
                            
                ]
        read_only_fields = [ 'groups', 'user_permissions']
    

    def create(self, validated_data):
        password = self.context.get('password')
        teacher = Teacher.objects.create_user(password=password,**validated_data)
        return teacher


class StudentRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
                style={'input_type': 'password'}

    )
    password_confirmation = serializers.CharField(
        style={'input_type': 'password'}, write_only=True
    )

    class Meta:
        model= Student
        fields= ['email','password','password_confirmation'
                            
                ]

        # read_only_fields = [ 'groups', 'user_permissions']
    

    def create(self, validated_data):
        validated_data.pop('password_confirmation')
        teacher = Student.objects.create_user(**validated_data)
        return teacher

    def validate(self, data):
        try:
            password = data["password"]
            password_c = data["password_confirmation"]
        except KeyError as e:
            print(e)
        else:
            if password != password_c:
                raise serializers.ValidationError(
                    "Doesn't match. Please confirm your password.")
            password_validation.validate_password(password)
            return data

class AdminRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
                style={'input_type': 'password'}

    )
    password_confirmation = serializers.CharField(
        style={'input_type': 'password'}, write_only=True
    )

    class Meta:
        model= User_Admin
        fields= ['email','password','password_confirmation'
                            
                ]

        # read_only_fields = [ 'groups', 'user_permissions']
    

    def create(self, validated_data):
        validated_data.pop('password_confirmation')
        admin = User_Admin.objects.create_user(**validated_data)
        return admin

    def validate(self, data):
        try:
            password = data["password"]
            password_c = data["password_confirmation"]
        except KeyError as e:
            print(e)
        else:
            if password != password_c:
                raise serializers.ValidationError(
                    "Doesn't match. Please confirm your password.")
            password_validation.validate_password(password)
            return data



class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'}, write_only=True
    )

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            try:
                user = Teacher.objects.get(email=email)
                user_type = 'teacher'
            except Teacher.DoesNotExist:
                try:
                    user = Student.objects.get(email=email)
                    user_type = 'student'
                except Student.DoesNotExist:
                    # raise serializers.ValidationError({'email': 'User with provided email does not exist'})
                    try:
                        # user=User.objects.get(email = email)
                        user = User_Admin.objects.get(email=email)
                        user_type='admin'
                    except User_Admin.DoesNotExist:
                        raise serializers.ValidationError({'email': 'User with provided email does not exist'})

            user = authenticate(email=email, password=password)

            # if not user:
            #     raise serializers.ValidationError({'credentials': 'Invalid credentials'})

            # if not user.is_active:
            #     raise serializers.ValidationError({'status': 'Account is not active'})

            data['user'] = user
            data['user_type'] = user_type
            # data['admin'] = admin
            return data
        else:
            raise serializers.ValidationError({'credentials': 'Must include "email" and "password".'})

class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ResetPasswordVerifySerializer(serializers.Serializer):
    reset_code = serializers.CharField()
    new_password = serializers.CharField(style={'input_type': 'password'})

class ChangePasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    old_password = serializers.CharField(style={'input_type':'password'})
    new_password = serializers.CharField(style={'input_type':'password'})

class ChangePasswordVerifySerializer(serializers.Serializer):  
    reset_code = serializers.CharField()  

class TimeSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSlot
        fields = '__all__'          


class TeacherSerializer(serializers.ModelSerializer):
    time_slots = TimeSlotSerializer(many=True, read_only=True)

    class Meta:
        model=Teacher
        fields='__all__'
        
class TeacherUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['phone_number','address','gender','education','teaching_experience','teaching_location','grade','subjects','about_me','image',
                  'latitude','longitude','certificate'
                  
                  ]   
        
class TeacherDetailSerializer(serializers.ModelSerializer):
    address = serializers.CharField(required=False)  
    gender = serializers.CharField(required=False)  

    class Meta:
        model = Teacher
        fields = '__all__'

        
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Student
        fields=['id','email','date_joined','name','number','parents_name','parents_number','gender','block','address','latitude','longitude'
                ]

class StudentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=Student
        fields=['name','number','parents_name','parents_number','gender','address','latitude','longitude'
                ]


class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model=EnrollmentForm
        fields = '__all__'     

class StudentNotificationSerializer(serializers.ModelSerializer):
    teacher = TeacherSerializer(source = 'teacher_id',read_only = True)
    class Meta:
        model = Student_Notification
        fields = ['id','student_id','teacher_id','message','seen','date','teacher']          

class TeacherNotificationSerializer(serializers.ModelSerializer):
    teacher = TeacherSerializer(source = 'teacher_id',read_only = True)
    class Meta:
        model = Teacher_Notification
        fields = ['id','teacher_id','message','seen','date','teacher','previewCertificate','verified']          



class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'

class ClassSubjectSerializer(serializers.ModelSerializer):
    class_name = serializers.StringRelatedField(source='class_name.name')
    subjects = serializers.SerializerMethodField()

    class Meta:
        model = ClassSubject
        fields = ['id', 'class_name_id', 'class_name', 'subjects']

    def get_subjects(self, obj):
        subjects = Subject.objects.filter(classsubject__class_name_id=obj.class_name_id).distinct()
        return SubjectSerializer(subjects, many=True).data

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        class_name_id = representation['class_name_id']
        if 'class_names' not in self.context:
            self.context['class_names'] = set()
        if class_name_id in self.context['class_names']:
            return None
        self.context['class_names'].add(class_name_id)
        return representation
    


class ClassSerializer(serializers.ModelSerializer):

    class Meta:
        model = Class
        fields = '__all__'

            