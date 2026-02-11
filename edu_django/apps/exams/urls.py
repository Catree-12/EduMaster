# exams 应用的路由配置
from django.urls import path
from . import views

urlpatterns = [
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
    
    # ===== 教师考试管理 =====
    # GET    /api/teacher/exams/ - 获取试卷库
    path('teacher/exams/', views.TeacherExamListView.as_view(), name='teacher-exam-list'),
    
    # GET    /api/teacher/exams/{id}/ - 获取试卷详情
    path('teacher/exams/<int:pk>/', views.TeacherExamDetailView.as_view(), name='teacher-exam-detail'),
    
    # POST   /api/teacher/exams/ - 创建试卷
    path('teacher/exams/', views.TeacherExamCreateView.as_view(), name='teacher-exam-create'),
    
    # PUT    /api/teacher/exams/{id}/ - 更新试卷
    path('teacher/exams/<int:pk>/', views.TeacherExamUpdateView.as_view(), name='teacher-exam-update'),
    
    # DELETE /api/teacher/exams/{id}/ - 删除试卷
    path('teacher/exams/<int:pk>/', views.TeacherExamDeleteView.as_view(), name='teacher-exam-delete'),
    
    # POST   /api/teacher/exams/{id}/publish/ - 发布试卷
    path('teacher/exams/<int:pk>/publish/', views.TeacherExamPublishView.as_view(), name='teacher-exam-publish'),
    
    # GET    /api/teacher/exams/{id}/submissions/ - 获取考试提交列表
    path('teacher/exams/<int:pk>/submissions/', views.TeacherExamSubmissionsView.as_view(), name='teacher-exam-submissions'),
    
    # POST   /api/teacher/exams/{id}/submissions/{submissionId}/grade/ - 批改试卷
    path('teacher/exams/<int:exam_id>/submissions/<int:submission_id>/grade/', views.TeacherExamGradeView.as_view(), name='teacher-exam-grade'),
]
