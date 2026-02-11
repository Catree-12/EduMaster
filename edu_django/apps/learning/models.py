# learning 应用的数据模型
from django.db import models
from django.conf import settings
from courses.models import CourseTerm, ClassGroup, Course
from knowledge.models import KnowledgePoint

# Create your models here.

class Enrollment(models.Model):
    """选课记录"""
    STATUS_CHOICES = [
        ('active', '学习中'),
        ('completed', '已完成'),
        ('dropped', '已退课'),
    ]
    
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='enrollments',
        verbose_name='学生'
    )
    term = models.ForeignKey(
        CourseTerm,
        on_delete=models.CASCADE,
        related_name='enrollments',
        verbose_name='关联班期'
    )
    class_group = models.ForeignKey(
        ClassGroup,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='enrollments',
        verbose_name='所属班级'
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active', verbose_name='状态')
    progress = models.FloatField(default=0.0, verbose_name='学习进度', help_text='0-100的百分比')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='选课时间')
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name='完成时间')
    
    class Meta:
        db_table = 'enrollments'
        verbose_name = '选课记录'
        verbose_name_plural = verbose_name
        unique_together = [['student', 'term']]  # 同一学生同一班期只能选一次
        indexes = [
            models.Index(fields=['student', 'status'], name='idx_enroll_status'),
        ]
    
    def __str__(self):
        return f"{self.student.nickname or self.student.username} - {self.term.course.title}"


class StudentKnowledgeMastery(models.Model):
    """学生知识掌握度 - 用于学情分析和BKT/IRT算法"""
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='knowledge_masteries',
        verbose_name='学生'
    )
    knowledge_point = models.ForeignKey(
        KnowledgePoint,
        on_delete=models.CASCADE,
        related_name='student_masteries',
        verbose_name='知识点'
    )
    mastery_level = models.FloatField(
        default=0.0,
        verbose_name='掌握度',
        help_text='0.0-1.0之间，算法：得分/总分'
    )
    total_attempts = models.IntegerField(default=0, verbose_name='练习总次数', help_text='作业/考试/测验总次数')
    total_score_earned = models.FloatField(default=0.0, verbose_name='实际得分总和')
    total_score_possible = models.FloatField(default=0.0, verbose_name='总分值')
    
    last_updated = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        db_table = 'student_knowledge_masteries'
        verbose_name = '学生知识掌握度'
        verbose_name_plural = verbose_name
        unique_together = [['student', 'knowledge_point']]
        indexes = [
            models.Index(fields=['student', 'mastery_level'], name='idx_mastery_level'),
        ]
    
    def __str__(self):
        return f"{self.student.nickname or self.student.username} - {self.knowledge_point.name}: {self.mastery_level:.2f}"
    
    def update_mastery(self):
        """更新掌握度"""
        if self.total_score_possible > 0:
            self.mastery_level = self.total_score_earned / self.total_score_possible
        else:
            self.mastery_level = 0.0
        self.save()


class Certificate(models.Model):
    """证书"""
    STATUS_CHOICES = [
        ('active', '有效'),
        ('revoked', '已撤销'),
        ('expired', '已过期'),
    ]
    
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='certificates',
        verbose_name='学生'
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.PROTECT,
        related_name='certificates',
        verbose_name='课程'
    )
    term = models.ForeignKey(
        CourseTerm,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='certificates',
        verbose_name='关联班期'
    )
    certificate_no = models.CharField(max_length=50, unique=True, verbose_name='证书编号')
    file = models.FileField(
        upload_to='certificates/%Y/%m/',
        null=True,
        blank=True,
        verbose_name='证书文件',
        help_text='生成的PDF/Image'
    )
    template_url = models.URLField(null=True, blank=True, verbose_name='证书模板快照')
    meta_snapshot = models.JSONField(
        null=True,
        blank=True,
        verbose_name='元数据快照',
        help_text='课程名、讲师、学期名等，防止源数据变更'
    )
    score = models.IntegerField(null=True, blank=True, verbose_name='最终成绩')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active', verbose_name='状态')
    
    issued_at = models.DateTimeField(auto_now_add=True, verbose_name='颁发时间')
    
    class Meta:
        db_table = 'certificates'
        verbose_name = '证书'
        verbose_name_plural = verbose_name
        indexes = [
            models.Index(fields=['certificate_no'], name='idx_cert_no'),
            models.Index(fields=['student', 'status'], name='idx_cert_student'),
        ]
    
    def __str__(self):
        return f"{self.certificate_no} - {self.student.nickname or self.student.username}"
