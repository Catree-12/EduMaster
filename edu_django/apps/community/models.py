# community 应用的数据模型
from django.db import models
from django.conf import settings
from courses.models import Course

# Create your models here.

class Thread(models.Model):
    """帖子/问题"""
    TYPE_CHOICES = [
        ('question', '问答'),
        ('discussion', '讨论'),
    ]
    
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='threads',
        verbose_name='作者'
    )
    course = models.ForeignKey(
        Course,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='threads',
        verbose_name='关联课程',
        help_text='为空则是公共广场帖子'
    )
    category = models.CharField(max_length=50, null=True, blank=True, verbose_name='分类', help_text='如 技术分享, 公共问答')
    title = models.CharField(max_length=200, verbose_name='帖子标题')
    excerpt = models.CharField(max_length=500, null=True, blank=True, verbose_name='摘要', help_text='列表页显示')
    content = models.TextField(verbose_name='帖子内容')
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='discussion', verbose_name='类型')
    is_pinned = models.BooleanField(default=False, verbose_name='是否置顶')
    is_essence = models.BooleanField(default=False, verbose_name='是否加精')
    
    view_count = models.IntegerField(default=0, verbose_name='浏览量')
    reply_count = models.IntegerField(default=0, verbose_name='回复数', help_text='冗余字段，优化查询')
    like_count = models.IntegerField(default=0, verbose_name='点赞数', help_text='冗余字段')
    
    last_reply_at = models.DateTimeField(null=True, blank=True, verbose_name='最后回复时间')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        db_table = 'community_threads'
        verbose_name = '帖子'
        verbose_name_plural = verbose_name
        ordering = ['-is_pinned', '-last_reply_at', '-created_at']
        indexes = [
            models.Index(fields=['course', '-created_at'], name='idx_thread_course'),
            models.Index(fields=['-is_pinned', '-last_reply_at'], name='idx_thread_hot'),
        ]
    
    def __str__(self):
        return self.title


class Comment(models.Model):
    """回答/评论"""
    thread = models.ForeignKey(
        Thread,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='关联帖子'
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='作者'
    )
    content = models.TextField(verbose_name='评论内容')
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='replies',
        verbose_name='父评论',
        help_text='用于楼中楼'
    )
    like_count = models.IntegerField(default=0, verbose_name='点赞数')
    is_accepted = models.BooleanField(default=False, verbose_name='是否采纳', help_text='作为最佳答案')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='评论时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        db_table = 'community_comments'
        verbose_name = '评论'
        verbose_name_plural = verbose_name
        ordering = ['-is_accepted', 'created_at']
    
    def __str__(self):
        return f"{self.author.nickname} @ {self.thread.title}"


class PostLike(models.Model):
    """帖子点赞"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='post_likes',
        verbose_name='点赞用户'
    )
    thread = models.ForeignKey(
        Thread,
        on_delete=models.CASCADE,
        related_name='likes',
        verbose_name='点赞帖子'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='点赞时间')
    
    class Meta:
        db_table = 'community_post_likes'
        verbose_name = '帖子点赞'
        verbose_name_plural = verbose_name
        unique_together = [['user', 'thread']]
    
    def __str__(self):
        return f"{self.user.nickname} likes {self.thread.title}"


class CommentLike(models.Model):
    """评论点赞"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comment_likes',
        verbose_name='点赞用户'
    )
    comment = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
        related_name='likes',
        verbose_name='点赞评论'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='点赞时间')
    
    class Meta:
        db_table = 'community_comment_likes'
        verbose_name = '评论点赞'
        verbose_name_plural = verbose_name
        unique_together = [['user', 'comment']]
    
    def __str__(self):
        return f"{self.user.nickname} likes comment {self.comment.id}"
