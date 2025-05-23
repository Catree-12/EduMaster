from django.contrib import admin
from .models import Question, ChoiceAnswer, JudgmentAnswer, Tiankong_Answer, Jianda_Answer, Question_Submission


class ChoiceAnswerInline(admin.StackedInline):
    model = ChoiceAnswer
    extra = 1
    verbose_name = "选择题答案"
    verbose_name_plural = "选择题答案"

class JudgmentAnswerInline(admin.StackedInline):
    model = JudgmentAnswer
    extra = 1
    verbose_name = "判断题答案"
    verbose_name_plural = "判断题答案"

class TiankongAnswerInline(admin.StackedInline):
    model = Tiankong_Answer
    extra = 1
    verbose_name = "填空题答案"
    verbose_name_plural = "填空题答案"

class JiandaAnswerInline(admin.StackedInline):
    model = Jianda_Answer
    extra = 1
    verbose_name = "简答题答案"
    verbose_name_plural = "简答题答案"

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'node', 'content_type', 'content')
    list_filter = ('node', 'content_type')
    search_fields = ('content', 'node__name')
    filter_horizontal = ()  # 如果有需要，可以在这里添加多对多字段
    fieldsets = (
            (None, {
                'fields': ('node', 'content_type', 'content')
            }),
            ('选项', {
                'fields': ('choice_options',),
                'classes': ('collapse',),  # 可折叠
                'description': '选择题的选项'
            }),
            ('说明', {
                'fields': ('explanation',),
                'classes': ('collapse',),  # 可折叠
                'description': '额外说明'
            }),
        )
        
    inlines = []

    def get_inline_instances(self, request, obj=None):
        inlines = super().get_inline_instances(request, obj)
        if obj:
            if obj.content_type == 'single_choice' or obj.content_type == 'multiple_choice':
                inlines.append(ChoiceAnswerInline(self.model, self.admin_site))
            elif obj.content_type == 'judgment':
                inlines.append(JudgmentAnswerInline(self.model, self.admin_site))
            elif obj.content_type == 'fill_in_the_blank':
                inlines.append(TiankongAnswerInline(self.model, self.admin_site))
            elif obj.content_type == 'short_answer':
                inlines.append(JiandaAnswerInline(self.model, self.admin_site))
        return inlines

# 自定义 ChoiceAnswer 的 Admin 显示
@admin.register(ChoiceAnswer)
class ChoiceAnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'question_content', 'correct_answer')
    list_filter = ('question__node',)
    search_fields = ('question__content',)
    def question_content(self, obj):
        return obj.question.content
    question_content.short_description = '题目'

# 自定义 JudgmentAnswer 的 Admin 显示
@admin.register(JudgmentAnswer)
class JudgmentAnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'question_content', 'correct_answer')
    list_filter = ('question__node',)
    search_fields = ('question__content',)
    def question_content(self, obj):
        return obj.question.content
    question_content.short_description = '题目'

# 自定义 Tiankong_Answer 的 Admin 显示
@admin.register(Tiankong_Answer)
class TiankongAnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'question_content', 'correct_answer')
    list_filter = ('question__node',)
    search_fields = ('question__content',)
    def question_content(self, obj):
        return obj.question.content
    question_content.short_description = '题目'    

# 自定义 Jianda_Answer 的 Admin 显示
@admin.register(Jianda_Answer)
class JiandaAnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'question_content', 'correct_answer')
    list_filter = ('question__node',)
    search_fields = ('question__content',)

    def question_content(self, obj):
        return obj.question.content
    question_content.short_description = '题目'    

# 自定义 Question_Submission 的 Admin 显示
@admin.register(Question_Submission)
class QuestionSubmissionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'question_content','answer' ,'is_correct', 'submitted_at')
    list_filter = ('user', 'question__node', 'is_correct')
    search_fields = ('user__username', 'question__content')

    def question_content(self, obj):
        return obj.question.content
    question_content.short_description = '题目'