from rest_framework import serializers
from .models import User, Studentuser, Teacheruser, Adminuser
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.utils import timezone
from rest_framework_simplejwt.authentication import JWTAuthentication

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Studentuser
        fields = ['user','student_id']
    
class TeacherSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Teacheruser
        fields = "__all__"

class AdminSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Adminuser
        fields = "__all__"

class UserSerializer(serializers.ModelSerializer):
    student=StudentSerializer(required=False)
    # teacher=TeacherSerializer(required=False)
    # admin=AdminSerializer(required=False)

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    class Meta:
        model = User
        # ,'student','teacher','admin'
        fields = ['username', 'email', 'password', 'role','student']

    def create(self, validated_data):

        stu_data=validated_data.pop('student',None)
        tea_data=validated_data.pop('teacher',None)
        admin_data=validated_data.pop('admin',None)
        user=User.objects.create_user(validated_data,stu_data,tea_data,admin_data)
        return user
    
        
    # def validate_email(self, value):
    #     if value is None:
    #         raise serializers.ValidationError("邮箱不能为空")
    #     if User.objects.filter(email=value).exists():
    #         raise serializers.ValidationError("邮箱已存在")
    #     return value




class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
       data=super().validate(attrs)
       user=self.user
       user.last_login = timezone.now()
       user.save()
       data['username']=user.username
       return data