from rest_framework import serializers
from .models import Student, Teacher
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
                'address','password','password_confirmation','gender'
                            
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

class StudentRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
                style={'input_type': 'password'}

    )
    password_confirmation = serializers.CharField(
        style={'input_type': 'password'}, write_only=True
    )

    class Meta:
        model= Student
        fields= ['full_name','email','phone_number','image',
                'address','grade','subjects','password','password_confirmation'
                            
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


# class LoginSerializer(serializers.Serializer):
#     email = serializers.EmailField()
#     password = serializers.CharField(
#         style={'input_type': 'password'}, write_only=True
#     )
# def validate(self, attrs):
#         email = attrs.get('email')
#         password = attrs.get('password')

#         if email and password:
#             # Check if provided credentials are valid for a Teacher object
#             teacher = authenticate(email=email, password=password, model=Teacher)
#             if teacher:
#                 attrs['user'] = teacher
#                 return attrs

#             # Check if provided credentials are valid for a Student object
#             student = authenticate(email=email, password=password, model=Student)
#             if student:
#                 attrs['user'] = student
#                 return attrs

#             raise serializers.ValidationError('Unable to login with provided credentials')
#         else:
#             raise serializers.ValidationError('Must include email and password')    


# class LoginStudentSerializer(serializers.Serializer):
#     model = Student
#     email = serializers.EmailField()
#     password = serializers.CharField(
#         style={'input_type': 'password'}, write_only=True
#     )

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
                    raise serializers.ValidationError({'email': 'User with provided email does not exist'})

            user = authenticate(email=email, password=password)

            # if not user:
            #     raise serializers.ValidationError({'credentials': 'Invalid credentials'})

            # if not user.is_active:
            #     raise serializers.ValidationError({'status': 'Account is not active'})

            data['user'] = user
            data['user_type'] = user_type
            return data
        else:
            raise serializers.ValidationError({'credentials': 'Must include "email" and "password".'})

        


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model=Teacher
        fields=['full_name','email','phone_number','image',
                'address','gender']
        
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Student
        fields=['full_name','email','phone_number','image',
                'address','subjects']


# class SubjectSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Subject
#         fields = '__all__'

# class ClassSerializer(serializers.ModelSerializer):
#     subjects = SubjectSerializer(many=True, read_only=True)

#     class Meta:
#         model = Class
#         fields = ['id', 'class_number', 'subjects']