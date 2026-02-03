# 项目目录结构优化说明

## 📁 新的目录结构

### 1. views/ 视图层目录

```
views/
├── public/                         # 公共页面（无需登录）
│   ├── auth/                       # 认证相关
│   │   ├── Login.vue
│   │   ├── Register.vue
│   │   └── ForgotPassword.vue
│   ├── home/                       # 首页
│   │   └── Index.vue
│   ├── course/                     # 课程中心
│   │   ├── Center.vue              # 课程列表
│   │   ├── Detail.vue              # 课程详情
│   │   └── ClassEnrollment.vue     # 选课报名
│   └── certificate/                # 证书分享
│       └── Share.vue
│
├── student/                        # 学生功能（学生角色路由）
│   ├── course/                     # 课程学习
│   │   ├── List.vue                # 我的课程
│   │   ├── Detail.vue              # 课程详情
│   │   └── LessonPlayer.vue        # 课程播放
│   ├── homework/                   # 作业
│   │   ├── List.vue
│   │   └── Detail.vue
│   ├── exam/                       # 考试
│   │   ├── List.vue
│   │   ├── Confirm.vue
│   │   └── Answer.vue
│   └── community/                  # 课程社区（学生视角）
│       ├── PostCreate.vue
│       ├── PostDetail.vue
│       └── PostEdit.vue
│
├── teacher/                        # 教师功能（教师角色路由）
│   ├── course/                     # 课程管理
│   │   ├── List.vue                # 我的课程
│   │   ├── Create.vue              # 创建课程
│   │   ├── Edit.vue                # 编辑课程
│   │   ├── Detail.vue              # 课程详情
│   │   ├── Preview.vue             # 课程预览
│   │   ├── ChapterEdit.vue         # 章节编辑
│   │   └── LessonPlayer.vue        # 课程播放
│   ├── homework/                   # 作业管理
│   │   ├── Create.vue
│   │   ├── Publish.vue
│   │   ├── GradingList.vue
│   │   └── GradingDetail.vue
│   ├── exam/                       # 考试管理
│   │   ├── Create.vue
│   │   ├── CreateManual.vue
│   │   ├── CreateIntelligent.vue
│   │   ├── Publish.vue
│   │   └── ...
│   ├── class/                      # 班级管理
│   │   ├── List.vue
│   │   └── TermManage.vue
│   └── community/                  # 课程社区（教师视角）
│       ├── PostCreate.vue
│       ├── PostDetail.vue
│       └── PostEdit.vue
│
├── user/                           # ✨ 用户个人功能（不区分角色）
│   ├── Profile.vue                 # 个人中心
│   ├── Certificates.vue            # 我的证书
│   └── components/                 # 用户相关组件
│       ├── CertificateDetail.vue
│       └── CertificateShare.vue
│
├── admin/                          # 管理员功能
│   ├── AdminDashboard.vue
│   ├── UserManagement.vue
│   ├── CourseAudit.vue
│   └── ...
│
└── shared/                         # 共享功能（任何登录用户）
    ├── NotFound.vue                # 404页面
    ├── community/                  # 公共社区
    │   ├── Plaza.vue               # 社区广场
    │   ├── PostCreate.vue
    │   ├── PostDetail.vue
    │   └── PostEdit.vue
    └── message/                    # 消息中心
        └── Center.vue
```

### 2. components/ 公共组件目录

```
components/
├── layout/                         # 布局组件
│   ├── MainHeader.vue              # 头部导航（待创建）
│   ├── MainSidebar.vue             # 侧边栏（待创建）
│   └── MainFooter.vue              # 底部（待创建）
│
├── course/                         # 课程相关组件
│   ├── CourseCard.vue              # ✅ 课程卡片
│   ├── ChapterList.vue             # 章节列表（待创建）
│   └── LessonItem.vue              # 课时项（待创建）
│
├── common/                         # 通用组件
│   ├── SearchBar.vue               # ✅ 搜索栏
│   ├── Pagination.vue              # 分页（待创建）
│   └── EmptyState.vue              # ✅ 空状态
│
└── form/                           # 表单组件
    └── RichTextEditor.vue          # 富文本编辑器（待创建）
```

### 3. router/modules/ 路由模块

```
router/modules/
├── public.js                       # 公共路由（首页、课程中心、认证）
├── student.js                      # 学生路由（课程学习、作业、考试）
├── teacher.js                      # 教师路由（课程管理、作业批改、考试管理）
├── user.js                         # ✨ 用户路由（个人中心、证书）
├── shared.js                       # 共享路由（社区、消息）
└── admin.js                        # 管理员路由
```

## 🎯 核心优化点

### 1. 角色与功能分离

**之前的问题：**
- `views/student/user/` 混淆了角色（student）与功能（user）
- 个人信息需要判断角色才能访问正确页面

**优化后：**
```javascript
// MainLayout.vue - 简化后的导航逻辑
goToProfile() {
  // 不再需要判断角色，统一跳转
  this.$router.push('/user/profile')
},
goToCertificates() {
  this.$router.push('/user/certificates')
}
```

### 2. 路由结构更清晰

**路由命名规则：**
- `/student/*` - 学生学习功能
- `/teacher/*` - 教师教学功能
- `/user/*` - 个人信息管理（不区分角色）
- `/community/*` - 公共社区
- `/admin/*` - 管理员功能

**示例：**
```javascript
// 用户路由 - 所有角色共用
{
  path: '/user/profile',
  name: 'UserProfile',
  component: () => import('@/views/user/Profile.vue'),
  meta: { requiresAuth: true, title: '个人中心' }
}
```

### 3. 组件分类更合理

**公共组件按功能分类：**
- `components/layout/` - 布局相关
- `components/course/` - 课程相关
- `components/common/` - 通用组件
- `components/form/` - 表单组件

**用户特定组件：**
- `views/user/components/` - 证书等用户专属组件

## 📊 路由映射对照表

| 功能 | 旧路径 | 新路径 |
|------|--------|--------|
| 个人中心（学生） | `/student/profile` | `/user/profile` |
| 个人中心（教师） | `/teacher/profile` | `/user/profile` |
| 我的证书 | `/student/certificates` | `/user/certificates` |

## 🔧 迁移步骤

### 已完成 ✅

1. ✅ 创建 `views/user/` 目录
2. ✅ 移动 `Profile.vue` 和 `Certificates.vue` 到 `views/user/`
3. ✅ 移动证书组件到 `views/user/components/`
4. ✅ 创建 `router/modules/user.js`
5. ✅ 更新 `router/index.js` 引入 user 路由
6. ✅ 简化 `MainLayout.vue` 导航逻辑
7. ✅ 创建 `components/{layout,course,common,form}` 目录结构
8. ✅ 创建示例公共组件（CourseCard, SearchBar, EmptyState）
9. ✅ 删除旧的 `views/student/user/` 目录
10. ✅ 从 `student.js` 中移除个人中心路由

### 待完成 📝

1. 创建更多公共组件（ChapterList, LessonItem, Pagination 等）
2. 提取现有重复组件到 components 目录
3. 更新所有引用旧路径的页面链接

## 💡 使用指南

### 如何判断页面应该放在哪里？

**判断流程：**
```
1. 是否需要登录？
   └─ 否 → public/
   └─ 是 → 继续判断

2. 是否区分角色？
   └─ 否 → user/ 或 shared/
   └─ 是 → 继续判断

3. 是什么角色？
   └─ 学生 → student/
   └─ 教师 → teacher/
   └─ 管理员 → admin/
```

**示例：**
- ✅ 个人资料 → `views/user/Profile.vue`（所有角色共用）
- ✅ 课程学习 → `views/student/course/Detail.vue`（学生专用）
- ✅ 课程管理 → `views/teacher/course/Detail.vue`（教师专用）
- ✅ 社区广场 → `views/shared/community/Plaza.vue`（所有登录用户）

## 🚀 优势总结

1. **更清晰的职责划分**：角色路由专注于角色特定功能，用户路由处理通用功能
2. **更简单的导航逻辑**：无需在多处判断角色
3. **更好的可维护性**：组件分类明确，易于查找和维护
4. **更符合直觉**：路径结构与功能语义对应

---

📅 更新日期：2026年2月3日
