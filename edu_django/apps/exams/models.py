# exams 应用的数据模型
from django.db import models
from django.conf import settings
from courses.models import Course, CourseTerm, ClassGroup
from knowledge.models import KnowledgePoint

# Create your models here.

class QuestionBank(models.Model):
    """题库 - 智能组卷数据源"""
    TYPE_CHOICES = [
        ('single', '单选题'),
        ('multiple', '多选题'),
        ('true_false', '判断题'),
        ('fill', '填空题'),
        ('essay', '简答题'),
    ]
    
    title = models.CharField(max_length=200, verbose_name='题目名称', help_text='后台管理检索用')
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, verbose_name='题目类型')
    content = models.JSONField(
        verbose_name='题目完整内容',
        help_text='题干、选项、答案、解析'
    )
    grading_rule = models.JSONField(
        null=True,
        blank=True,
        verbose_name='自动批改规则',
        help_text='{"fuzzy_match": true, "ignore_case": true}'
    )
    difficulty = models.FloatField(
        default=0.5,
        verbose_name='难度系数',
        help_text='0.1-1.0，用于贪心算法适配度参数'
    )
    score = models.IntegerField(default=5, verbose_name='题目分值')
    is_active = models.BooleanField(default=True, verbose_name='是否启用', help_text='软删除')
    
    knowledge_points = models.ManyToManyField(
        KnowledgePoint,
        blank=True,
        related_name='questions',
        verbose_name='关联知识点'
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_questions',
        verbose_name='出题人'
    )
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        db_table = 'question_bank'
        verbose_name = '题库'
        verbose_name_plural = verbose_name
        indexes = [
            models.Index(fields=['type', 'is_active'], name='idx_question_type'),
            models.Index(fields=['difficulty'], name='idx_question_diff'),
        ]
    
    def __str__(self):
        return f"{self.get_type_display()} - {self.title}"


class ExamPaper(models.Model):
    """试卷模板"""
    STATUS_CHOICES = [
        ('draft', '草稿'),
        ('published', '已发布'),
    ]
    
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='exam_papers',
        verbose_name='所属课程'
    )
    title = models.CharField(max_length=200, verbose_name='试卷标题')
    total_score = models.IntegerField(default=100, verbose_name='总分')
    duration = models.IntegerField(default=90, verbose_name='考试时长(分钟)')
    questions = models.ManyToManyField(
        QuestionBank,
        related_name='exam_papers',
        verbose_name='关联题目',
        help_text='用于组卷编辑'
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft', verbose_name='状态')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        db_table = 'exam_papers'
        verbose_name = '试卷模板'
        verbose_name_plural = verbose_name
    
    def __str__(self):
        return self.title


class ExamSession(models.Model):
    """考试场次"""
    paper = models.ForeignKey(
        ExamPaper,
        on_delete=models.CASCADE,
        related_name='sessions',
        verbose_name='关联试卷'
    )
    term = models.ForeignKey(
        CourseTerm,
        on_delete=models.CASCADE,
        related_name='exam_sessions',
        verbose_name='关联班期'
    )
    class_group = models.ForeignKey(
        ClassGroup,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='exam_sessions',
        verbose_name='关联班级'
    )
    start_time = models.DateTimeField(verbose_name='开始时间')
    end_time = models.DateTimeField(verbose_name='结束时间')
    questions_snapshot = models.JSONField(
        null=True,
        blank=True,
        verbose_name='题目快照',
        help_text='考试发布时固化题目内容'
    )
    is_published = models.BooleanField(default=False, verbose_name='是否发布')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    class Meta:
        db_table = 'exam_sessions'
        verbose_name = '考试场次'
        verbose_name_plural = verbose_name
    
    def __str__(self):
        return f"{self.paper.title} - {self.term.name}"


class ExamSubmission(models.Model):
    """考试记录"""
    STATUS_CHOICES = [
        ('ongoing', '考试中'),
        ('submitted', '已提交'),
        ('grading', '阅卷中'),
        ('graded', '已阅卷'),
    ]
    
    session = models.ForeignKey(
        ExamSession,
        on_delete=models.CASCADE,
        related_name='submissions',
        verbose_name='关联场次'
    )
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='exam_submissions',
        verbose_name='学生'
    )
    answers = models.JSONField(
        null=True,
        blank=True,
        verbose_name='考生答卷数据',
        help_text='题目ID: 答案内容'
    )
    total_score = models.IntegerField(null=True, blank=True, verbose_name='总分')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ongoing', verbose_name='状态')
    reviewer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='reviewed_exams',
        verbose_name='阅卷人'
    )
    feedback = models.TextField(null=True, blank=True, verbose_name='评语')
    
    started_at = models.DateTimeField(auto_now_add=True, verbose_name='开始时间')
    submit_time = models.DateTimeField(null=True, blank=True, verbose_name='提交时间')
    reviewed_at = models.DateTimeField(null=True, blank=True, verbose_name='阅卷时间')
    
    class Meta:
        db_table = 'exam_submissions'
        verbose_name = '考试记录'
        verbose_name_plural = verbose_name
        unique_together = [['session', 'student']]
    
    def __str__(self):
        return f"{self.student.nickname or self.student.username} - {self.session.paper.title}"


class ExamAnswer(models.Model):
    """答题详情 - 用于自动阅卷"""
    submission = models.ForeignKey(
        ExamSubmission,
        on_delete=models.CASCADE,
        related_name='answer_details',
        verbose_name='关联考试记录'
    )
    question_snapshot = models.JSONField(
        verbose_name='题目快照',
        help_text='存储答题时的题目内容'
    )
    answer_content = models.TextField(verbose_name='学生答案')
    score = models.IntegerField(null=True, blank=True, verbose_name='得分')
    is_correct = models.BooleanField(null=True, blank=True, verbose_name='是否正确')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='答题时间')
    
    class Meta:
        db_table = 'exam_answers'
        verbose_name = '答题详情'
        verbose_name_plural = verbose_name
    
    def __str__(self):
        return f"{self.submission.student.nickname} - Q{self.id}"
