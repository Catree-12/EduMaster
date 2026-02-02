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

### 6. Django模型建议

#### 核心模型
```python
# models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """用户模型"""
    ROLE_CHOICES = [
        ('student', '学生'),
        ('teacher', '教师'),
        ('admin', '管理员'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    
class Course(models.Model):
    """课程模型"""
    STATUS_CHOICES = [
        ('draft', '草稿'),
        ('pending', '待审核'),
        ('published', '已发布'),
        ('rejected', '已拒绝'),
    ]
    title = models.CharField(max_length=200)
    description = models.TextField()
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
class Chapter(models.Model):
    """章节模型"""
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='chapters')
    title = models.CharField(max_length=200)
    order = models.IntegerField(default=0)
    
class Lesson(models.Model):
    """课时模型"""
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    video_url = models.URLField(null=True, blank=True)
    duration = models.IntegerField(default=0)  # 秒
    order = models.IntegerField(default=0)
    
class Enrollment(models.Model):
    """选课记录"""
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)
    progress = models.FloatField(default=0.0)  # 0-100
    
class Homework(models.Model):
    """作业模型"""
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    deadline = models.DateTimeField(null=True, blank=True)
    total_points = models.IntegerField(default=100)
    
class HomeworkSubmission(models.Model):
    """作业提交"""
    homework = models.ForeignKey(Homework, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    score = models.IntegerField(null=True, blank=True)
    feedback = models.TextField(null=True, blank=True)
    
class Exam(models.Model):
    """考试模型"""
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    duration = models.IntegerField(default=60)  # 分钟
    total_points = models.IntegerField(default=100)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
```

### 7. JWT认证配置

#### Django设置
```python
# settings.py
INSTALLED_APPS = [
    'rest_framework',
    'rest_framework_simplejwt',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
}
```

### 8. 权限控制

#### Django权限装饰器
```python
from rest_framework.permissions import BasePermission

class IsTeacher(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'teacher'

class IsStudent(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'student'

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'admin'
```

### 9. 前端使用示例

```javascript
// 在组件中使用
import { studentAPI } from '@/api'

export default {
  async mounted() {
    // 获取我的选课
    const enrollments = await studentAPI.getStudentEnrollments()
    
    // 提交作业
    await studentAPI.submitHomework(courseId, homeworkId, {
      content: this.answer
    })
  }
}
```

### 10. 下一步工作

#### 前端 (已完成)
- ✅ 路由结构重构
- ✅ API文件规范化
- ✅ 创建student.js和teacher.js
- ✅ 统一路径命名

#### 后端 (待开发)
1. 创建Django项目和应用
2. 配置JWT认证
3. 实现用户模型和角色系统
4. 实现核心业务模型
5. 开发RESTful API
6. 编写序列化器
7. 实现权限控制
8. 添加API文档(drf-yasg)

### 11. 测试建议

- 使用Postman测试所有API接口
- 前端使用Mock数据先行开发
- 集成测试时逐个接口对接
- 使用Django TestCase编写单元测试

### 12. 联系方式

如有疑问,请查看:
- 路由规范: `/ROUTE_STRUCTURE.md`
- API规范: `/src/api/README.md`
