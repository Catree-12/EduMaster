# API 接口规范

## 目录结构
```
api/
├── index.js           # 统一导出（推荐使用）
├── http.js            # Axios 配置
├── auth.js            # 认证相关
├── user.js            # 用户相关
├── course.js          # 课程公共 API
├── student.js         # 学生功能
├── teacher.js         # 教师功能
├── assignment.js      # 作业管理
├── exam.js            # 考试管理
├── community.js       # 社区功能
├── admin.js           # 管理员功能
└── services.js        # 废弃的兼容层（不推荐使用）
```

## 使用方式

### 推荐方式（使用命名导出）
```javascript
// 导入 API 模块
import { courseAPI, teacherAPI, studentAPI, authAPI } from '@/api'
import { getTeacherCourses, createCourse } from '@/api'

// 调用
const courses = await courseAPI.getCourseList({ page: 1, size: 10 })
const detail = await courseAPI.getCourseDetail(courseId)
const teacherCourses = await getTeacherCourses({ page: 1 })
await createCourse(courseData)
```

### 不推荐方式（已废弃）
```javascript
// ❌ 不推荐：使用 services.js（会显示废弃警告）
import { courseService } from '@/api/services'
```

## RESTful 规范

### 基础URL
```
开发环境: http://localhost:8000/api
生产环境: https://your-domain.com/api
```

### HTTP方法
- GET: 获取资源
- POST: 创建资源
- PUT: 更新资源(完整更新)
- PATCH: 更新资源(部分更新)
- DELETE: 删除资源

### 响应格式
```javascript
{
  "code": 200,           // 状态码
  "message": "success",  // 消息
  "data": {}            // 数据
}
```

### 状态码
- 200: 成功
- 201: 创建成功
- 400: 请求错误
- 401: 未认证
- 403: 无权限
- 404: 资源不存在
- 500: 服务器错误

## 接口列表

### 认证 (auth.js)
```javascript
import { authAPI } from '@/api'

authAPI.login(credentials)        // POST /auth/login - 登录
authAPI.register(userData)        // POST /auth/register - 注册
authAPI.logout()                  // POST /auth/logout - 登出
authAPI.getCurrentUser()          // GET /auth/current-user - 获取当前用户
authAPI.changePassword(data)      // POST /auth/change-password - 修改密码
authAPI.forgetPassword(email)     // POST /auth/forget-password - 忘记密码
authAPI.resetPassword(data)       // POST /auth/reset-password - 重置密码
```

### 课程公共 API (course.js)
```javascript
import { courseAPI } from '@/api'

courseAPI.getCourseList(params)      // GET /courses - 课程列表
courseAPI.getCourseDetail(courseId)  // GET /courses/:id - 课程详情
courseAPI.getMyCourses(params)       // GET /courses/my-courses - 我的课程
courseAPI.getCourseResources(courseId) // GET /courses/:id/resources - 课程资源
```

### 学生功能 (student.js)
```javascript
import { 
  getStudentEnrollments, 
  enrollCourse, 
  getStudentCourse,
  getStudentHomework,
  submitHomework,
  getStudentExam,
  submitExam
} from '@/api'

// 选课管理
getStudentEnrollments(params)           // GET /student/enrollments - 我的选课
enrollCourse(courseId)                  // POST /student/enrollments - 选课
unenrollCourse(enrollmentId)           // DELETE /student/enrollments/:id - 退课

// 课程学习
getStudentCourse(courseId)             // GET /student/courses/:id - 课程学习页
getStudentLesson(courseId, lessonId)   // GET /student/courses/:id/lessons/:lessonId
completeLessonStudy(courseId, lessonId) // POST /student/courses/:id/lessons/:lessonId/complete
updateLearningProgress(courseId, data)  // POST /student/courses/:id/progress

// 作业
getStudentHomeworkList(params)         // GET /student/homework - 作业列表
getStudentHomework(courseId, homeworkId) // GET /student/courses/:id/homework/:homeworkId
submitHomework(courseId, homeworkId, data) // POST /student/courses/:id/homework/:homeworkId/submit

// 考试
getStudentExamList(params)             // GET /student/exams - 考试列表
getStudentExam(courseId, examId)       // GET /student/courses/:id/exams/:examId
startExam(courseId, examId)            // POST /student/courses/:id/exams/:examId/start
submitExam(courseId, examId, data)     // POST /student/courses/:id/exams/:examId/submit

// 课程社区
getStudentCourseThreads(courseId, params) // GET /student/courses/:id/threads
createStudentThread(courseId, data)    // POST /student/courses/:id/threads
```

### 教师功能 (teacher.js)
```javascript
import { 
  getTeacherCourses,
  createCourse,
  updateCourse,
  getCourseChapters,
  getTeacherHomework,
  createHomework,
  getTeacherExams,
  createExam
} from '@/api'

// 课程管理
getTeacherCourses(params)              // GET /teacher/courses - 我的课程
getTeacherCourse(courseId)             // GET /teacher/courses/:id
createCourse(data)                     // POST /teacher/courses
updateCourse(courseId, data)           // PUT /teacher/courses/:id
deleteCourse(courseId)                 // DELETE /teacher/courses/:id
publishCourse(courseId)                // POST /teacher/courses/:id/publish

// 章节管理
getCourseChapters(courseId)            // GET /teacher/courses/:id/chapters
createChapter(courseId, data)          // POST /teacher/courses/:id/chapters
updateChapter(courseId, chapterId, data) // PUT /teacher/courses/:id/chapters/:chapterId
deleteChapter(courseId, chapterId)     // DELETE /teacher/courses/:id/chapters/:chapterId

// 学生管理
getCourseStudents(courseId, params)    // GET /teacher/courses/:id/students
getStudentProgress(courseId, studentId) // GET /teacher/courses/:id/students/:studentId/progress

// 学期与班级
getCourseTerms(courseId)               // GET /teacher/courses/:id/terms
createTerm(courseId, data)             // POST /teacher/courses/:id/terms
getCourseClasses(courseId, params)     // GET /teacher/courses/:id/classes
createClass(courseId, data)            // POST /teacher/courses/:id/classes

// 作业管理
getTeacherHomework(params)             // GET /teacher/homework
createHomework(data)                   // POST /teacher/homework
publishHomework(homeworkId, data)      // POST /teacher/homework/:id/publish
getHomeworkSubmissions(homeworkId, params) // GET /teacher/homework/:id/submissions
gradeHomework(homeworkId, submissionId, data) // POST /teacher/homework/:id/submissions/:submissionId/grade

// 考试管理
getTeacherExams(params)                // GET /teacher/exams
createExam(data)                       // POST /teacher/exams
publishExam(examId, data)              // POST /teacher/exams/:id/publish
getExamSubmissions(examId, params)     // GET /teacher/exams/:id/submissions
gradeExam(examId, submissionId, data)  // POST /teacher/exams/:id/submissions/:submissionId/grade

// 课程社区管理
getTeacherCourseThreads(courseId, params) // GET /teacher/courses/:id/threads
createTeacherThread(courseId, data)    // POST /teacher/courses/:id/threads
pinThread(courseId, threadId)          // POST /teacher/courses/:id/threads/:threadId/pin
```

### 社区功能 (community.js)
```javascript
import { communityAPI } from '@/api'

communityAPI.getPublicQuestions(params)    // GET /community/questions - 问题列表
communityAPI.getQuestionDetail(questionId) // GET /community/questions/:id - 问题详情
communityAPI.postQuestion(data)            // POST /community/questions - 发布问题
communityAPI.updateQuestion(questionId, data) // PUT /community/questions/:id
communityAPI.deleteQuestion(questionId)    // DELETE /community/questions/:id
communityAPI.postAnswer(questionId, data)  // POST /community/questions/:id/answers
communityAPI.likeQuestion(questionId)      // POST /community/questions/:id/like
```

### 管理员功能 (admin.js)
```javascript
import { adminAPI } from '@/api'

adminAPI.getPendingCourses(params)         // GET /admin/courses/pending - 待审核课程
adminAPI.approveCourse(courseId, data)     // POST /admin/courses/:id/approve
adminAPI.rejectCourse(courseId, data)      // POST /admin/courses/:id/reject
adminAPI.getUserList(params)               // GET /admin/users - 用户列表
adminAPI.updateUser(userId, data)          // PUT /admin/users/:id
adminAPI.deleteUser(userId)                // DELETE /admin/users/:id
adminAPI.getAnalytics()                    // GET /admin/analytics - 数据统计
```

### 用户功能 (user.js)
```javascript
import { userAPI } from '@/api'

userAPI.getUserInfo(userId)           // GET /users/:id - 用户信息
userAPI.updateUserInfo(data)          // PUT /users/profile - 更新资料
userAPI.uploadAvatar(file)            // POST /users/avatar - 上传头像
userAPI.getLearningProgress()         // GET /users/learning-progress
userAPI.getGradeStats()               // GET /users/grade-stats - 成绩统计
```
