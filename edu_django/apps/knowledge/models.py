# knowledge 应用的数据模型
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from courses.models import Course

class Tag(models.Model):     
    """标签库 """
    name = models.CharField(max_length=50, unique=True, verbose_name='标签名称')
    course = models.ForeignKey(
        Course, 
        on_delete=models.CASCADE, 
        related_name='tags',
        verbose_name='所属课程',
    )
    class Meta:
        db_table = 'tags'
        verbose_name = '标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
    
class TagRelation(models.Model):
    """标签关联表 - 将标签贴到各种对象上"""
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='tag_rels')
    # 多态关联
    content_type = models.ForeignKey(
        ContentType, 
        on_delete=models.CASCADE,
    )
    object_id = models.PositiveIntegerField(verbose_name='标签关联对象ID')
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        db_table = 'tag_relations'
        unique_together = ('tag', 'content_type', 'object_id')
        verbose_name = '标签关联'



class KnowledgePoint(models.Model):
    """知识点 - 核心资产库，不直接绑定业务对象"""
    name = models.CharField(max_length=100, verbose_name='知识点名称', help_text='如: 循环结构')
    course = models.ForeignKey(
        Course, 
        on_delete=models.CASCADE, 
        related_name='knowledge_points',
        verbose_name='所属课程',
    )
    parent = models.ForeignKey(
        'self', 
        null=True, 
        blank=True, 
        on_delete=models.SET_NULL,  # 父节点删了，子节点变孤儿但不消失
        related_name='children',
        verbose_name='父知识点'
    )
    # 可以在这里增加排序字段，保证树状显示的顺序
    order = models.PositiveIntegerField(default=0, verbose_name='排序')
    
    class Meta:
        db_table = 'knowledge_points'
        verbose_name = '知识点'
        verbose_name_plural = verbose_name
        ordering = ['order', 'id']

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


class KnowledgePointRelation(models.Model):
    """
    知识点关联表 - 实现“一个知识点挂在多个地方”的核心
    """
    knowledge_point = models.ForeignKey(
        KnowledgePoint, 
        on_delete=models.CASCADE, # 如果知识点本体删了，这个关联才消失
        related_name='rel_objects',
        verbose_name='知识点'
    )

    # 多态关联：指向 Course, Lesson, QuestionBank 等
    content_type = models.ForeignKey(
        ContentType, 
        on_delete=models.CASCADE, # 如果关联的课程/题目删了，这条关联记录随之消失
    )
    object_id = models.PositiveIntegerField(verbose_name='知识点关联对象ID')
    content_object = GenericForeignKey('content_type', 'object_id')


    class Meta:
        db_table = 'knowledge_point_rels'
        verbose_name = '知识点挂载'
        unique_together = ('knowledge_point', 'content_type', 'object_id')


class QuestionCategory(models.Model):
    """题目分类/文件夹 - 用于后台管理的目录树"""
    name = models.CharField(max_length=100, verbose_name='文件夹名称')
    
    # 无限层级：实现文件夹套文件夹
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE, # 如果父文件夹删了，子文件夹也没了
        related_name='children',
        verbose_name='父文件夹'
    )
    
    # 归属课程：必须隔离，防止不同课程的文件夹混在一起
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='question_categories',
        verbose_name='所属课程'
    )
    
    # 伪删除字段
    is_deleted = models.BooleanField(default=False, verbose_name='是否已删除')
    
    # 排序字段：允许用户拖拽排序
    order = models.PositiveIntegerField(default=0, verbose_name='排序')
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'question_categories'
        verbose_name = '题目分类'
        verbose_name_plural = verbose_name
        ordering = ['order', 'id'] # 默认按排序字段查

    def __str__(self):
        return self.name