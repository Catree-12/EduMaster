# 前端路由完整列表

## 路由总览

**总计**: 67 个路由
- 认证路由: 3个（无需登录）
- 公共路由: 4个（无需登录）
- 学生路由: 12个
- 教师路由: 29个
- 管理员路由: 8个
- 用户路由: 2个
- 共享路由: 5个
- 其他: 404页面

---

## 1. 认证路由（无需登录）

| 路由路径 | 路由名称 | 组件 | 说明 |
|---------|---------|------|------|
| `/login` | Login | `@/views/public/auth/Login.vue` | 用户登录 |
| `/register` | Register | `@/views/public/auth/Register.vue` | 用户注册 |
| `/forgot-password` | ForgotPassword | `@/views/public/auth/ForgotPassword.vue` | 忘记密码 |

---

## 2. 公共内容路由（无需登录）

| 路由路径 | 路由名称 | 组件 | 说明 |
|---------|---------|------|------|
| `/` | Home | `@/views/public/home/Index.vue` | 首页 |
| `/courses` | CourseCenter | `@/views/public/course/Center.vue` | 课程中心 |
| `/courses/:id` | CourseDetail | `@/views/public/course/Detail.vue` | 课程详情 |
| `/enrollment` | CourseEnrollment | `@/views/public/course/ClassEnrollment.vue` | 课程报名（需登录） |

---

## 3. 学生路由（需要学生角色）

### 3.1 课程学习（3个）

| 路由路径 | 路由名称 | 组件 | 说明 |
|---------|---------|------|------|
| `/student/courses` | StudentCourseList | `@/views/student/course/List.vue` | 我学的课程 |
| `/student/courses/:courseId` | StudentCourseDetail | `@/views/student/course/Detail.vue` | 课程学习详情 |
| `/student/courses/:courseId/lessons/:lessonId` | StudentLessonPlayer | `@/views/student/course/LessonPlayer.vue` | 观看课时 |

### 3.2 作业（2个）

| 路由路径 | 路由名称 | 组件 | 说明 |
|---------|---------|------|------|
| `/student/homework` | StudentHomeworkList | `@/views/student/homework/List.vue` | 我的作业列表 |
| `/student/courses/:courseId/homework/:homeworkId` | StudentHomeworkDetail | `@/views/student/homework/Detail.vue` | 作业详情 |

### 3.3 考试（3个）

| 路由路径 | 路由名称 | 组件 | 说明 |
|---------|---------|------|------|
| `/student/exams` | StudentExamList | `@/views/student/exam/List.vue` | 我的考试列表 |
| `/student/courses/:courseId/exams/:examId` | StudentExamConfirm | `@/views/student/exam/Confirm.vue` | 考试确认 |
| `/student/courses/:courseId/exams/:examId/answer` | StudentExamAnswer | `@/views/student/exam/Answer.vue` | 考试答题 |

### 3.4 课程社区（3个）

| 路由路径 | 路由名称 | 组件 | 说明 |
|---------|---------|------|------|
| `/student/courses/:courseId/community/posts/create` | StudentCommunityPostCreate | `@/views/student/community/PostCreate.vue` | 发布话题 |
| `/student/courses/:courseId/community/posts/:postId` | StudentCommunityPostDetail | `@/views/student/community/PostDetail.vue` | 话题详情 |
| `/student/courses/:courseId/community/posts/:postId/edit` | StudentCommunityPostEdit | `@/views/student/community/PostEdit.vue` | 编辑话题 |

**学生路由小计**: 12个

---

## 4. 教师路由（需要教师角色）

### 4.1 课程管理（8个）

| 路由路径 | 路由名称 | 组件 | 说明 |
|---------|---------|------|------|
| `/teacher/courses` | TeacherCourseList | `@/views/teacher/course/List.vue` | 我教的课程 |
| `/teacher/courses/create` | TeacherCourseCreate | `@/views/teacher/course/Create.vue` | 创建课程 |
| `/teacher/courses/:courseId` | TeacherCourseDetail | `@/views/teacher/course/Detail.vue` | 课程管理 |
| `/teacher/courses/:courseId/edit` | TeacherCourseEdit | `@/views/teacher/course/Edit.vue` | 编辑课程 |
| `/teacher/courses/:courseId/chapters` | TeacherCourseChapterEdit | `@/views/teacher/course/ChapterEdit.vue` | 章节编辑 |
| `/teacher/courses/:courseId/preview` | TeacherCoursePreview | `@/views/teacher/course/Preview.vue` | 预览课程 |
| `/teacher/courses/:courseId/lessons/:lessonId` | TeacherLessonPlayer | `@/views/teacher/course/LessonPlayer.vue` | 课时预览 |
| `/teacher/courses/:courseId/review` | CourseReview | `@/views/admin/CourseReview.vue` | 课程评价管理 |

### 4.2 作业管理（8个）

| 路由路径 | 路由名称 | 组件 | 说明 |
|---------|---------|------|------|
| `/teacher/homework` | TeacherHomeworkLibrary | `@/views/teacher/homework/Library.vue` | 作业库 |
| `/teacher/homework/create` | TeacherHomeworkCreate | `@/views/teacher/homework/Create.vue` | 创建作业 |
| `/teacher/homework/:id` | TeacherHomeworkDetail | `@/views/teacher/homework/Detail.vue` | 作业详情 |
| `/teacher/homework/:id/edit` | TeacherHomeworkEdit | `@/views/teacher/homework/Edit.vue` | 编辑作业 |
| `/teacher/homework/:id/settings` | TeacherHomeworkSettings | `@/views/teacher/homework/Settings.vue` | 作业设置 |
| `/teacher/homework/:id/publish` | TeacherHomeworkPublish | `@/views/teacher/homework/Publish.vue` | 发布作业 |
| `/teacher/homework/:id/grading` | TeacherHomeworkGradingList | `@/views/teacher/homework/GradingList.vue` | 批阅列表 |
| `/teacher/homework/:id/grading/:studentId` | TeacherHomeworkGradingDetail | `@/views/teacher/homework/GradingDetail.vue` | 批阅详情 |

### 4.3 考试管理（9个）

| 路由路径 | 路由名称 | 组件 | 说明 |
|---------|---------|------|------|
| `/teacher/exams` | TeacherExamLibrary | `@/views/teacher/exam/Library.vue` | 试卷库 |
| `/teacher/exams/create` | TeacherExamCreateSelection | `@/views/teacher/exam/CreateSelection.vue` | 选择组卷方式 |
| `/teacher/exams/create/manual` | TeacherExamCreateManual | `@/views/teacher/exam/CreateManual.vue` | 手动组卷 |
| `/teacher/exams/create/intelligent` | TeacherExamCreateIntelligent | `@/views/teacher/exam/CreateIntelligent.vue` | 智能组卷 |
| `/teacher/exams/:id` | TeacherExamDetail | `@/views/teacher/exam/Detail.vue` | 试卷详情 |
| `/teacher/exams/:id/settings` | TeacherExamSettings | `@/views/teacher/exam/Settings.vue` | 考试设置 |
| `/teacher/exams/:id/publish` | TeacherExamPublish | `@/views/teacher/exam/Publish.vue` | 发布试卷 |
| `/teacher/exams/:id/grading` | TeacherExamGradingList | `@/views/teacher/exam/GradingList.vue` | 批阅列表 |
| `/teacher/exams/:id/grading/:studentId` | TeacherExamGradingDetail | `@/views/teacher/exam/GradingDetail.vue` | 批阅详情 |

### 4.4 课程社区管理（3个）

| 路由路径 | 路由名称 | 组件 | 说明 |
|---------|---------|------|------|
| `/teacher/courses/:courseId/community/posts/create` | TeacherCommunityPostCreate | `@/views/teacher/community/PostCreate.vue` | 发布公告 |
| `/teacher/courses/:courseId/community/posts/:postId` | TeacherCommunityPostDetail | `@/views/teacher/community/PostDetail.vue` | 话题详情 |
| `/teacher/courses/:courseId/community/posts/:postId/edit` | TeacherCommunityPostEdit | `@/views/teacher/community/PostEdit.vue` | 编辑话题 |

### 4.5 班级管理（2个）

| 路由路径 | 路由名称 | 组件 | 说明 |
|---------|---------|------|------|
| `/teacher/classes` | TeacherClassList | `@/views/teacher/class/List.vue` | 班级管理 |
| `/teacher/terms` | TeacherTermManage | `@/views/teacher/class/TermManage.vue` | 学期管理 |

**教师路由小计**: 29个

---

## 5. 管理员路由（需要管理员角色）

| 路由路径 | 路由名称 | 组件 | 说明 |
|---------|---------|------|------|
| `/admin/dashboard` | AdminDashboard | `@/views/admin/AdminDashboard.vue` | 仪表盘 |
| `/admin/users` | AdminUserManagement | `@/views/admin/UserManagement.vue` | 用户管理 |
| `/admin/courses/audit` | AdminCourseAudit | `@/views/admin/CourseAudit.vue` | 课程审核 |
| `/admin/content/review` | AdminContentReview | `@/views/admin/ContentReview.vue` | 内容审查 |
| `/admin/certificates` | AdminCertificateManagement | `@/views/admin/CertificateManagement.vue` | 证书管理 |
| `/admin/analytics` | AdminAnalytics | `@/views/admin/AdminAnalytics.vue` | 数据分析 |
| `/admin/settings` | AdminSystemSettings | `@/views/admin/SystemSettings.vue` | 系统设置 |
| `/admin/courses/:courseId/review` | CourseReview | `@/views/admin/CourseReview.vue` | 课程评价管理 |

**管理员路由小计**: 8个

---

## 6. 用户路由（所有登录用户）

| 路由路径 | 路由名称 | 组件 | 说明 |
|---------|---------|------|------|
| `/user/profile` | UserProfile | `@/views/user/Profile.vue` | 个人中心 |
| `/user/certificates` | UserCertificates | `@/views/user/Certificates.vue` | 我的证书 |

**用户路由小计**: 2个

---

## 7. 共享路由（需要登录，不限角色）

### 7.1 社区广场（4个）

| 路由路径 | 路由名称 | 组件 | 说明 |
|---------|---------|------|------|
| `/community` | CommunityPlaza | `@/views/shared/community/Plaza.vue` | 社区广场 |
| `/community/posts/create` | CommunityPostCreate | `@/views/shared/community/PostCreate.vue` | 发布话题 |
| `/community/posts/:id` | CommunityPostDetail | `@/views/shared/community/PostDetail.vue` | 话题详情 |
| `/community/posts/:id/edit` | CommunityPostEdit | `@/views/shared/community/PostEdit.vue` | 编辑话题 |

### 7.2 消息中心（1个）

| 路由路径 | 路由名称 | 组件 | 说明 |
|---------|---------|------|------|
| `/messages` | MessageCenter | `@/views/shared/message/Center.vue` | 消息中心 |

**共享路由小计**: 5个

---

## 8. 其他路由

| 路由路径 | 路由名称 | 组件 | 说明 |
|---------|---------|------|------|
| `*` | NotFound | `@/views/shared/NotFound.vue` | 404页面 |

---

## 路由参数说明

### 常用路由参数

| 参数名 | 说明 | 示例 |
|-------|------|------|
| `:id` | 通用资源ID | `/community/posts/123` |
| `:courseId` | 课程ID | `/student/courses/456` |
| `:lessonId` | 课时ID | `/student/courses/456/lessons/789` |
| `:examId` | 考试ID | `/student/courses/456/exams/101` |
| `:homeworkId` | 作业ID | `/student/courses/456/homework/202` |
| `:postId` | 帖子ID | `/student/courses/456/community/posts/303` |
| `:studentId` | 学生ID | `/teacher/homework/404/grading/505` |

---

## 路由元信息（meta）

所有路由都包含以下 meta 信息：

```javascript
{
  requiresAuth: true/false,  // 是否需要登录
  roles: ['student', 'teacher', 'admin'],  // 允许的角色（可选）
  title: '页面标题'  // 页面标题
}
```

### 权限级别

1. **公开路由** (`requiresAuth: false`): 无需登录即可访问
   - 认证页面：`/login`, `/register`, `/forgot-password`
   - 公共内容：`/`, `/courses`, `/courses/:id`

2. **需登录路由** (`requiresAuth: true`): 需要登录，部分需要特定角色
   - 角色限定：`/student/*`, `/teacher/*`, `/admin/*`
   - 所有角色：`/user/*`, `/community/*`, `/messages`

---

## 路由守卫逻辑

### 权限检查流程

1. **检查是否需要登录**
   - `requiresAuth: false` → 直接放行
   - `requiresAuth: true` → 检查 token

2. **未登录用户访问需登录路由**
   - 重定向到 `/login`

3. **已登录用户访问登录/注册页**
   - 根据角色重定向：
     - admin → `/admin/dashboard`
     - teacher → `/teacher/courses`
     - student → `/student/courses`

4. **角色权限检查**（基于路径前缀）
   - `/student/*` → 只允许 student 角色
   - `/teacher/*` → 只允许 teacher 角色
   - `/admin/*` → 只允许 admin 角色

5. **无权限访问**
   - 显示错误提示
   - 重定向到 `/`

---

## 开发环境自动登录

开发模式下自动设置测试用户：

```javascript
localStorage.setItem('token', 'dev-test-token')
localStorage.setItem('userRole', 'student')
localStorage.setItem('userId', '1')
localStorage.setItem('userName', '测试用户')
```

**注意**: 生产环境下此功能自动禁用

---

## 路由模块文件

| 文件路径 | 说明 |
|---------|------|
| `src/router/index.js` | 路由主文件，整合所有模块 |
| `src/router/modules/public.js` | 公共路由（认证 + 公共内容） |
| `src/router/modules/student.js` | 学生路由 |
| `src/router/modules/teacher.js` | 教师路由 |
| `src/router/modules/admin.js` | 管理员路由 |
| `src/router/modules/user.js` | 用户路由 |
| `src/router/modules/shared.js` | 共享路由 |

---

## 布局组件

| 布局组件 | 使用路由 | 说明 |
|---------|---------|------|
| 无布局 | `/login`, `/register`, `/forgot-password` | 认证页面全屏显示 |
| `MainLayout` | 学生、教师、用户、共享路由 | 包含顶部导航和侧边栏 |
| `AdminLayout` | 管理员路由 | 管理员专用布局 |

---

## 路由命名规范

### 命名格式

- **角色前缀** + **功能模块** + **操作**
- 示例：
  - `StudentCourseList` - 学生-课程-列表
  - `TeacherHomeworkCreate` - 教师-作业-创建
  - `AdminUserManagement` - 管理员-用户-管理

### 特殊命名

- **Create**: 创建/新建
- **Edit**: 编辑
- **Detail**: 详情
- **List**: 列表
- **Library**: 资源库
- **Grading**: 批阅
- **Settings**: 设置
- **Publish**: 发布
- **Preview**: 预览
- **Confirm**: 确认
- **Answer**: 答题

---

## 统计数据

### 按角色分类

| 角色 | 路由数量 | 主要功能 |
|-----|---------|---------|
| 学生 | 12个 | 课程学习、作业、考试、社区 |
| 教师 | 29个 | 课程管理、作业管理、考试管理、班级管理 |
| 管理员 | 8个 | 用户管理、内容审核、系统设置 |
| 通用 | 7个 | 个人中心、证书、社区、消息 |
| 公共 | 7个 | 首页、课程中心、认证页面 |

### 按功能分类

| 功能模块 | 路由数量 |
|---------|---------|
| 认证相关 | 3个 |
| 课程学习/管理 | 11个 |
| 作业管理 | 10个 |
| 考试管理 | 12个 |
| 社区功能 | 10个 |
| 用户管理 | 3个 |
| 管理员功能 | 8个 |
| 其他 | 10个 |

**总计**: 67个路由

---

## 后端对接要点

### 1. 需要对接的主要 API 端点

根据前端路由，后端需要提供以下模块的 API：

#### 认证模块（6个端点）
- `POST /api/auth/login/` - 登录
- `POST /api/auth/register/` - 注册
- `POST /api/auth/logout/` - 登出
- `POST /api/auth/forget-password/` - 忘记密码
- `POST /api/auth/change-password/` - 修改密码
- `GET /api/auth/profile/` - 获取用户信息

#### 课程模块
- 课程列表、详情、创建、编辑、删除
- 章节管理
- 课时管理
- 学生课程列表（已选课程）

#### 作业模块
- 作业库管理（CRUD）
- 作业发布
- 学生作业提交
- 作业批阅

#### 考试模块
- 试卷库管理（CRUD）
- 手动/智能组卷
- 考试发布
- 学生答题
- 考试批阅

#### 社区模块
- 帖子 CRUD
- 评论功能
- 社区广场
- 课程社区

#### 用户模块
- 个人信息更新
- 证书列表
- 消息中心

#### 管理员模块
- 用户管理
- 内容审核
- 数据统计
- 系统设置

### 2. RESTful API 建议路径

所有 API 路径建议使用 `/api/` 前缀，例如：

```
/api/courses/                    # 课程列表
/api/courses/:id/                # 课程详情
/api/courses/:id/chapters/       # 课程章节
/api/courses/:id/lessons/:lid/   # 课程课时
/api/homework/                   # 作业列表
/api/exams/                      # 考试列表
/api/community/posts/            # 社区帖子
/api/users/:id/                  # 用户信息
...
```

### 3. 权限控制

后端需要根据用户角色（student/teacher/admin）进行权限验证：
- JWT Token 验证
- 角色权限检查
- 资源所有权验证（例如：学生只能访问自己的作业）

### 4. 响应格式

建议统一的响应格式：

```javascript
// 成功响应
{
  code: 200,
  data: { ... },
  message: "操作成功"
}

// 错误响应
{
  code: 400,
  error: "错误信息",
  message: "操作失败"
}
```
