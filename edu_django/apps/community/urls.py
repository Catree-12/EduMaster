from django.urls import path
from . import views

urlpatterns = [
    # ===== 公共社区 =====
    # GET    /api/community/questions/ - 获取社区问题列表
    path('questions/', views.PublicQuestionListView.as_view(), name='public-question-list'),
    
    # GET    /api/community/questions/{id}/ - 获取问题详情
    path('questions/<int:pk>/', views.PublicQuestionDetailView.as_view(), name='public-question-detail'),
    
    # POST   /api/community/questions/ - 发布问题
    path('questions/', views.PostQuestionView.as_view(), name='post-question'),
    
    # PUT    /api/community/questions/{id}/ - 编辑问题
    path('questions/<int:pk>/', views.UpdateQuestionView.as_view(), name='update-question'),
    
    # DELETE /api/community/questions/{id}/ - 删除问题
    path('questions/<int:pk>/', views.DeleteQuestionView.as_view(), name='delete-question'),
    
    # POST   /api/community/questions/{id}/like/ - 点赞问题
    path('questions/<int:pk>/like/', views.LikeQuestionView.as_view(), name='like-question'),
    
    # ===== 问答 =====
    # POST   /api/community/questions/{id}/answers/ - 回答问题
    path('questions/<int:question_id>/answers/', views.PostAnswerView.as_view(), name='post-answer'),
    
    # PUT    /api/community/answers/{id}/ - 编辑回答
    path('answers/<int:pk>/', views.UpdateAnswerView.as_view(), name='update-answer'),
    
    # DELETE /api/community/answers/{id}/ - 删除回答
    path('answers/<int:pk>/', views.DeleteAnswerView.as_view(), name='delete-answer'),
    
    # POST   /api/community/answers/{id}/like/ - 点赞回答
    path('answers/<int:pk>/like/', views.LikeAnswerView.as_view(), name='like-answer'),
    
    # ===== 课程社区（学生） =====
    # GET    /api/student/courses/{courseId}/threads/ - 获取课程话题列表
    path('student/courses/<int:course_id>/threads/', views.StudentThreadListView.as_view(), name='student-thread-list'),
    
    # GET    /api/student/courses/{courseId}/threads/{threadId}/ - 获取话题详情
    path('student/courses/<int:course_id>/threads/<int:thread_id>/', views.StudentThreadDetailView.as_view(), name='student-thread-detail'),
    
    # POST   /api/student/courses/{courseId}/threads/ - 发布话题
    path('student/courses/<int:course_id>/threads/', views.StudentThreadCreateView.as_view(), name='student-thread-create'),
    
    # PUT    /api/student/courses/{courseId}/threads/{threadId}/ - 编辑话题
    path('student/courses/<int:course_id>/threads/<int:thread_id>/', views.StudentThreadUpdateView.as_view(), name='student-thread-update'),
    
    # DELETE /api/student/courses/{courseId}/threads/{threadId}/ - 删除话题
    path('student/courses/<int:course_id>/threads/<int:thread_id>/', views.StudentThreadDeleteView.as_view(), name='student-thread-delete'),
    
    # POST   /api/student/courses/{courseId}/threads/{threadId}/comments/ - 发布评论
    path('student/courses/<int:course_id>/threads/<int:thread_id>/comments/', views.StudentThreadCommentView.as_view(), name='student-thread-comment'),
    
    # ===== 课程社区（教师） =====
    # GET    /api/teacher/courses/{courseId}/threads/ - 获取课程话题列表
    path('teacher/courses/<int:course_id>/threads/', views.TeacherThreadListView.as_view(), name='teacher-thread-list'),
    
    # GET    /api/teacher/courses/{courseId}/threads/{threadId}/ - 获取话题详情
    path('teacher/courses/<int:course_id>/threads/<int:thread_id>/', views.TeacherThreadDetailView.as_view(), name='teacher-thread-detail'),
    
    # POST   /api/teacher/courses/{courseId}/threads/ - 发布公告/话题
    path('teacher/courses/<int:course_id>/threads/', views.TeacherThreadCreateView.as_view(), name='teacher-thread-create'),
    
    # PUT    /api/teacher/courses/{courseId}/threads/{threadId}/ - 编辑话题
    path('teacher/courses/<int:course_id>/threads/<int:thread_id>/', views.TeacherThreadUpdateView.as_view(), name='teacher-thread-update'),
    
    # DELETE /api/teacher/courses/{courseId}/threads/{threadId}/ - 删除话题
    path('teacher/courses/<int:course_id>/threads/<int:thread_id>/', views.TeacherThreadDeleteView.as_view(), name='teacher-thread-delete'),
    
    # POST   /api/teacher/courses/{courseId}/threads/{threadId}/pin/ - 置顶话题
    path('teacher/courses/<int:course_id>/threads/<int:thread_id>/pin/', views.PinThreadView.as_view(), name='pin-thread'),
    
    # POST   /api/teacher/courses/{courseId}/threads/{threadId}/unpin/ - 取消置顶
    path('teacher/courses/<int:course_id>/threads/<int:thread_id>/unpin/', views.UnpinThreadView.as_view(), name='unpin-thread'),
]
