# operations 应用的数据模型
from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

# Create your models here.

class Banner(models.Model):
    """轮播图"""
    POSITION_CHOICES = [
        ('home_top', '首页顶部'),
        ('course_list_top', '课程列表顶部'),
    ]
    
    title = models.CharField(max_length=200, verbose_name='标题')
    image = models.ImageField(upload_to='banners/%Y/%m/', verbose_name='图片地址')
    link_url = models.URLField(null=True, blank=True, verbose_name='跳转链接')
    order = models.IntegerField(default=0, verbose_name='排序', help_text='数字越小越靠前')
    position = models.CharField(max_length=50, choices=POSITION_CHOICES, default='home_top', verbose_name='位置')
    is_active = models.BooleanField(default=True, verbose_name='是否启用')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        db_table = 'operations_banners'
        verbose_name = '轮播图'
        verbose_name_plural = verbose_name
        ordering = ['order', 'id']
    
    def __str__(self):
        return self.title


class Announcement(models.Model):
    """系统公告"""
    title = models.CharField(max_length=200, verbose_name='标题')
    content = models.TextField(verbose_name='内容')
    is_popup = models.BooleanField(default=False, verbose_name='是否弹窗强提醒')
    start_time = models.DateTimeField(verbose_name='展示开始时间')
    end_time = models.DateTimeField(verbose_name='展示结束时间')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    class Meta:
        db_table = 'operations_announcements'
        verbose_name = '系统公告'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title


class DailyStat(models.Model):
    """每日统计"""
    date = models.DateField(unique=True, verbose_name='统计日期')
    new_users = models.IntegerField(default=0, verbose_name='新增用户数')
    active_users = models.IntegerField(default=0, verbose_name='活跃用户数')
    new_courses = models.IntegerField(default=0, verbose_name='新增课程数')
    total_enrollments = models.IntegerField(default=0, verbose_name='累计选课人次')
    new_enrollments = models.IntegerField(default=0, verbose_name='当日选课人次')
    certificates_issued = models.IntegerField(default=0, verbose_name='颁发证书数')
    total_income = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name='当日营收')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    class Meta:
        db_table = 'operations_daily_stats'
        verbose_name = '每日统计'
        verbose_name_plural = verbose_name
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.date} 统计"


class Report(models.Model):
    """举报"""
    STATUS_CHOICES = [
        ('pending', '待处理'),
        ('resolved', '已处理'),
        ('rejected', '已驳回'),
    ]
    
    reporter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reports',
        verbose_name='举报人'
    )
    # 多态关联 - 可举报 Thread, Comment, Course 等
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, verbose_name='举报对象类型')
    object_id = models.PositiveIntegerField(verbose_name='举报对象ID')
    content_object = GenericForeignKey('content_type', 'object_id')
    
    reason = models.CharField(max_length=200, verbose_name='举报原因')
    description = models.TextField(null=True, blank=True, verbose_name='详细描述')
    content_snapshot = models.JSONField(
        null=True,
        blank=True,
        verbose_name='被举报内容快照',
        help_text='防止用户删除/修改证据'
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='处理状态')
    admin_remark = models.TextField(null=True, blank=True, verbose_name='处理备注')
    handler = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='handled_reports',
        verbose_name='处理人'
    )
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='举报时间')
    handled_at = models.DateTimeField(null=True, blank=True, verbose_name='处理时间')
    
    class Meta:
        db_table = 'operations_reports'
        verbose_name = '举报'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', '-created_at'], name='idx_report_status'),
        ]
    
    def __str__(self):
        return f"{self.reporter.nickname} 举报 {self.content_type.model}"
