# 路由路径映射表

## 旧路由 → 新路由对照

### 公共路由（无需登录）
| 旧路径 | 新路径 | 说明 |
|--------|--------|------|
| `/` | `/` | 首页（保持不变）|
| `/course` | `/courses` | 课程中心 |
| `/course/:id` | `/courses/:id` | 课程详情 |
| `/login` | `/login` | 登录 |
| `/register` | `/register` | 注册 |

### 学生路由
| 旧路径 | 新路径 | 说明 |
|--------|--------|------|
| `/mycourse/student` | `/student/courses` | 我学的课程 |
| `/mycourse/student/:id` | `/student/courses/:id` | 课程学习 |
| `/mycourse/student/:courseId/lessons/:lessonId` | `/student/courses/:courseId/lessons/:lessonId` | 观看课时 |
| `/mycourse/student/:courseId/homework/:id` | `/student/courses/:courseId/homework/:id` | 作业详情 |
| `/mycourse/student/:courseId/exams/:id` | `/student/courses/:courseId/exams/:id` | 考试确认 |
| `/mycourse/student/:courseId/exams/:id/answer` | `/student/courses/:courseId/exams/:id/answer` | 考试答题 |
| `/homework` | `/student/homework` | 我的作业 |
| `/exams` | `/student/exams` | 我的考试 |
| `/user/profile` | `/student/profile` | 个人信息 |
| `/user/certificates` | `/student/certificates` | 我的证书 |

### 教师路由
| 旧路径 | 新路径 | 说明 |
|--------|--------|------|
| `/mycourse/teacher` | `/teacher/courses` | 我教的课程 |
| `/mycourse/teacher/create` | `/teacher/courses/create` | 创建课程 |
| `/mycourse/teacher/:id` | `/teacher/courses/:id` | 课程管理 |
| `/mycourse/teacher/:id/edit` | `/teacher/courses/:id/edit` | 编辑课程 |
| `/mycourse/teacher/:id/chapters` | `/teacher/courses/:id/chapters` | 章节编辑 |
| `/mycourse/teacher/:id/lessons/:lessonId` | `/teacher/courses/:id/lessons/:lessonId` | 课时预览 |
| `/teacher/homework/create` | `/teacher/homework/create` | 创建作业 |
| `/teacher/homework/:id` | `/teacher/homework/:id` | 作业详情 |
| `/teacher/homework/:id/grading` | `/teacher/homework/:id/grading` | 批阅列表 |
| `/teacher/exams/create` | `/teacher/exams/create` | 创建试卷 |
| `/teacher/exams/:id` | `/teacher/exams/:id` | 试卷详情 |
| `/teacher/term-management` | `/teacher/terms` | 学期管理 |
| `/teacher/class-management` | `/teacher/classes` | 班级管理 |

### 共享路由（需登录）
| 旧路径 | 新路径 | 说明 |
|--------|--------|------|
| `/community` | `/community` | 社区广场 |
| `/community/plaza` | `/community` | 社区广场 |
| `/community/posts/:id` | `/community/posts/:id` | 话题详情 |
| `/community/posts/create` | `/community/posts/create` | 发布话题 |
| `/messages` | `/messages` | 消息中心 |

### 管理员路由
| 旧路径 | 新路径 | 说明 |
|--------|--------|------|
| `/admin` | `/admin/dashboard` | 管理后台首页 |
| `/admin/users` | `/admin/users` | 用户管理 |
| `/admin/courses` | `/admin/courses` | 课程审核 |

## 路由层次结构

```
/
├── 认证路由（无布局）
│   ├── /login
│   ├── /register
│   └── /forgot-password
│
├── 主应用（MainLayout布局 - 有导航栏）
│   ├── 公共内容
│   │   ├── / (首页)
│   │   ├── /courses (课程中心)
│   │   └── /courses/:id (课程详情)
│   │
│   ├── 学生路由 (/student/*)
│   │   ├── /student/courses (我学的课程)
│   │   ├── /student/courses/:id (课程学习)
│   │   ├── /student/homework (我的作业)
│   │   ├── /student/exams (我的考试)
│   │   └── /student/profile (个人中心)
│   │
│   ├── 教师路由 (/teacher/*)
│   │   ├── /teacher/courses (我教的课程)
│   │   ├── /teacher/homework (作业库)
│   │   ├── /teacher/exams (试卷库)
│   │   └── /teacher/classes (班级管理)
│   │
│   └── 共享路由
│       ├── /community (社区广场)
│       └── /messages (消息中心)
│
└── 管理后台（AdminLayout布局）
    └── /admin/* (管理员功能)
```

## 导航链接更新

### MainLayout 导航栏
- **首页**: `/` ✅
- **课程中心**: `/courses` ✅
- **我的课程**: 根据角色跳转
  - 学生: `/student/courses`
  - 教师: `/teacher/courses`
- **社区**: `/community` ✅
- **消息**: `/messages` ✅
- **个人中心**: 根据角色跳转
  - 学生: `/student/profile`
  - 教师: `/teacher/profile`
- **我的证书**: `/student/certificates` ✅

## 已修复的文件列表

### 学生端
- ✅ `views/student/course/List.vue`
- ✅ `views/student/course/Detail.vue`
- ✅ `views/student/course/LessonPlayer.vue`
- ✅ `views/student/homework/Detail.vue`
- ✅ `views/student/exam/List.vue`
- ✅ `views/student/exam/Confirm.vue`
- ✅ `views/student/exam/Answer.vue`

### 教师端
- ✅ `views/teacher/course/List.vue`
- ✅ `views/teacher/course/Create.vue`
- ✅ `views/teacher/course/Detail.vue`
- ✅ `views/teacher/course/Edit.vue`
- ✅ `views/teacher/course/LessonPlayer.vue`
- ✅ `views/teacher/course/ChapterEdit.vue`
- ✅ `views/teacher/course/Preview.vue`
- ✅ `views/teacher/homework/Create.vue`
- ✅ `views/teacher/homework/Publish.vue`
- ✅ `views/teacher/exam/Publish.vue`
- ✅ `views/teacher/community/PostCreate.vue`
- ✅ `views/teacher/community/PostDetail.vue`

### 公共页面
- ✅ `views/public/home/Index.vue`
- ✅ `layouts/MainLayout.vue`

### 路由配置
- ✅ `router/index.js`
- ✅ `router/modules/public.js`
- ✅ `router/modules/student.js`
- ✅ `router/modules/teacher.js`
- ✅ `router/modules/admin.js`
- ✅ `router/modules/shared.js`

## 注意事项

1. **开发模式自动登录**: 在 `router/index.js` 中配置了开发模式自动设置 token 和角色，方便测试
2. **权限检查**: 路由守卫会根据路径前缀检查权限（`/student/*`, `/teacher/*`, `/admin/*`）
3. **角色跳转**: 某些导航链接（如"我的课程"）会根据当前登录角色自动跳转到对应路由
4. **404处理**: 未匹配的路由会显示 404 页面

## 测试建议

访问以下路径测试路由是否正常：
- http://localhost:8080/ (首页)
- http://localhost:8080/courses (课程中心)
- http://localhost:8080/student/courses (学生课程)
- http://localhost:8080/teacher/courses (教师课程)
- http://localhost:8080/community (社区广场)
- http://localhost:8080/admin/dashboard (管理后台)
