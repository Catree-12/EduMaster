# exams 应用的路由配置
from django.urls import path
from . import views

urlpatterns = [
    # ===== 教师题目文件夹管理 =====
    # GET  /api/teacher/courses/{course_id}/question-categories/ - 获取文件夹树
    # POST /api/teacher/courses/{course_id}/question-categories/ - 创建文件夹
    path('teacher/courses/<int:course_id>/question-categories/', views.TeacherQuestionCategoryManageView.as_view(), name='teacher-question-categories'),
    
    # GET    /api/teacher/courses/{course_id}/question-categories/{category_id}/ - 获取文件夹详情
    # PUT    /api/teacher/courses/{course_id}/question-categories/{category_id}/ - 更新文件夹
    # DELETE /api/teacher/courses/{course_id}/question-categories/{category_id}/ - 删除文件夹（软删除）
    path('teacher/courses/<int:course_id>/question-categories/<int:category_id>/', views.TeacherQuestionCategoryDetailView.as_view(), name='teacher-question-category-detail'),
    
    # ===== 教师题库管理 =====
    # GET  /api/teacher/courses/{course_id}/questions/ - 获取题库列表
    # POST /api/teacher/courses/{course_id}/questions/ - 创建题目
    path('teacher/courses/<int:course_id>/questions/', views.TeacherQuestionBankManageView.as_view(), name='teacher-questions'),
    
    # GET    /api/teacher/courses/{course_id}/questions/{question_id}/ - 获取题目详情
    # PUT    /api/teacher/courses/{course_id}/questions/{question_id}/ - 更新题目
    # DELETE /api/teacher/courses/{course_id}/questions/{question_id}/ - 删除题目
    path('teacher/courses/<int:course_id>/questions/<int:question_id>/', views.TeacherQuestionBankDetailView.as_view(), name='teacher-question-detail'),
    
    # ===== 教师试卷管理 =====
    # GET  /api/teacher/courses/{course_id}/exams/ - 获取试卷列表
    # POST /api/teacher/courses/{course_id}/exams/ - 创建试卷
    path('teacher/courses/<int:course_id>/exams/', views.TeacherExamManageView.as_view(), name='teacher-exams'),
    
    # GET    /api/teacher/courses/{course_id}/exams/{exam_id}/ - 获取试卷详情
    # PUT    /api/teacher/courses/{course_id}/exams/{exam_id}/ - 更新试卷
    # DELETE /api/teacher/courses/{course_id}/exams/{exam_id}/ - 删除试卷
    path('teacher/courses/<int:course_id>/exams/<int:exam_id>/', views.TeacherExamPaperDetailView.as_view(), name='teacher-exam-detail'),
    
    # POST   /api/teacher/courses/{course_id}/exams/{exam_id}/publish/ - 发布试卷
    path('teacher/courses/<int:course_id>/exams/<int:exam_id>/publish/', views.TeacherExamPublishView.as_view(), name='teacher-exam-publish'),
    
    # GET    /api/teacher/courses/{course_id}/exams/{exam_id}/submissions/ - 获取考试提交列表
    path('teacher/courses/<int:course_id>/exams/<int:exam_id>/submissions/', views.TeacherExamSubmissionsView.as_view(), name='teacher-exam-submissions'),
    
    # POST   /api/teacher/courses/{course_id}/exams/{exam_id}/submissions/{submission_id}/grade/ - 批改试卷
    path('teacher/courses/<int:course_id>/exams/<int:exam_id>/submissions/<int:submission_id>/grade/', views.TeacherExamGradeView.as_view(), name='teacher-exam-grade'),
    
    # ===== 学生考试 =====
    # GET    /api/student/exams/ - 获取考试列表
    path('student/exams/', views.StudentExamListView.as_view(), name='student-exam-list'),
    
    # GET    /api/student/courses/{courseId}/exams/{examId}/ - 获取考试详情
    path('student/courses/<int:course_id>/exams/<int:exam_id>/', views.StudentExamDetailView.as_view(), name='student-exam-detail'),
    
    # POST   /api/student/courses/{courseId}/exams/{examId}/start/ - 开始考试
    path('student/courses/<int:course_id>/exams/<int:exam_id>/start/', views.StudentExamStartView.as_view(), name='student-exam-start'),
    
    # POST   /api/student/courses/{courseId}/exams/{examId}/submit/ - 提交答卷
    path('student/courses/<int:course_id>/exams/<int:exam_id>/submit/', views.StudentExamSubmitView.as_view(), name='student-exam-submit'),
    
    # GET    /api/student/courses/{courseId}/exams/{examId}/result/ - 获取考试成绩
    path('student/courses/<int:course_id>/exams/<int:exam_id>/result/', views.StudentExamResultView.as_view(), name='student-exam-result'),
]
