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
    
    # GET    /api/teacher/courses/{id}/ - 获取课程管理详情
    path('teacher/courses/<int:pk>/', views.TeacherCourseDetailView.as_view(), name='teacher-course-detail'),
    
    # POST   /api/teacher/courses/ - 创建课程
    path('teacher/courses/create/', views.TeacherCourseCreateView.as_view(), name='teacher-course-create'),
    
    # PUT    /api/teacher/courses/{id}/ - 更新课程------(待定)
    path('teacher/courses/<int:pk>/', views.TeacherCourseUpdateView.as_view(), name='teacher-course-update'),
    
    # DELETE /api/teacher/courses/{id}/ - 删除课程
    path('teacher/courses/<int:pk>/', views.TeacherCourseDeleteView.as_view(), name='teacher-course-delete'),
    
    # POST   /api/teacher/courses/{id}/publish/ - 发布课程
    path('teacher/courses/<int:pk>/publish/', views.TeacherCoursePublishView.as_view(), name='teacher-course-publish'),
    
    # POST   /api/teacher/courses/{id}/cover/ - 上传课程封面
    path('teacher/courses/<int:pk>/cover/', views.TeacherCourseCoverUploadView.as_view(), name='teacher-course-cover-upload'),
    
    # ===== 教师章节管理 =====
    # GET    /api/teacher/courses/{courseId}/chapters/ - 获取章节列表
    path('teacher/courses/<int:course_id>/chapters/', views.TeacherChapterListView.as_view(), name='teacher-chapter-list'),
    
    # POST   /api/teacher/courses/{courseId}/chapters/ - 创建章节
    path('teacher/courses/<int:course_id>/chapters/', views.TeacherChapterCreateView.as_view(), name='teacher-chapter-create'),
    
    # PUT    /api/teacher/courses/{courseId}/chapters/{id}/ - 更新章节
    path('teacher/courses/<int:course_id>/chapters/<int:chapter_id>/', views.TeacherChapterUpdateView.as_view(), name='teacher-chapter-update'),
    
    # DELETE /api/teacher/courses/{courseId}/chapters/{id}/ - 删除章节
    path('teacher/courses/<int:course_id>/chapters/<int:chapter_id>/', views.TeacherChapterDeleteView.as_view(), name='teacher-chapter-delete'),
    
    # POST   /api/teacher/courses/{courseId}/chapters/sort/ - 排序章节
    path('teacher/courses/<int:course_id>/chapters/sort/', views.TeacherChapterSortView.as_view(), name='teacher-chapter-sort'),
    
    # ===== 教师学生管理 =====
    # GET    /api/teacher/courses/{courseId}/students/ - 获取课程学生列表
    path('teacher/courses/<int:course_id>/students/', views.TeacherCourseStudentListView.as_view(), name='teacher-course-students'),
    
    # GET    /api/teacher/courses/{courseId}/students/{studentId}/progress/ - 获取学生学习进度
    path('teacher/courses/<int:course_id>/students/<int:student_id>/progress/', views.TeacherStudentProgressView.as_view(), name='teacher-student-progress'),
    
    # ===== 班级与学期管理 =====
    # GET    /api/teacher/courses/{courseId}/terms/ - 获取学期列表
    path('teacher/courses/<int:course_id>/terms/', views.TeacherTermListView.as_view(), name='teacher-term-list'),
    
    # POST   /api/teacher/courses/{courseId}/terms/ - 创建学期
    path('teacher/courses/<int:course_id>/terms/', views.TeacherTermCreateView.as_view(), name='teacher-term-create'),
    
    # PUT    /api/teacher/courses/{courseId}/terms/{id}/ - 更新学期
    path('teacher/courses/<int:course_id>/terms/<int:term_id>/', views.TeacherTermUpdateView.as_view(), name='teacher-term-update'),
    
    # DELETE /api/teacher/courses/{courseId}/terms/{id}/ - 删除学期
    path('teacher/courses/<int:course_id>/terms/<int:term_id>/', views.TeacherTermDeleteView.as_view(), name='teacher-term-delete'),
    
    # GET    /api/teacher/courses/{courseId}/classes/ - 获取班级列表
    path('teacher/courses/<int:course_id>/classes/', views.TeacherClassListView.as_view(), name='teacher-class-list'),
    
    # POST   /api/teacher/courses/{courseId}/classes/ - 创建班级
    path('teacher/courses/<int:course_id>/classes/', views.TeacherClassCreateView.as_view(), name='teacher-class-create'),
    
    # PUT    /api/teacher/courses/{courseId}/classes/{id}/ - 更新班级
    path('teacher/courses/<int:course_id>/classes/<int:class_id>/', views.TeacherClassUpdateView.as_view(), name='teacher-class-update'),
    
    # DELETE /api/teacher/courses/{courseId}/classes/{id}/ - 删除班级
    path('teacher/courses/<int:course_id>/classes/<int:class_id>/', views.TeacherClassDeleteView.as_view(), name='teacher-class-delete'),
    
    # ===== 数据统计 =====
    # GET    /api/teacher/courses/{courseId}/statistics/ - 获取课程统计数据
    path('teacher/courses/<int:course_id>/statistics/', views.TeacherCourseStatisticsView.as_view(), name='teacher-course-statistics'),
    
    # GET    /api/teacher/dashboard/ - 获取教师仪表板数据
    path('teacher/dashboard/', views.TeacherDashboardView.as_view(), name='teacher-dashboard'),
]
