from django.db import models
from django.contrib.auth.models import AbstractUser
from ..courses.models import Node
from guardian.shortcuts import assign_perm
from django.conf import settings


from django.contrib.auth.models import UserManager

class my_manager(UserManager):
    
    def create_user(self, validated_data,stu_data,tea_data,admin_data):
        role=validated_data['role']
        user=super().create_user(**validated_data)
        user.is_active=True #控制用户是否可以登录和使用系统
        user.set_password(validated_data['password'])
        user.save()
        if role=='student':
            Studentuser.objects.create(**stu_data)
        elif role=='teacher':
            Teacheruser.objects.create(**tea_data)
        elif role=='admin':
            Adminuser.objects.create(**admin_data)
        return user 
    

class User(AbstractUser):

    ROLE_CHOICES = [
        ('student', '学生'),
        ('teacher', '教师'),
        ('admin', '管理员')
    ]
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["username"]
    email = models.EmailField(unique=True, verbose_name='邮箱', blank=False,null=False)
    mobile = models.CharField(max_length=15,unique=True, blank=True, null=True,verbose_name="手机号码")
    avatar = models.ImageField(upload_to='avatars/',blank=True,null=True,verbose_name='用户头像')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student', verbose_name='用户角色')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = my_manager()

    class Meta:
        db_table = "user"
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['role'])
        ]

    def __str__(self):
        return self.email
    

class Studentuser(models.Model):

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='student')
    student_id = models.CharField(max_length=20,verbose_name="学号",primary_key=True)
    enrolled_courses = models.ManyToManyField(Node, related_name='enrolled_students', blank=True,limit_choices_to={'node_type':'course'})
    tags=models.JSONField(default=list,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = "studentuser"
        verbose_name = "学生信息"
        verbose_name_plural = "学生信息"


class Teacheruser(models.Model):

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='teacher')
    teacher_id = models.CharField(max_length=20, primary_key=True, verbose_name="工号",default="000000000000")
    tags=models.JSONField(default=list,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = "teacheruser"
        verbose_name = "教师信息"
        verbose_name_plural = "教师信息"

    
class Adminuser(models.Model):
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='admin')
    admin_id = models.CharField(max_length=20, primary_key=True, verbose_name="工号")
    tags=models.JSONField(default=list,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = "adminuser"
        verbose_name = "管理员信息"
        verbose_name_plural=verbose_name


