# 前端路由结构规范

## 目录结构说明

```
src/
├── api/              # API接口层
├── views/            # 页面组件(路由组件)
│   ├── auth/         # 认证相关页面
│   ├── home/         # 首页
│   ├── course/       # 课程相关
│   ├── user/         # 用户中心
│   ├── community/    # 社区
│   ├── exam/         # 考试
│   ├── homework/     # 作业
│   ├── teacher/      # 教师管理
│   ├── admin/        # 管理员后台
│   ├── certificate/  # 证书
│   └── message/      # 消息
├── components/       # 公共组件(非路由组件)
├── layouts/          # 布局组件
├── router/           # 路由配置
└── store/            # Vuex状态管理
```

## 路由命名规范

### 1. 公开路由 (无需认证)
- `/login` - 登录
- `/register` - 注册
- `/forgot-password` - 忘记密码
- `/certificate/share/:shareCode` - 证书分享页

### 2. 通用路由 (需要认证)
- `/` - 首页
- `/courses` - 课程中心
- `/courses/:id` - 课程详情
- `/user/profile` - 个人资料
- `/user/certificates` - 我的证书
- `/messages` - 消息中心
- `/community` - 社区广场
- `/community/posts/:id` - 帖子详情

### 3. 学生路由 (以 `/student` 开头)
```
/student/enrollments                           # 我的学习
/student/courses/:courseId                     # 课程学习页
/student/courses/:courseId/lessons/:lessonId   # 课时播放
/student/courses/:courseId/homework/:hwId      # 作业详情
/student/courses/:courseId/exams/:examId       # 考试确认页
/student/courses/:courseId/exams/:examId/answer # 考试答题
/student/courses/:courseId/community           # 课程社区
/student/courses/:courseId/threads/:threadId   # 帖子详情
```

### 4. 教师路由 (以 `/teacher` 开头)
```
/teacher/courses                               # 我的课程列表
/teacher/courses/create                        # 创建课程
/teacher/courses/:id                           # 课程管理主页
/teacher/courses/:id/edit                      # 编辑课程信息
/teacher/courses/:id/chapters                  # 章节管理
/teacher/courses/:id/preview                   # 课程预览
/teacher/courses/:id/terms                     # 学期管理
/teacher/courses/:id/classes                   # 班级管理
/teacher/courses/:id/community                 # 课程社区管理
/teacher/courses/:id/threads/:threadId         # 帖子详情

# 作业管理
/teacher/homework                              # 作业库
/teacher/homework/create                       # 创建作业
/teacher/homework/:id                          # 作业详情
/teacher/homework/:id/edit                     # 编辑作业
/teacher/homework/:id/publish                  # 发布作业
/teacher/homework/:id/grading                  # 批改作业

# 考试管理
/teacher/exams                                 # 考试库
/teacher/exams/create                          # 创建考试
/teacher/exams/:id                             # 考试详情
/teacher/exams/:id/edit                        # 编辑考试
/teacher/exams/:id/publish                     # 发布考试
/teacher/exams/:id/grading                     # 批改考试
```

### 5. 管理员路由 (以 `/admin` 开头)
```
/admin/dashboard                               # 管理仪表盘
/admin/users                                   # 用户管理
/admin/courses/audit                           # 课程审核
/admin/content/review                          # 内容审查
/admin/certificates                            # 证书管理
/admin/analytics                               # 数据分析
/admin/settings                                # 系统设置
```

## API 接口命名规范

### RESTful 风格
```javascript
// 认证
POST   /api/auth/login
POST   /api/auth/register
POST   /api/auth/logout
POST   /api/auth/refresh
GET    /api/auth/profile

// 课程
GET    /api/courses                           # 课程列表
GET    /api/courses/:id                       # 课程详情
POST   /api/courses                           # 创建课程
PUT    /api/courses/:id                       # 更新课程
DELETE /api/courses/:id                       # 删除课程

// 课程章节
GET    /api/courses/:courseId/chapters        # 章节列表
POST   /api/courses/:courseId/chapters        # 创建章节
PUT    /api/courses/:courseId/chapters/:id    # 更新章节
DELETE /api/courses/:courseId/chapters/:id    # 删除章节

// 学生选课
GET    /api/student/enrollments               # 我的选课
POST   /api/student/enrollments               # 选课
GET    /api/student/courses/:id               # 学习详情
POST   /api/student/courses/:id/progress      # 更新进度

// 作业
GET    /api/teacher/homework                  # 教师作业库
POST   /api/teacher/homework                  # 创建作业
GET    /api/student/homework                  # 学生作业列表
POST   /api/student/homework/:id/submit       # 提交作业

// 考试
GET    /api/teacher/exams                     # 教师考试库
POST   /api/teacher/exams                     # 创建考试
GET    /api/student/exams/:id                 # 考试详情
POST   /api/student/exams/:id/submit          # 提交考试

// 社区
GET    /api/community/posts                   # 帖子列表
POST   /api/community/posts                   # 发帖
GET    /api/community/posts/:id               # 帖子详情
POST   /api/community/posts/:id/comments      # 评论
POST   /api/community/posts/:id/like          # 点赞

// 管理员
GET    /api/admin/users                       # 用户列表
PUT    /api/admin/users/:id                   # 更新用户
GET    /api/admin/courses/pending             # 待审核课程
POST   /api/admin/courses/:id/approve         # 审核通过
POST   /api/admin/courses/:id/reject          # 审核拒绝
```

## 文件命名规范

### Vue 组件
- 使用 PascalCase: `CourseDetail.vue`, `ExamAnswer.vue`
- 页面组件放在 `views/` 目录
- 公共组件放在 `components/` 目录

### API 文件
- 使用 camelCase: `auth.js`, `course.js`, `user.js`
- 按业务模块划分文件

### 路由命名
- name 使用 PascalCase: `CourseDetail`, `StudentExamAnswer`
- path 使用 kebab-case: `/course-detail`, `/exam-answer`

## 权限控制

### meta 字段
```javascript
{
  requiresAuth: true,        // 需要登录
  requiresRole: 'teacher',   // 需要特定角色
  requiresRole: ['teacher', 'admin']  // 需要多个角色之一
}
```

### 角色类型
- `student` - 学生
- `teacher` - 教师
- `admin` - 管理员

## 迁移说明

### 已完成
1. ✅ 创建路由结构规范文档
2. ✅ 合并 `pages/exam/ExamDetail.vue` 到 `views/exam/`
3. ✅ 统一文件命名规范

### 待完成
1. ⏳ 清理 `pages/` 目录中的重复文件
2. ⏳ 更新路由配置文件
3. ⏳ 统一 API 调用路径
4. ⏳ 更新所有组件中的路由跳转
