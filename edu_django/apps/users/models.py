# users 应用的数据模型
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    """自定义用户模型 - 继承Django的AbstractUser"""
    # 基础字段 (username, password, email 继承自 AbstractUser)
    real_name = models.CharField(max_length=50, verbose_name='真实姓名')
    nickname = models.CharField(max_length=50, null=True, blank=True, verbose_name='昵称', help_text='显示用昵称')
    avatar = models.ImageField(upload_to='avatars/%Y/%m/', null=True, blank=True, verbose_name='头像')
    bio = models.TextField(null=True, blank=True, verbose_name='个人简介')
    phone = models.CharField(max_length=11, unique=True, null=True, blank=True,verbose_name='手机号')
    email = models.EmailField(
        unique=True, 
        verbose_name='邮箱地址',
        help_text='用于登录和找回密码',
        error_messages={
            'unique': "该邮箱已被注册。",
        },
    )
    gender = models.CharField(
        max_length=10, 
        choices=[('male', '男'), ('female', '女'), ('secret', '保密')], 
        default='secret',
        verbose_name='性别'
    )
    school = models.CharField(max_length=100, null=True, blank=True, verbose_name='学校')
    major = models.CharField(max_length=100, null=True, blank=True, verbose_name='专业')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='注册时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS=[]
    class Meta:
        db_table = 'users'
        verbose_name = '用户'
        verbose_name_plural = verbose_name
        indexes = [
            models.Index(fields=['created_at'], name='idx_user_created'),
        ]

    def save(self, *args, **kwargs):
        # 核心技巧：既然系统要求 username 唯一，我们自动把 email 填进去
        # 这样你就不用管 username 字段了，它只是一个后台运行的“唯一 ID”
        if not self.username:
            self.username = self.email
        
        # 处理手机号 NULL 逻辑
        if not self.phone:
            self.phone = None
            
        super().save(*args, **kwargs)
    
    def __str__(self):
        # 优先显示真实姓名（班级用），如果没有真实姓名就显示网名，再没有就显示系统 ID
        return self.real_name or self.nickname 


class StudentProfile(models.Model):
    """学生档案 - 与User一对一关联"""
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='student_profile',
        verbose_name='关联用户'
    )
    student_id = models.CharField(max_length=20, unique=True, verbose_name='学号')
    
    class Meta:
        db_table = 'student_profiles'
        verbose_name = '学生档案'
        verbose_name_plural = verbose_name
    
    def __str__(self):
        return f"{self.user.nickname or self.user.username} - {self.student_id}"


class TeacherProfile(models.Model):
    """教师档案 - 与User一对一关联"""
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='teacher_profile',
        verbose_name='关联用户'
    )
    teacher_id = models.CharField(max_length=20, unique=True, verbose_name='工号')
    # is_verified = models.BooleanField(default=False, verbose_name='认证状态', help_text='是否通过平台认证')
    # verified_at = models.DateTimeField(null=True, blank=True, verbose_name='认证时间')
    
    class Meta:
        db_table = 'teacher_profiles'
        verbose_name = '教师档案'
        verbose_name_plural = verbose_name
    
    def __str__(self):
        return f"{self.user.nickname or self.user.username} - {self.teacher_id}"
