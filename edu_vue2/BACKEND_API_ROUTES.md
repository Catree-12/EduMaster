# 后端 API 路由对接文档

> 本文档列出前端所有 API 请求对应的后端路由，用于后端开发参考

---

## 基础配置

**Base URL**: `http://localhost:8000/api`  
**生产环境**: `https://api.yourdomain.com/api`

**认证方式**: JWT Bearer Token  
**请求头**: `Authorization: Bearer <token>`

---

## 1. 认证模块 (Authentication)

> **注意**: 认证模块只负责认证相关功能，用户信息管理请查看"用户模块"

| 方法 | 路由 | 前端调用 | 说明 | 请求体 | 响应体 |
|-----|------|---------|------|--------|--------|
| POST | `/api/auth/register/` | `authAPI.register()` | 用户注册 | `{ username, email, password, password_confirm }` | `{ user, message }` |
| POST | `/api/auth/login/` | `authAPI.login()` | 用户登录 | `{ email, password }` | `{ token, refresh_token, user }` |
| POST | `/api/auth/logout/` | `authAPI.logout()` | 用户登出 | - | `{ message }` |
| POST | `/api/auth/forget-password/` | `authAPI.forgetPassword()` | 忘记密码 | `{ email }` | `{ message }` |
| POST | `/api/auth/change-password/` | `authAPI.changePassword()` | 修改密码（需登录） | `{ old_password, new_password, confirm_password }` | `{ message }` |


## 2. 用户模块 (Users)

| 方法 | 路由 | 前端调用 | 说明 | 请求体/参数 |
|-----|------|---------|------|------------|
| GET | `/api/users/me/` | `userAPI.getCurrentUser()` | 获取当前登录用户基本信息 | - |
| GET | `/api/users/{id}/` | `userAPI.getUserInfo()` | 获取指定用户详情 | - |
| GET | `/api/users/profile/` | `userAPI.getCurrentUserProfile()` | 获取当前用户完整信息（含 profile） | - |
| PATCH | `/api/users/profile/` | `userAPI.updateUserInfo()` | 更新用户信息 | `{ nickname, bio, gender, school, major }` |
| POST | `/api/users/avatar/` | `userAPI.uploadAvatar()` | 上传头像 | `FormData: { avatar: file }` |
| GET | `/api/users/stats/learning/` | `userAPI.getLearningStats()` | 获取学习统计 | - |
| GET | `/api/users/stats/grades/` | `userAPI.getGradeStats()` | 获取成绩统计 | - |
| GET | `/api/users/certificates/` | `userAPI.getCertificates()` | 获取证书列表 | `?page=1&pageSize=10` |
| GET | `/api/users/certificates/{id}/` | `userAPI.getCertificateDetail()` | 获取证书详情 | - |
| POST | `/api/users/courses/{courseId}/certificate/` | `userAPI.generateCourseCertificate()` | 生成课程证书 | - |
| POST | `/api/users/certificates/{id}/share/` | `userAPI.generateCertificateShareLink()` | 生成证书分享链接 | `{ password?, expiryDays? }` |
| GET | `/api/users/certificates/{id}/download/` | `userAPI.downloadCertificate()` | 下载证书文件 | - |
| GET | `/api/users/messages/` | `userAPI.getMessages()` | 获取消息列表 | `?page=1&pageSize=10` |
| POST | `/api/users/messages/{id}/read/` | `userAPI.markMessageAsRead()` | 标记消息已读 | - |
| GET | `/api/users/stats/certificates/` | `userAPI.getCertificateStats()` | 获取证书统计信息 | - |

---

## 3. 课程模块 (Courses)

### 3.1 公共课程接口

| 方法 | 路由 | 前端调用 | 说明 | 参数 |
|-----|------|---------|------|------|
| GET | `/api/courses/` | `courseAPI.getCourseList()` | 获取课程列表 | `?page=1&pageSize=10&category=xxx` |
| GET | `/api/courses/{id}/` | `courseAPI.getCourseDetail()` | 获取课程详情 | - |
| GET | `/api/courses/{id}/resources/` | `courseAPI.getCourseResources()` | 获取课程资源 | - |
| GET | `/api/courses/my-courses/` | `courseAPI.getMyCourses()` | 获取我的课程 | `?page=1` |

### 3.2 学生选课

| 方法 | 路由 | 前端调用 | 说明 |
|-----|------|---------|------|
| GET | `/api/student/enrollments/` | `studentAPI.getStudentEnrollments()` | 获取选课列表 |
| POST | `/api/student/enrollments/` | `studentAPI.enrollCourse()` | 选课 |
| DELETE | `/api/student/enrollments/{id}/` | `studentAPI.unenrollCourse()` | 退课 |
    
### 3.3 学生学习

| 方法 | 路由 | 前端调用 | 说明 |
|-----|------|---------|------|
| GET | `/api/student/courses/{courseId}/` | `studentAPI.getStudentCourse()` | 获取课程学习详情 |
| POST | `/api/student/courses/{courseId}/progress/` | `studentAPI.updateLearningProgress()` | 更新学习进度 |
| GET | `/api/student/courses/{courseId}/lessons/{lessonId}/` | `studentAPI.getStudentLesson()` | 获取课时详情 |
| POST | `/api/student/courses/{courseId}/lessons/{lessonId}/complete/` | `studentAPI.completeLessonStudy()` | 完成课时学习 |

### 3.4 教师课程管理

| 方法 | 路由 | 前端调用 | 说明 |
|-----|------|---------|------|
| GET | `/api/teacher/courses/` | `teacherAPI.getTeacherCourses()` | 获取我教的课程 |
| GET | `/api/teacher/courses/{id}/` | `teacherAPI.getTeacherCourse()` | 获取课程管理详情 |
| POST | `/api/teacher/courses/` | `teacherAPI.createCourse()` | 创建课程 |
| PUT | `/api/teacher/courses/{id}/` | `teacherAPI.updateCourse()` | 更新课程 |
| DELETE | `/api/teacher/courses/{id}/` | `teacherAPI.deleteCourse()` | 删除课程 |
| POST | `/api/teacher/courses/{id}/publish/` | `teacherAPI.publishCourse()` | 发布课程 |

### 3.5 教师章节管理

| 方法 | 路由 | 前端调用 | 说明 |
|-----|------|---------|------|
| GET | `/api/teacher/courses/{courseId}/chapters/` | `teacherAPI.getCourseChapters()` | 获取章节列表 |
| POST | `/api/teacher/courses/{courseId}/chapters/` | `teacherAPI.createChapter()` | 创建章节 |
| PUT | `/api/teacher/courses/{courseId}/chapters/{id}/` | `teacherAPI.updateChapter()` | 更新章节 |
| DELETE | `/api/teacher/courses/{courseId}/chapters/{id}/` | `teacherAPI.deleteChapter()` | 删除章节 |
| POST | `/api/teacher/courses/{courseId}/chapters/sort/` | `teacherAPI.sortChapters()` | 排序章节 |

### 3.6 教师学生管理

| 方法 | 路由 | 前端调用 | 说明 |
|-----|------|---------|------|
| GET | `/api/teacher/courses/{courseId}/students/` | `teacherAPI.getCourseStudents()` | 获取课程学生列表 |
| GET | `/api/teacher/courses/{courseId}/students/{studentId}/progress/` | `teacherAPI.getStudentProgress()` | 获取学生学习进度 |

---

## 4. 作业模块 (Homework/Assignments)

### 4.1 学生作业

| 方法 | 路由 | 前端调用 | 说明 |
|-----|------|---------|------|
| GET | `/api/student/homework/` | `studentAPI.getStudentHomeworkList()` | 获取作业列表 |
| GET | `/api/student/courses/{courseId}/homework/{homeworkId}/` | `studentAPI.getStudentHomework()` | 获取作业详情 |
| POST | `/api/student/courses/{courseId}/homework/{homeworkId}/submit/` | `studentAPI.submitHomework()` | 提交作业 |
| GET | `/api/student/courses/{courseId}/homework/{homeworkId}/submission/` | `studentAPI.getStudentHomeworkSubmission()` | 获取作业提交详情 |

### 4.2 教师作业管理

| 方法 | 路由 | 前端调用 | 说明 |
|-----|------|---------|------|
| GET | `/api/teacher/homework/` | `teacherAPI.getTeacherHomework()` | 获取作业库 |
| GET | `/api/teacher/homework/{id}/` | `teacherAPI.getHomeworkDetail()` | 获取作业详情 |
| POST | `/api/teacher/homework/` | `teacherAPI.createHomework()` | 创建作业 |
| PUT | `/api/teacher/homework/{id}/` | `teacherAPI.updateHomework()` | 更新作业 |
| DELETE | `/api/teacher/homework/{id}/` | `teacherAPI.deleteHomework()` | 删除作业 |
| POST | `/api/teacher/homework/{id}/publish/` | `teacherAPI.publishHomework()` | 发布作业 |
| GET | `/api/teacher/homework/{id}/submissions/` | `teacherAPI.getHomeworkSubmissions()` | 获取作业提交列表 |
| POST | `/api/teacher/homework/{id}/submissions/{submissionId}/grade/` | `teacherAPI.gradeHomework()` | 批改作业 |

---

## 5. 考试模块 (Exams)

### 5.1 学生考试

| 方法 | 路由 | 前端调用 | 说明 |
|-----|------|---------|------|
| GET | `/api/student/exams/` | `studentAPI.getStudentExamList()` | 获取考试列表 |
| GET | `/api/student/courses/{courseId}/exams/{examId}/` | `studentAPI.getStudentExam()` | 获取考试详情 |
| POST | `/api/student/courses/{courseId}/exams/{examId}/start/` | `studentAPI.startExam()` | 开始考试 |
| POST | `/api/student/courses/{courseId}/exams/{examId}/submit/` | `studentAPI.submitExam()` | 提交答卷 |
| GET | `/api/student/courses/{courseId}/exams/{examId}/result/` | `studentAPI.getStudentExamResult()` | 获取考试成绩 |

### 5.2 教师考试管理

| 方法 | 路由 | 前端调用 | 说明 |
|-----|------|---------|------|
| GET | `/api/teacher/exams/` | `teacherAPI.getTeacherExams()` | 获取试卷库 |
| GET | `/api/teacher/exams/{id}/` | `teacherAPI.getExamDetail()` | 获取试卷详情 |
| POST | `/api/teacher/exams/` | `teacherAPI.createExam()` | 创建试卷 |
| PUT | `/api/teacher/exams/{id}/` | `teacherAPI.updateExam()` | 更新试卷 |
| DELETE | `/api/teacher/exams/{id}/` | `teacherAPI.deleteExam()` | 删除试卷 |
| POST | `/api/teacher/exams/{id}/publish/` | `teacherAPI.publishExam()` | 发布试卷 |
| GET | `/api/teacher/exams/{id}/submissions/` | `teacherAPI.getExamSubmissions()` | 获取考试提交列表 |
| POST | `/api/teacher/exams/{id}/submissions/{submissionId}/grade/` | `teacherAPI.gradeExam()` | 批改试卷 |

---

## 6. 社区模块 (Community)

### 6.1 公共社区

| 方法 | 路由 | 前端调用 | 说明 |
|-----|------|---------|------|
| GET | `/api/community/questions/` | `communityAPI.getPublicQuestions()` | 获取社区问题列表 |
| GET | `/api/community/questions/{id}/` | `communityAPI.getQuestionDetail()` | 获取问题详情 |
| POST | `/api/community/questions/` | `communityAPI.postQuestion()` | 发布问题 |
| PUT | `/api/community/questions/{id}/` | `communityAPI.updateQuestion()` | 编辑问题 |
| DELETE | `/api/community/questions/{id}/` | `communityAPI.deleteQuestion()` | 删除问题 |
| POST | `/api/community/questions/{id}/like/` | `communityAPI.likeQuestion()` | 点赞问题 |

### 6.2 问答

| 方法 | 路由 | 前端调用 | 说明 |
|-----|------|---------|------|
| POST | `/api/community/questions/{id}/answers/` | `communityAPI.postAnswer()` | 回答问题 |
| PUT | `/api/community/answers/{id}/` | `communityAPI.updateAnswer()` | 编辑回答 |
| DELETE | `/api/community/answers/{id}/` | `communityAPI.deleteAnswer()` | 删除回答 |
| POST | `/api/community/answers/{id}/like/` | `communityAPI.likeAnswer()` | 点赞回答 |

### 6.3 课程社区（学生）

| 方法 | 路由 | 前端调用 | 说明 |
|-----|------|---------|------|
| GET | `/api/student/courses/{courseId}/threads/` | `studentAPI.getStudentCourseThreads()` | 获取课程话题列表 |
| GET | `/api/student/courses/{courseId}/threads/{threadId}/` | `studentAPI.getStudentThread()` | 获取话题详情 |
| POST | `/api/student/courses/{courseId}/threads/` | `studentAPI.createStudentThread()` | 发布话题 |
| PUT | `/api/student/courses/{courseId}/threads/{threadId}/` | `studentAPI.updateStudentThread()` | 编辑话题 |
| DELETE | `/api/student/courses/{courseId}/threads/{threadId}/` | `studentAPI.deleteStudentThread()` | 删除话题 |
| POST | `/api/student/courses/{courseId}/threads/{threadId}/comments/` | `studentAPI.createStudentThreadComment()` | 发布评论 |

### 6.4 课程社区（教师）

| 方法 | 路由 | 前端调用 | 说明 |
|-----|------|---------|------|
| GET | `/api/teacher/courses/{courseId}/threads/` | `teacherAPI.getTeacherCourseThreads()` | 获取课程话题列表 |
| GET | `/api/teacher/courses/{courseId}/threads/{threadId}/` | `teacherAPI.getTeacherThread()` | 获取话题详情 |
| POST | `/api/teacher/courses/{courseId}/threads/` | `teacherAPI.createTeacherThread()` | 发布公告/话题 |
| PUT | `/api/teacher/courses/{courseId}/threads/{threadId}/` | `teacherAPI.updateTeacherThread()` | 编辑话题 |
| DELETE | `/api/teacher/courses/{courseId}/threads/{threadId}/` | `teacherAPI.deleteTeacherThread()` | 删除话题 |
| POST | `/api/teacher/courses/{courseId}/threads/{threadId}/pin/` | `teacherAPI.pinThread()` | 置顶话题 |
| POST | `/api/teacher/courses/{courseId}/threads/{threadId}/unpin/` | `teacherAPI.unpinThread()` | 取消置顶 |

---

## 7. 班级与学期模块 (Classes & Terms)

| 方法 | 路由 | 前端调用 | 说明 |
|-----|------|---------|------|
| GET | `/api/teacher/courses/{courseId}/terms/` | `teacherAPI.getCourseTerms()` | 获取学期列表 |
| POST | `/api/teacher/courses/{courseId}/terms/` | `teacherAPI.createTerm()` | 创建学期 |
| PUT | `/api/teacher/courses/{courseId}/terms/{id}/` | `teacherAPI.updateTerm()` | 更新学期 |
| DELETE | `/api/teacher/courses/{courseId}/terms/{id}/` | `teacherAPI.deleteTerm()` | 删除学期 |
| GET | `/api/teacher/courses/{courseId}/classes/` | `teacherAPI.getCourseClasses()` | 获取班级列表 |
| POST | `/api/teacher/courses/{courseId}/classes/` | `teacherAPI.createClass()` | 创建班级 |
| PUT | `/api/teacher/courses/{courseId}/classes/{id}/` | `teacherAPI.updateClass()` | 更新班级 |
| DELETE | `/api/teacher/courses/{courseId}/classes/{id}/` | `teacherAPI.deleteClass()` | 删除班级 |

## 8. 证书模块 (Certificates)

> **注意**: 证书路由已统一到用户模块 `/api/users/certificates/`，因为用户可能同时拥有学生和教师身份

| 方法 | 路由 | 前端调用 | 说明 |
|-----|------|---------|------|
| GET | `/api/users/certificates/` | `userAPI.getCertificates()` | 获取证书列表 |
| GET | `/api/users/certificates/{id}/` | `userAPI.getCertificateDetail()` | 获取证书详情 |
| POST | `/api/users/courses/{courseId}/certificate/` | `userAPI.generateCourseCertificate()` | 生成课程证书 |

---

## 9. 管理员模块 (Admin)

### 9.1 仪表板

| 方法 | 路由 | 前端调用 | 说明 |
|-----|------|---------|------|
| GET | `/api/admin/dashboard/stats/` | `adminAPI.getDashboardStats()` | 获取平台统计数据 |
| GET | `/api/admin/dashboard/pending-tasks/` | `adminAPI.getPendingTasks()` | 获取待处理任务 |

### 9.2 课程审核

| 方法 | 路由 | 前端调用 | 说明 |
|-----|------|---------|------|
| GET | `/api/admin/courses/pending/` | `adminAPI.getPendingCourses()` | 获取待审核课程列表 |
| GET | `/api/admin/courses/audit-list/` | `adminAPI.getCourseAuditList()` | 获取课程审核列表 |
| GET | `/api/admin/courses/{id}/audit-detail/` | `adminAPI.getCourseAuditDetail()` | 获取审核详情 |
| POST | `/api/admin/courses/{id}/approve/` | `adminAPI.approveCourse()` | 审核通过 |
| POST | `/api/admin/courses/{id}/reject/` | `adminAPI.rejectCourse()` | 审核拒绝 |

### 9.3 用户管理

| 方法 | 路由 | 前端调用 | 说明 |
|-----|------|---------|------|
| GET | `/api/admin/users/` | `adminAPI.getAllUsers()` | 获取所有用户 |
| GET | `/api/admin/users/{id}/` | `adminAPI.getUserDetail()` | 获取用户详情 |
| PUT | `/api/admin/users/{id}/` | `adminAPI.updateUser()` | 更新用户信息 |
| POST | `/api/admin/users/{id}/disable/` | `adminAPI.disableUser()` | 禁用用户 |
| POST | `/api/admin/users/{id}/enable/` | `adminAPI.enableUser()` | 启用用户 |
| POST | `/api/admin/users/batch-disable/` | `adminAPI.batchDisableUsers()` | 批量禁用 |
| POST | `/api/admin/users/batch-enable/` | `adminAPI.batchEnableUsers()` | 批量启用 |

---

## 10. 数据统计模块 (Statistics)

| 方法 | 路由 | 前端调用 | 说明 |
|-----|------|---------|------|
| GET | `/api/teacher/courses/{courseId}/statistics/` | `teacherAPI.getCourseStatistics()` | 获取课程统计数据 |
| GET | `/api/teacher/dashboard/` | `teacherAPI.getTeacherDashboard()` | 获取教师仪表板数据 |

---

## 通用响应格式

### 成功响应
```json
{
  "code": 200,
  "data": { ... },
  "message": "操作成功"
}
```

### 分页响应
```json
{
  "code": 200,
  "data": {
    "results": [ ... ],
    "count": 100,
    "next": "http://api/endpoint/?page=2",
    "previous": null,
    "page": 1,
    "pageSize": 10,
    "totalPages": 10
  }
}
```

### 错误响应
```json
{
  "code": 400,
  "error": "详细错误信息",
  "message": "操作失败"
}
```

---

## HTTP 状态码

| 状态码 | 说明 |
|-------|------|
| 200 | 成功 |
| 201 | 创建成功 |
| 204 | 删除成功（无内容返回） |
| 400 | 请求参数错误 |
| 401 | 未认证/Token 过期 |
| 403 | 无权限访问 |
| 404 | 资源不存在 |
| 500 | 服务器内部错误 |

---

## 权限说明

### 角色类型
- `student` - 学生
- `teacher` - 教师
- `admin` - 管理员

### 路由权限
- `/api/auth/*` - 无需认证（除 logout 外）
- `/api/student/*` - 需要 student 角色
- `/api/teacher/*` - 需要 teacher 角色
- `/api/admin/*` - 需要 admin 角色
- `/api/users/*` - 需要认证
- `/api/courses/` - 公开访问
- `/api/community/*` - 需要认证

---

## 请求头示例

```http
POST /api/auth/login/ HTTP/1.1
Host: localhost:8000
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}
```

```http
GET /api/users/profile/ HTTP/1.1
Host: localhost:8000
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

```http
POST /api/users/avatar/ HTTP/1.1
Host: localhost:8000
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary

------WebKitFormBoundary
Content-Disposition: form-data; name="avatar"; filename="avatar.jpg"
Content-Type: image/jpeg

[binary data]
------WebKitFormBoundary--
```

---

## 环境变量配置

**开发环境** (`.env.development`):
```env
VUE_APP_API_URL=http://localhost:8000/api
VUE_APP_MEDIA_URL=http://localhost:8000/media
```

**生产环境** (`.env.production`):
```env
VUE_APP_API_URL=https://api.yourdomain.com/api
VUE_APP_MEDIA_URL=https://cdn.yourdomain.com/media
```

## 总计

- **认证模块**: 5 个接口(只负责认证)
- **用户模块**: 15 个接口(含证书管理)
- **课程模块(公共)**: 4 个接口
- **学生模块**: 24 个接口
- **教师模块**: 45+ 个接口
- **社区模块**: 14 个接口
- **管理员模块**: 20+ 个接口

**总计约 120+ 个后端 API 接口需要实现**
