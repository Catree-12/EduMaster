# system 应用的数据模型
from django.db import models
from django.conf import settings
import uuid

# Create your models here.

class Task(models.Model):
    """异步任务"""
    STATUS_CHOICES = [
        ('pending', '待处理'),
        ('processing', '处理中'),
        ('success', '成功'),
        ('failure', '失败'),
    ]
    
    task_id = models.UUIDField(default=uuid.uuid4, unique=True, verbose_name='任务ID', help_text='Celery Task ID')
    name = models.CharField(max_length=100, verbose_name='任务名称', help_text='如 generate_exam, transcode_video')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='tasks',
        verbose_name='触发用户'
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='状态')
    result = models.JSONField(
        null=True,
        blank=True,
        verbose_name='任务结果',
        help_text='如 生成的试卷ID, 错误信息'
    )
    progress = models.IntegerField(default=0, verbose_name='进度', help_text='0-100')
    error_message = models.TextField(null=True, blank=True, verbose_name='错误信息')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    started_at = models.DateTimeField(null=True, blank=True, verbose_name='开始时间')
    finished_at = models.DateTimeField(null=True, blank=True, verbose_name='完成时间')
    
    class Meta:
        db_table = 'system_tasks'
        verbose_name = '异步任务'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['task_id'], name='idx_task_id'),
            models.Index(fields=['user', 'status'], name='idx_task_user'),
        ]
    
    def __str__(self):
        return f"{self.name} - {self.get_status_display()}"


class SystemConfig(models.Model):
    """系统配置"""
    key = models.CharField(max_length=100, unique=True, verbose_name='配置键', help_text='如 site_name, allow_register')
    value = models.JSONField(verbose_name='配置值', help_text='支持各种类型')
    description = models.CharField(max_length=200, null=True, blank=True, verbose_name='描述')
    is_public = models.BooleanField(default=False, verbose_name='是否公开', help_text='前端可见')
    
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    class Meta:
        db_table = 'system_configs'
        verbose_name = '系统配置'
        verbose_name_plural = verbose_name
    
    def __str__(self):
        return f"{self.key}: {self.value}"


class Message(models.Model):
    """消息通知"""
    TYPE_CHOICES = [
        ('system', '系统消息'),
        ('course', '课程消息'),
        ('interaction', '互动消息'),
        ('security', '安全消息'),
    ]
    
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='sent_messages',
        verbose_name='发送者',
        help_text='系统消息为空'
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='received_messages',
        verbose_name='接收者'
    )
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='system', verbose_name='消息类型')
    title = models.CharField(max_length=200, verbose_name='标题')
    content = models.TextField(verbose_name='内容')
    related_link = models.CharField(max_length=500, null=True, blank=True, verbose_name='跳转链接')
    is_read = models.BooleanField(default=False, verbose_name='是否已读')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='发送时间')
    read_at = models.DateTimeField(null=True, blank=True, verbose_name='阅读时间')
    
    class Meta:
        db_table = 'system_messages'
        verbose_name = '消息通知'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['receiver', 'is_read'], name='idx_message_receiver'),
            models.Index(fields=['-created_at'], name='idx_message_created'),
        ]
    
    def __str__(self):
        return f"{self.title} -> {self.receiver.nickname or self.receiver.username}"
