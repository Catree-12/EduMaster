# homework 应用的路由配置
from django.urls import path
from . import views

urlpatterns = [
    # ===== 学生作业 =====
    # GET    /api/student/homework/ - 获取作业列表
    path('student/homework/', views.StudentHomeworkListView.as_view(), name='student-homework-list'),
    
    # GET    /api/student/courses/{courseId}/homework/{homeworkId}/ - 获取作业详情
    path('student/courses/<int:course_id>/homework/<int:homework_id>/', views.StudentHomeworkDetailView.as_view(), name='student-homework-detail'),
    
    # POST   /api/student/courses/{courseId}/homework/{homeworkId}/submit/ - 提交作业
    path('student/courses/<int:course_id>/homework/<int:homework_id>/submit/', views.StudentHomeworkSubmitView.as_view(), name='student-homework-submit'),
    
    # GET    /api/student/courses/{courseId}/homework/{homeworkId}/submission/ - 获取作业提交详情
    path('student/courses/<int:course_id>/homework/<int:homework_id>/submission/', views.StudentHomeworkSubmissionView.as_view(), name='student-homework-submission'),
    
    # ===== 教师作业管理 =====
    # GET    /api/teacher/homework/ - 获取作业库
    path('teacher/homework/', views.TeacherHomeworkListView.as_view(), name='teacher-homework-list'),
    
    # GET    /api/teacher/homework/{id}/ - 获取作业详情
    path('teacher/homework/<int:pk>/', views.TeacherHomeworkDetailView.as_view(), name='teacher-homework-detail'),
    
    # POST   /api/teacher/homework/ - 创建作业
    path('teacher/homework/', views.TeacherHomeworkCreateView.as_view(), name='teacher-homework-create'),
    
    # PUT    /api/teacher/homework/{id}/ - 更新作业
    path('teacher/homework/<int:pk>/', views.TeacherHomeworkUpdateView.as_view(), name='teacher-homework-update'),
    
    # DELETE /api/teacher/homework/{id}/ - 删除作业
    path('teacher/homework/<int:pk>/', views.TeacherHomeworkDeleteView.as_view(), name='teacher-homework-delete'),
    
    # POST   /api/teacher/homework/{id}/publish/ - 发布作业
    path('teacher/homework/<int:pk>/publish/', views.TeacherHomeworkPublishView.as_view(), name='teacher-homework-publish'),
    
    # GET    /api/teacher/homework/{id}/submissions/ - 获取作业提交列表
    path('teacher/homework/<int:pk>/submissions/', views.TeacherHomeworkSubmissionsView.as_view(), name='teacher-homework-submissions'),
    
    # POST   /api/teacher/homework/{id}/submissions/{submissionId}/grade/ - 批改作业
    path('teacher/homework/<int:homework_id>/submissions/<int:submission_id>/grade/', views.TeacherHomeworkGradeView.as_view(), name='teacher-homework-grade'),
]
