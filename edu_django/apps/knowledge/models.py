# knowledge 应用的数据模型
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.conf import settings

# Create your models here.

class Tag(models.Model):
    """标签 - 通用多态关联，可关联课程、课时、题目等"""
    name = models.CharField(max_length=50, unique=True, verbose_name='标签名称', help_text='如 Python, 难度:高')
    # 多态关联字段
    content_type = models.ForeignKey(
        ContentType, 
        on_delete=models.CASCADE,
        verbose_name='内容类型'
    )
    object_id = models.PositiveIntegerField(verbose_name='对象ID')
    content_object = GenericForeignKey('content_type', 'object_id')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    class Meta:
        db_table = 'tags'
        verbose_name = '标签'
        verbose_name_plural = verbose_name
        indexes = [
            models.Index(fields=['content_type', 'object_id'], name='idx_tag_content'),
            models.Index(fields=['name'], name='idx_tag_name'),
        ]
    
    def __str__(self):
        return self.name


class KnowledgePoint(models.Model):
    """知识点 - 支持树状结构，为推荐算法和学情分析提供基础"""
    parent = models.ForeignKey(
        'self', 
        null=True, 
        blank=True, 
        on_delete=models.CASCADE,
        related_name='children',
        verbose_name='父知识点',
        help_text='支持树状结构'
    )
    name = models.CharField(max_length=100, verbose_name='知识点名称', help_text='如 循环结构')
    # description = models.TextField(null=True, blank=True, verbose_name='知识点描述')
    
    # 多态关联字段 - 仅限关联 Course, Lesson, QuestionBank
    content_type = models.ForeignKey(
        ContentType, 
        on_delete=models.CASCADE,
        verbose_name='关联类型',
        help_text='仅限 Course, Lesson, QuestionBank'
    )
    object_id = models.PositiveIntegerField(verbose_name='关联对象ID')
    content_object = GenericForeignKey('content_type', 'object_id')
    
    # created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    # updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        db_table = 'knowledge_points'
        verbose_name = '知识点'
        verbose_name_plural = verbose_name
        indexes = [
            models.Index(fields=['parent'], name='idx_kp_parent'),
            models.Index(fields=['content_type', 'object_id'], name='idx_kp_content'),
        ]
    
    def __str__(self):
        return self.name
    
    def get_full_path(self):
        """获取知识点的完整路径"""
        path = [self.name]
        parent = self.parent
        while parent:
            path.insert(0, parent.name)
            parent = parent.parent
        return ' > '.join(path)
