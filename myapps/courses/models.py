from django.db import models
from django.conf import settings
from guardian.shortcuts import assign_perm

# Create your models here.
class Node (models.Model):
    TYPE_CHOICES = [
        ('course', '课程'),
        ('chapter', '章'),
        ('section', '节'),
        ('subsection', '小节')
    ]
    node_id=models.AutoField(primary_key=True)
    node_type = models.CharField(max_length=20, choices=TYPE_CHOICES, help_text='节点类型',verbose_name='节点类型')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children',help_text='父节点',verbose_name='父节点')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,help_text='作者',verbose_name='作者')
    title = models.CharField(max_length=200, help_text='标题',verbose_name='标题')
    order = models.PositiveIntegerField()  # 节点顺序控制
    description = models.TextField(blank=True, null=True, help_text='描述',verbose_name='描述')
    tags = models.TextField(blank=True, null=True, help_text='标签',verbose_name='标签')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Node'
        verbose_name = '节点'
        verbose_name_plural = '节点'
        ordering = ['order']

    def get_ancestors(self, include_self=False, include_depth=False):
        """
        参数：
            include_depth - 是否包含深度信息
        返回：
            当include_depth=True时： [(node, depth), ...]
            当include_depth=False时： [node, ...]
        """
        qs = NodeClosure.objects.filter(descendant=self).select_related('ancestor').order_by('depth')
    
        if not include_self:
            qs = qs.exclude(depth=0)  # 排除自引用
        if include_depth:
            return list( (n.ancestor, n.depth) for n in qs )
        return list( n.ancestor for n in qs )   

    
    def get_descendants(self,include_self=False, include_depth=False):

        """获取所有后代节点"""

        qs = NodeClosure.objects.filter(ancestor=self).select_related('descendant').order_by('depth')
    
        if not include_self:
            qs = qs.exclude(depth=0)  # 排除自引用
        if include_depth:
            return [ (n.descendant, n.depth) for n in qs ]
        return [ n.descendant for n in qs ]

    def get_children(self):
        """获取所有直接子节点"""
        qs = Node.objects.filter(parent=self)
        return list(qs)
        
    
    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    #     # 自动分配对象级权限
    #     assign_perm('_course', self.author, self)
    def __str__(self):
        return self.title
    


class section_content(models.Model):

    content_id=models.AutoField(primary_key=True)
    node = models.ForeignKey(Node, on_delete=models.CASCADE, related_name='contents')
    text_content = models.TextField(null=True, blank=True,help_text='文本内容',verbose_name='文本内容')  # 文本内容
    file_url = models.FileField(upload_to='chapters_file/', null=True, blank=True,verbose_name='文件路径')  # 文件内容
    image_url = models.ImageField(upload_to='chapters_images/', null=True, blank=True,verbose_name='图片路径')  # 图片内容
    order = models.PositiveIntegerField()  # 内容排序
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'section_contents'
        verbose_name = '内容'
        verbose_name_plural = '内容'
        ordering = ['order']
        constraints = [
            models.UniqueConstraint(fields=['node', 'order'], name='unique_order_in_node'),
        ]


from django.core.validators import MinValueValidator

class video_content(models.Model):

    RESOLUTION_CHOICES = [
        ('1080p', '1920x1080'),
        ('720p', '1280x720'),
        ('480p', '854x480'),
    ]
    chapter=models.ForeignKey(Node,on_delete=models.CASCADE,related_name='videos')
    video_url=models.FileField (upload_to='chapters_videos/',null=True,blank=True,verbose_name='视频路径')
    total_duration=models.DurationField(validators=[MinValueValidator(0)],help_text='时长',verbose_name='视频总时长')  
    resolution=models.CharField(max_length=20,choices=RESOLUTION_CHOICES,default='1080p',help_text='分辨率',verbose_name='视频分辨率')
    file_size=models.PositiveIntegerField(default=0,verbose_name='视频大小')  # 字节数
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'video_contents'
        verbose_name = '视频内容'
        indexes = [
            models.Index(fields=['resolution']),
        ]


class Lerning_progress(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='learning_progress')
    node = models.OneToOneField(Node, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False,help_text='是否完成',verbose_name='是否完成')
    last_visited = models.DurationField(validators=[MinValueValidator(0)],default=0,verbose_name='上次观看时长')  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'learning_progress'
        verbose_name = '学习进度'
        verbose_name_plural = '学习进度'
        indexes = [
            models.Index(fields=['last_visited']),
        ]

from django.db import transaction
from collections import deque
class NodeClosure(models.Model):
    ancestor = models.ForeignKey(Node, on_delete=models.CASCADE, related_name='descendant_relations')
    descendant = models.ForeignKey(Node, on_delete=models.CASCADE, related_name='ancestor_relations')
    depth = models.IntegerField(default=0)

    class Meta:
        unique_together = [('ancestor', 'descendant')]

    @classmethod
    def _delete_relations(cls,node):
        """删除节点的所有descendant关系"""
        cls.objects.filter(descendant=node).delete()
        
    @classmethod
    def _create_relations(cls,node):
        """创建节点的完整祖先关系"""
        relations = []
        node_ancestors = node.parent.get_ancestors(include_self=True, include_depth=True)
        for ancestor, depth in node_ancestors:
            relations.append(cls(
                ancestor=ancestor,
                descendant=node,
                depth=depth + 1
            ))
        relations.append(cls(
            ancestor=node,
            descendant=node,
            depth=0
        ))        
        cls.objects.bulk_create(relations)

    @classmethod
    def rebuild_for_node(cls, node, parent_changed=False):
        """重构单个节点的闭包关系"""
        with transaction.atomic():
            cls._delete_relations(node)
            cls._create_relations(node)
                
    @classmethod
    def rebuild_branch(cls, node):
        """级联重建所有后代的闭包关系"""

        with transaction.atomic():
            # 获取旧节点
            node_descendants = node.get_descendants(include_self=True)
            old_ancestors = node.get_ancestors()
            # 构建需要删除的对象的查询集
            to_delete = NodeClosure.objects.filter(
                ancestor__in=old_ancestors,
                descendant__in=node_descendants
            )
            # 批量删除
            to_delete.delete()

            relative_depth_map = {}
            queue = deque([(node, 0)])
            while queue:
                current, depth = queue.popleft()

                relative_depth_map[current.pk] = depth
                for child in current.get_children():
                    queue.append((child, depth + 1))

            # 批量创建新关系
            new_relations = []
            # 获取新关系祖先
            new_ancestors = node.parent.get_ancestors(include_self=True, include_depth=True)                    
            if node.parent:
                for descendant in node_descendants:
                    for ancestor, parent_depth in new_ancestors:
                        new_relations.append(cls(
                                    ancestor= ancestor,
                                    descendant= descendant,
                                    depth=parent_depth + 1 + relative_depth_map[descendant.pk]
                                ))             
            cls.objects.bulk_create(new_relations)

            

    