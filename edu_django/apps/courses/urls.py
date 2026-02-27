# courses 应用的路由配置
from django.urls import path
from . import views

urlpatterns = [

    # ===== 公共课程接口 =====

    # GET    /api/courses/ - 获取课程列表
    path('courses/', views.PublicCourseListView.as_view(), name='public-course-list'),
    
    # GET    /api/courses/{id}/ - 获取课程详情
    path('courses/<int:pk>/', views.PublicCourseDetailView.as_view(), name='public-course-detail'),
    
    # GET    /api/courses/{id}/resources/ - 获取课程资源
    # path('courses/<int:pk>/resources/', views.CourseResourcesView.as_view(), name='course-resources'),
    
    # GET    /api/courses/my-courses/ - 获取我的课程（已选/已教）
    path('courses/mycourses/', views.MyCoursesView.as_view(), name='my-courses'),
    

    # ===== 学生选课和学习 =====

    # GET    /api/courses/{course_id}/enrollment/ - 获取课程班期班级信息（供选课使用）
    # POST   /api/courses/{course_id}/enrollment/ - 选课（传入班期ID、班级ID）
    # DELETE /api/courses/{course_id}/enrollment/ - 退课
    path('courses/<int:course_id>/enrollment/', views.CourseEnrollmentView.as_view(), name='course-enrollment'),
    
    # GET    /api/student/courses/{courseId}/ - 获取课程学习详情
    path('student/courses/<int:course_id>/', views.StudentCourseDetailView.as_view(), name='student-course-detail'),
    
    # POST   /api/student/courses/{courseId}/progress/ - 更新学习进度
    path('student/courses/<int:course_id>/progress/', views.StudentCourseProgressView.as_view(), name='student-course-progress'),
    
    # GET    /api/student/courses/{courseId}/lessons/{lessonId}/ - 获取课时详情
    path('student/courses/<int:course_id>/lessons/<int:lesson_id>/', views.StudentLessonDetailView.as_view(), name='student-lesson-detail'),
    
    # POST   /api/student/courses/{courseId}/lessons/{lessonId}/complete/ - 完成课时学习
    path('student/courses/<int:course_id>/lessons/<int:lesson_id>/complete/', views.StudentLessonCompleteView.as_view(), name='student-lesson-complete'),
    
    # ===== 教师课程管理 =====
    # GET    /api/teacher/courses/ - 获取我教的课程
    # path('teacher/courses/', views.TeacherCourseListView.as_view(), name='teacher-course-list'),
    
    # POST   /api/teacher/courses/ - 创建课程
    path('teacher/courses/create/', views.TeacherCourseCreateView.as_view(), name='teacher-course-create'),
    
    # GET    /api/teacher/courses/{id}/ - 获取课程管理详情
    # PUT    /api/teacher/courses/{id}/ - 更新课程
    # DELETE /api/teacher/courses/{id}/ - 删除课程
    path('teacher/courses/<int:pk>/', views.TeacherCourseManageView.as_view(), name='teacher-course-manage'),
    
    # POST   /api/teacher/courses/{id}/publish/ - 发布课程
    path('teacher/courses/<int:pk>/publish/', views.TeacherCoursePublishView.as_view(), name='teacher-course-publish'),
    
    # POST   /api/teacher/courses/{id}/cover/ - 上传课程封面
    path('teacher/courses/<int:pk>/cover/', views.TeacherCourseCoverUploadView.as_view(), name='teacher-course-cover-upload'),
    
    # ===== 教师章节管理 (RESTful) =====
    # GET    /api/teacher/courses/{course_id}/chapters/ - 获取章节目录结构（懒加载，不含课时内容）
    # POST   /api/teacher/courses/{course_id}/chapters/ - 创建章节
    path('teacher/courses/<int:course_id>/chapters/', views.TeacherChapterManageView.as_view(), name='teacher-chapters'),
    
    # GET    /api/teacher/courses/{course_id}/chapters/{chapter_id}/ - 获取章节详情
    # PUT    /api/teacher/courses/{course_id}/chapters/{chapter_id}/ - 更新章节
    # DELETE /api/teacher/courses/{course_id}/chapters/{chapter_id}/ - 删除章节
    path('teacher/courses/<int:course_id>/chapters/<int:chapter_id>/', views.TeacherChapterDetailView.as_view(), name='teacher-chapter-detail'),
    
    # POST   /api/teacher/courses/{course_id}/chapters/sort/ - 批量排序章节
    path('teacher/courses/<int:course_id>/chapters/sort/', views.TeacherChapterSortView.as_view(), name='teacher-chapters-sort'),
    
    # ===== 教师课时管理 (RESTful) =====
    # GET    /api/teacher/courses/{course_id}/chapters/{chapter_id}/lessons/ - 获取章节下的课时列表
    # POST   /api/teacher/courses/{course_id}/chapters/{chapter_id}/lessons/ - 创建课时
    path('teacher/courses/<int:course_id>/chapters/<int:chapter_id>/lessons/', views.TeacherChapterLessonManageView.as_view(), name='teacher-chapter-lessons'),
    
    # POST   /api/teacher/courses/{course_id}/chapters/{chapter_id}/lessons/sort/ - 批量排序课时
    path('teacher/courses/<int:course_id>/chapters/<int:chapter_id>/lessons/sort/', views.TeacherLessonSortView.as_view(), name='teacher-lessons-sort'),
    
    # GET    /api/teacher/courses/{course_id}/lessons/{lesson_id}/ - 获取课时详情（含内容块，懒加载第二步）
    # PUT    /api/teacher/courses/{course_id}/lessons/{lesson_id}/ - 更新课时信息
    # DELETE /api/teacher/courses/{course_id}/lessons/{lesson_id}/ - 删除课时
    path('teacher/courses/<int:course_id>/lessons/<int:lesson_id>/', views.TeacherLessonDetailView.as_view(), name='teacher-lesson-detail'),
    
    # ===== 教师内容块管理 =====
    # POST   /api/teacher/courses/{course_id}/lessons/{lesson_id}/content-blocks/ - 批量保存内容块（全量保存）
    path('teacher/courses/<int:course_id>/lessons/<int:lesson_id>/content-blocks/', views.TeacherContentBlockManageView.as_view(), name='teacher-content-blocks'),
    
    # POST   /api/teacher/courses/{course_id}/lessons/{lesson_id}/content-blocks/upload/ - 上传内容块文件
    path('teacher/courses/<int:course_id>/lessons/<int:lesson_id>/content-blocks/upload/', views.TeacherContentBlockFileUploadView.as_view(), name='teacher-content-block-upload'),
    

    # ===== 教师学生管理 =====
    
    # GET    /api/teacher/courses/{courseId}/students/ - 获取课程学生列表
    # POST   /api/teacher/courses/{courseId}/students/ - 手动添加学生
    path('teacher/courses/<int:course_id>/students/', views.TeacherCourseStudentManageView.as_view(), name='teacher-course-students'),
    
    # DELETE /api/teacher/courses/{courseId}/students/{studentId}/ - 移除学生
    path('teacher/courses/<int:course_id>/students/<int:student_id>/', views.TeacherStudentDetailView.as_view(), name='teacher-student-detail'),
    
    # GET    /api/teacher/courses/{courseId}/students/{studentId}/progress/ - 获取学生学习进度------(待定)
    path('teacher/courses/<int:course_id>/students/<int:student_id>/progress/', views.TeacherStudentProgressView.as_view(), name='teacher-student-progress'),
    
    # ===== 班级与学期管理 =====
    # GET    /api/teacher/courses/{courseId}/terms/ - 获取学期列表
    # POST   /api/teacher/courses/{courseId}/terms/ - 创建学期
    path('teacher/courses/<int:course_id>/terms/', views.TeacherTermManageView.as_view(), name='teacher-terms'),
    
    # PUT    /api/teacher/courses/{courseId}/terms/{id}/ - 更新学期
    # DELETE /api/teacher/courses/{courseId}/terms/{id}/ - 删除学期
    path('teacher/courses/<int:course_id>/terms/<int:term_id>/', views.TeacherTermDetailView.as_view(), name='teacher-term-detail'),
    
    # GET    /api/teacher/courses/{courseId}/classes/ - 获取班级列表
    # POST   /api/teacher/courses/{courseId}/classes/ - 创建班级
    path('teacher/courses/<int:course_id>/classes/', views.TeacherClassManageView.as_view(), name='teacher-classes'),
    
    # PUT    /api/teacher/courses/{courseId}/classes/{id}/ - 更新班级
    # DELETE /api/teacher/courses/{courseId}/classes/{id}/ - 删除班级
    path('teacher/courses/<int:course_id>/classes/<int:class_id>/', views.TeacherClassDetailView.as_view(), name='teacher-class-detail'),
    
    # ===== 数据统计 =====
    # GET    /api/teacher/courses/{courseId}/statistics/ - 获取课程统计数据------(待定)
    path('teacher/courses/<int:course_id>/statistics/', views.TeacherCourseStatisticsView.as_view(), name='teacher-course-statistics'),
    
    # GET    /api/teacher/dashboard/ - 获取教师仪表板数据------(待定)
    path('teacher/dashboard/', views.TeacherDashboardView.as_view(), name='teacher-dashboard'),
]
