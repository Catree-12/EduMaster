# courses 应用的数据模型
from django.db import models
from django.conf import settings

# Create your models here.

class CourseCategory(models.Model):
    """课程分类 - 支持树状结构"""
    name = models.CharField(max_length=50, verbose_name='分类名称', help_text='如 后端开发, Python')
    parent = models.ForeignKey(
        'self', 
        null=True, 
        blank=True, 
        on_delete=models.PROTECT,
        related_name='children',
        verbose_name='父分类'
    )
    order = models.IntegerField(default=0, verbose_name='排序权重', help_text='数字越小越靠前')
    # is_visible = models.BooleanField(default=True, verbose_name='是否显示')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    class Meta:
        db_table = 'course_categories'
        verbose_name = '课程分类'
        verbose_name_plural = verbose_name
        ordering = ['order', 'id']
    
    def __str__(self):
        return self.name


class Course(models.Model):
    """课程"""
    STATUS_CHOICES = [
        ('draft', '草稿'),
        ('pending_review', '待审核'),
        ('published', '已发布'),
        ('rejected', '已拒绝'),
    ]
    
    DIFFICULTY_CHOICES = [
        ('beginner', '初级'),
        ('intermediate', '中级'),
        ('advanced', '高级'),
    ]
    
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='teaching_courses',
        verbose_name='授课教师',
        help_text='防止误删教师导致课程孤立'
    )
    category = models.ForeignKey(
        CourseCategory,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name='courses',
        verbose_name='课程分类'
    )
    title = models.CharField(max_length=200, verbose_name='课程标题')
    description = models.TextField(verbose_name='课程描述')
    cover = models.ImageField(upload_to='courses/covers/%Y/%m/', null=True, blank=True, verbose_name='课程封面')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name='价格', help_text='0.00代表免费')
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='beginner', verbose_name='难度')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft', verbose_name='课程状态')
    audit_remark = models.TextField(null=True, blank=True, verbose_name='审核意见')
    
    # 统计字段
    view_count = models.IntegerField(default=0, verbose_name='浏览量')
    enrollment_count = models.IntegerField(default=0, verbose_name='报名人数')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    published_at = models.DateTimeField(null=True, blank=True, verbose_name='发布时间')
    
    class Meta:
        db_table = 'courses'
        verbose_name = '课程'
        verbose_name_plural = verbose_name
        indexes = [
            models.Index(fields=['teacher'], name='idx_course_teacher'),
            models.Index(fields=['category'], name='idx_course_category'),
            models.Index(fields=['status'], name='idx_course_status'),
            models.Index(fields=['-created_at'], name='idx_course_created'),
        ]
    
    def __str__(self):
        return self.title


class Chapter(models.Model):
    """章节 - 支持多级树状结构"""
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='chapters',
        verbose_name='所属课程'
    )
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='children',
        verbose_name='父章节',
        help_text='支持多级子章节'
    )
    title = models.CharField(max_length=200, verbose_name='章节标题')
    order = models.IntegerField(default=0, verbose_name='排序号')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        db_table = 'chapters'
        verbose_name = '章节'
        verbose_name_plural = verbose_name
        ordering = ['course', 'order', 'id']
        indexes = [
            models.Index(fields=['course', 'order'], name='idx_chapter_order'),
        ]
    
    def __str__(self):
        return f"{self.course.title} - {self.title}"


class Lesson(models.Model):
    """课时/小节"""
    chapter = models.ForeignKey(
        Chapter,
        on_delete=models.CASCADE,
        related_name='lessons',
        verbose_name='所属章节'
    )
    title = models.CharField(max_length=200, verbose_name='课时标题')
    order = models.IntegerField(default=0, verbose_name='排序号')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        db_table = 'lessons'
        verbose_name = '课时'
        verbose_name_plural = verbose_name
        ordering = ['chapter', 'order', 'id']
        indexes = [
            models.Index(fields=['chapter', 'order'], name='idx_lesson_order'),
        ]
    
    def __str__(self):
        return f"{self.chapter.title} - {self.title}"


class LessonContentBlock(models.Model):
    """课时内容块 - 多态内容组件"""
    TYPE_CHOICES = [
        ('video', '视频'),
        ('rich_text', '富文本'),
        ('file', '文件附件'),
        ('image', '图片'),
        ('code', '代码片段'),
    ]
    
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name='content_blocks',
        verbose_name='所属课时'
    )
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, verbose_name='内容类型')
    title = models.CharField(max_length=200, null=True, blank=True, verbose_name='块标题')
    content = models.JSONField(
        null=True, 
        blank=True, 
        verbose_name='内容数据',
        help_text='JSON存储配置/文本/代码片段'
    )
    file = models.FileField(
        upload_to='lessons/files/%Y/%m/',
        null=True,
        blank=True,
        verbose_name='文件资源',
        help_text='视频/图片/附件'
    )
    order = models.IntegerField(default=0, verbose_name='块内排序')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    class Meta:
        db_table = 'lesson_content_blocks'
        verbose_name = '课时内容块'
        verbose_name_plural = verbose_name
        ordering = ['lesson', 'order', 'id']
    
    def __str__(self):
        return f"{self.lesson.title} - {self.get_type_display()} {self.order}"


class CourseTerm(models.Model):
    """课程班期"""
    STATUS_CHOICES = [
        ('in_progress', '进行中'),
        ('finished', '已结课'),
    ]
    
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='terms',
        verbose_name='关联课程'
    )
    name = models.CharField(max_length=100, verbose_name='班期名称', help_text='如 2023秋季一期')
    start_date = models.DateField(verbose_name='开课日期')
    end_date = models.DateField(verbose_name='结课日期')
    description = models.TextField(null=True, blank=True, verbose_name='班期简介')
    enrollment_limit = models.IntegerField(default=0, verbose_name='招生人数限制', help_text='0表示不限制')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='recruiting', verbose_name='状态')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        db_table = 'course_terms'
        verbose_name = '课程班期'
        verbose_name_plural = verbose_name
        ordering = ['-start_date']
        indexes = [
            models.Index(fields=['course', 'status'], name='idx_term_status'),
        ]
    
    def __str__(self):
        return f"{self.course.title} - {self.name}"


class ClassGroup(models.Model):
    """教学班级"""
    term = models.ForeignKey(
        CourseTerm,
        on_delete=models.CASCADE,
        related_name='class_groups',
        verbose_name='关联班期'
    )
    name = models.CharField(max_length=100, verbose_name='班级名称', help_text='如 计算机1班')
    head_teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='managed_classes',
        verbose_name='班主任/助教'
    )
    students = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='enrolled_classes',
        verbose_name='班级学生',
        blank=True
    )
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    class Meta:
        db_table = 'class_groups'
        verbose_name = '教学班级'
        verbose_name_plural = verbose_name
        unique_together = [['term', 'name']]  # 同一班期下班级名不重复
    
    def __str__(self):
        return f"{self.term.name} - {self.name}"
