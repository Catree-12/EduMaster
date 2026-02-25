# homework 应用的数据模型
from django.db import models
from django.conf import settings
from courses.models import Course, CourseTerm, ClassGroup

# Create your models here.

class HomeworkTemplate(models.Model):
    """作业模板/题库"""
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='homework_templates',
        verbose_name='所属课程'
    )
    title = models.CharField(max_length=200, verbose_name='作业标题')
    content = models.TextField(blank=True, verbose_name='作业内容/要求')
    # 使用字符串引用避免循环导入
    questions = models.ManyToManyField(
        'exams.QuestionBank',
        blank=True,
        related_name='homework_templates',
        verbose_name='关联题目',
        help_text='用于客观题自动批改'
    )
    total_score = models.IntegerField(default=100, verbose_name='总分')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        db_table = 'homework_templates'
        verbose_name = '作业模板'
        verbose_name_plural = verbose_name
    

    def __str__(self):
        return self.title


class HomeworkAssignment(models.Model):
    """作业发布/任务"""
    template = models.ForeignKey(
        HomeworkTemplate,
        on_delete=models.SET_NULL,  # 模板删除时，此字段设为 NULL，不会删除作业实例
        null=True,                  # 数据库层面允许为空
        blank=True,                 # 表单验证层面允许为空
        related_name='assignments',
        verbose_name='关联作业模板'
    )
    title = models.CharField(max_length=200, verbose_name='作业标题', help_text='发布时固化模板标题')
    term = models.ForeignKey(
        CourseTerm,
        on_delete=models.CASCADE,
        related_name='homework_assignments',
        verbose_name='关联班期'
    )
    class_group = models.ForeignKey(
        ClassGroup,
        on_delete=models.CASCADE, 
        related_name='homework_assignments',
        verbose_name='指定班级'
    )
    specific_students = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name='specific_homework_assignments',
        verbose_name='指定学生',
        help_text='例外/补考'
    )
    deadline = models.DateTimeField(verbose_name='截止时间')
    content_snapshot = models.JSONField(
        null=True,
        blank=True,
        verbose_name='作业完整快照',
        help_text='包含题目、分值、标准答案'
    )
    is_published = models.BooleanField(default=False, verbose_name='是否发布')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    published_at = models.DateTimeField(null=True, blank=True, verbose_name='发布时间')
    
    class Meta:
        db_table = 'homework_assignments'
        verbose_name = '作业发布'
        verbose_name_plural = verbose_name
    
    def __str__(self):
        return f"{self.title} - {self.term.name}"


class HomeworkSubmission(models.Model):
    """学生作业提交"""
    STATUS_CHOICES = [
        ('pending', '未提交'),
        ('submitted', '已提交'),
        ('graded', '已批改'),
    ]
    
    assignment = models.ForeignKey(
        HomeworkAssignment,
        on_delete=models.CASCADE,
        related_name='submissions',
        verbose_name='关联发布记录'
    )
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='homework_submissions',
        verbose_name='学生'
    )
    content = models.JSONField(
        null=True,
        blank=True,
        verbose_name='提交内容',
        help_text='仅存答案，不含题目'
    )
    files = models.JSONField(
        default=list,
        null=True,
        blank=True,
        verbose_name='附件',
        help_text='存储文件URL列表'
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='状态')
    score = models.IntegerField(null=True, blank=True, verbose_name='得分')
    feedback = models.TextField(blank=True, verbose_name='评语')
    
    submitted_at = models.DateTimeField(null=True, blank=True, verbose_name='提交时间')
    graded_at = models.DateTimeField(null=True, blank=True, verbose_name='批改时间')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    class Meta:
        db_table = 'homework_submissions'
        verbose_name = '作业提交'
        verbose_name_plural = verbose_name
        unique_together = [['assignment', 'student']]
    
    def __str__(self):
        return f"{self.student.nickname or self.student.username} - {self.assignment.title}"
