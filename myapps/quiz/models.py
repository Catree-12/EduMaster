from django.db import models
# from EduMaster.myapps.quiz.models import Question
from ..courses.models import Node
from django.conf import settings
# Create your models here.
from django.core.exceptions import ValidationError

class Question (models.Model):

    QUESTION_TYPE_CHOICES  = [
        ('single_choice', '单选题'),
        ('multiple_choice', '多选题'),
        ('judgment', '判断题'),
        ('fill_in_the_blank', '填空题'),
        ('short_answer', '简答题'),
    ]
    id=models.AutoField(primary_key=True)
    node=models.ForeignKey(Node,on_delete=models.CASCADE,related_name='questions',verbose_name='所属节点')
    content_type=models.CharField(max_length=20,choices=QUESTION_TYPE_CHOICES,verbose_name='题型')
    content = models.TextField(blank=False,null=False,help_text="支持HTML/Markdown格式",verbose_name='题目内容')
    choice_options=models.JSONField(default=dict,null=True,blank=True,verbose_name='选择题选项')
    explanation = models.TextField(blank=True, null=True, help_text="额外说明")

    def clean(self):
        # 内容类型与字段匹配验证
        if self.content_type == 'single_choice' and not self.choice_options:
            raise ValidationError({
                'choice_options': '单选题必须提供选项'
            })
        elif self.content_type == 'multiple_choice' and not self.choice_options:
            raise ValidationError({
                'choice_options': '多选题必须提供选项'
            })
        elif self.content_type in ['fill_in_the_blank', 'short_answer'] and not self.content:
            raise ValidationError({
                'content': '填空题和简答题必须提供题目内容'
            })
        
    def __str__(self):
        return self.content
    
    class Meta:
        verbose_name='题目'
        verbose_name_plural='题目'

        
class ChoiceAnswer(models.Model):

    id=models.AutoField(primary_key=True)
    question=models.OneToOneField(Question,on_delete=models.CASCADE,related_name='choice_answer')
    correct_answer=models.JSONField(default=dict,null=True,blank=True,verbose_name='正确答案')
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name='选择题答案'
        verbose_name_plural='选择题答案'
    

class JudgmentAnswer(models.Model):

    id=models.AutoField(primary_key=True)
    question=models.OneToOneField(Question,on_delete=models.CASCADE,related_name='judgment_answer')
    correct_answer=models.BooleanField(null=True,blank=True,help_text='正确答案',verbose_name='正确答案')
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name='判断题答案'
        verbose_name_plural='判断题答案'


class Tiankong_Answer(models.Model):

    id=models.AutoField(primary_key=True)
    question=models.OneToOneField(Question,on_delete=models.CASCADE,related_name='tiankong_answer')
    correct_answer=models.TextField(max_length=200,null=True,blank=True,help_text='正确答案',verbose_name='正确答案')
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name='填空题答案'
        verbose_name_plural='填空题答案'


class Jianda_Answer(models.Model):

    id=models.AutoField(primary_key=True)
    question=models.OneToOneField(Question,on_delete=models.CASCADE,related_name='jianda_answer')
    correct_answer=models.TextField(max_length=200,null=True,blank=True,help_text='正确答案',verbose_name='正确答案')
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name='简答题答案'
        verbose_name_plural='简答题答案'


class Question_Submission(models.Model):
    
    id=models.AutoField(primary_key=True)
    user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='user_submissions')
    question=models.ForeignKey(Question,on_delete=models.CASCADE)
    answer=models.TextField(blank=True,null=True,verbose_name='回答内容')
    is_correct=models.BooleanField(null=True,blank=True,help_text='是否正确',verbose_name='是否正确')
    submitted_at = models.DateTimeField(auto_now_add=True,help_text='提交时间',verbose_name='提交时间')
    updated_at=models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name='提交记录'
        verbose_name_plural='提交记录'

  
