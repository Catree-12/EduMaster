# 前后端接口对接指南

## 项目规范总结

### 1. 技术栈
- **前端**: Vue 2 + Vue Router + Vuex + Element UI + Axios
- **后端**: Django 5.1 + Django REST Framework + JWT + MySQL 8.4
- **认证**: JWT (JSON Web Token)

### 2. 目录结构已优化

#### 前端目录
```
src/
├── api/              # API接口(已规范化)
│   ├── student.js    # 学生API(新)
│   ├── teacher.js    # 教师API(新)
│   ├── auth.js       # 认证API
│   ├── course.js     # 课程API
│   ├── exam.js       # 考试API
│   ├── assignment.js # 作业API
│   ├── community.js  # 社区API
│   ├── admin.js      # 管理员API
│   ├── user.js       # 用户API
│   ├── http.js       # Axios配置
│   └── index.js      # 统一导出
├── views/            # 页面组件(已统一)
├── components/       # 公共组件
├── router/           # 路由配置(已重构)
└── store/            # Vuex状态管理
```

### 3. 路由规范

#### 学生路由 (前缀: `/student`)
```
/student/enrollments                           # 我的学习
/student/courses/:courseId                     # 课程学习
/student/courses/:courseId/lessons/:lessonId   # 课时学习
/student/courses/:courseId/homework/:hwId      # 作业
/student/courses/:courseId/exams/:examId       # 考试
/student/courses/:courseId/threads/:threadId   # 课程讨论
```

#### 教师路由 (前缀: `/teacher`)
```
/teacher/courses                               # 课程列表
/teacher/courses/create                        # 创建课程
/teacher/courses/:id                           # 课程管理
/teacher/courses/:id/chapters                  # 章节管理
/teacher/homework                              # 作业库
/teacher/homework/:id/grading                  # 作业批改
/teacher/exams                                 # 考试库
/teacher/exams/:id/grading                     # 考试批改
```

#### 管理员路由 (前缀: `/admin`)
```
/admin/dashboard                               # 仪表盘
/admin/users                                   # 用户管理
/admin/courses/audit                           # 课程审核
/admin/content/review                          # 内容审查
```

### 4. API接口规范

#### 基础配置
```javascript
// http.js
const API_BASE_URL = process.env.VUE_APP_API_URL || 'http://localhost:8000/api'

// 请求头自动携带Token
headers: {
  Authorization: `Bearer ${token}`
}
```

#### RESTful风格
```
GET    /api/resource          # 获取列表
GET    /api/resource/:id      # 获取详情
POST   /api/resource          # 创建
PUT    /api/resource/:id      # 更新
DELETE /api/resource/:id      # 删除
```

#### 响应格式
```json
{
  "code": 200,
  "message": "success",
  "data": {
    // 实际数据
  }
}
```

### 5. Django后端需实现的接口

#### 认证接口 (auth/)
```python
# urls.py
urlpatterns = [
    path('auth/login/', LoginView.as_view()),
    path('auth/register/', RegisterView.as_view()),
    path('auth/logout/', LogoutView.as_view()),
    path('auth/refresh/', RefreshTokenView.as_view()),
    path('auth/profile/', ProfileView.as_view()),
]
```

#### 学生接口 (student/)
```python
urlpatterns = [
    # 选课
    path('student/enrollments/', EnrollmentListView.as_view()),
    path('student/enrollments/', EnrollCourseView.as_view()),
    
    # 学习
    path('student/courses/<int:course_id>/', StudentCourseDetailView.as_view()),
    path('student/courses/<int:course_id>/progress/', UpdateProgressView.as_view()),
    
    # 作业
    path('student/courses/<int:course_id>/homework/<int:hw_id>/', 
         StudentHomeworkDetailView.as_view()),
    path('student/courses/<int:course_id>/homework/<int:hw_id>/submit/', 
         SubmitHomeworkView.as_view()),
    
    # 考试
    path('student/courses/<int:course_id>/exams/<int:exam_id>/', 
         StudentExamDetailView.as_view()),
    path('student/courses/<int:course_id>/exams/<int:exam_id>/submit/', 
         SubmitExamView.as_view()),
]
```

#### 教师接口 (teacher/)
```python
urlpatterns = [
    # 课程管理
    path('teacher/courses/', TeacherCourseListView.as_view()),
    path('teacher/courses/', CreateCourseView.as_view()),
    path('teacher/courses/<int:pk>/', CourseDetailView.as_view()),
    
    # 章节管理
    path('teacher/courses/<int:course_id>/chapters/', ChapterListView.as_view()),
    path('teacher/courses/<int:course_id>/chapters/<int:pk>/', 
         ChapterDetailView.as_view()),
    
    # 作业管理
    path('teacher/homework/', HomeworkLibraryView.as_view()),
    path('teacher/homework/<int:pk>/submissions/', 
         HomeworkSubmissionsView.as_view()),
    path('teacher/homework/<int:hw_id>/submissions/<int:sub_id>/grade/', 
         GradeHomeworkView.as_view()),
    
    # 考试管理
    path('teacher/exams/', ExamLibraryView.as_view()),
    path('teacher/exams/<int:pk>/submissions/', 
         ExamSubmissionsView.as_view()),
]
```