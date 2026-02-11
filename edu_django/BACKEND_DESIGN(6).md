# Django 后端设计方案

基于 edu_vue2 前端项目的功能分析，本文档提供了完整的 Django 后端设计方案，包括目录结构、数据库模型关系（ER 设计）及关键 API 映射。

## 目录

* [1. 项目目录结构](#1-项目目录结构)
* [2. 数据库表关系设计 (Models)](#2-数据库表关系设计-models)
  * [2.1 用户模块 (apps.users)](#21-用户模块-appsusers)
  * [2.2 知识点模块 (apps.knowledge)](#22-知识点模块-appsknowledge-新增)
  * [2.3 课程模块 (apps.courses)](#23-课程模块-appscourses)
  * [2.4 学习模块 (apps.learning)](#24-学习模块-appslearning)
  * [2.5 作业模块 (apps.homework)](#25-作业模块-appshomework)
  * [2.6 考试模块 (apps.exams)](#26-考试模块-appsexams)
  * [2.7 社区模块 (apps.community)](#27-社区模块-appscommunity)
  * [2.8 运营模块 (apps.operations)](#28-运营模块-appsoperations)
  * [2.9 财务与订单模块 (apps.finance)](#29-财务与订单模块-appsfinance-补充)
  * [2.10 系统配置与消息模块 (apps.system)](#210-系统配置与消息模块-appssystem-新增)
* [3. 关键 API 路由映射](#3-关键-api-路由映射)
  * [3.1 认证模块 (Auth)](#31-认证模块-auth)
  * [3.2 教师端 (Teacher)](#32-教师端-teacher)
  * [3.3 学生端 (Student)](#33-学生端-student)
  * [3.4 管理员端 (Admin)](#34-管理员端-admin)
  * [3.5 公共/其他 (Public)](#35-公共其他-public)
* [4. 系统架构与关键技术补充](#4-系统架构与关键技术补充)

---

## 1. 项目目录结构

推荐采用 Django 的标准布局，并将所有业务应用（Apps）放入 apps/ 目录以保持整洁。

```text
backend/
├── manage.py
├── requirements.txt
├── config/                 # 项目配置目录
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py         # 核心配置（需配置 CORS, REST_FRAMEWORK）
│   ├── urls.py             # 主路由入口
│   └── wsgi.py
├── apps/                   # 业务应用模块
│   ├── __init__.py
│   ├── users/              # 用户与认证
│   ├── courses/            # 课程核心（课程、章节、课时、学期、班级）
│   ├── knowledge/          # 知识点与图谱（核心算法支撑）
│   ├── learning/           # 学习记录（选课、进度、证书）
│   ├── exams/              # 考试系统
│   ├── homework/           # 作业系统
│   ├── community/          # 问答与讨论区
│   ├── operations/         # 运营管理（审核、举报、统计）
│   ├── finance/            # 财务与订单
│   └── system/             # 系统配置与消息通知
├── media/                  # 用户上传文件（头像、课程封面、作业附件）
└── static/                 # 静态文件
```

---

## 2. 数据库表关系设计 (Models)

### 2.1 用户模块 (apps.users)

前端涉及：登录、注册、个人资料、角色管理。

#### **User** (继承 AbstractUser)

| 字段名 | 类型 | 说明 |
| :--- | :--- | :--- |
| username, password, email | 原生字段 | 用户名, 密码, 邮箱 |
| nickname | CharField | **(新增)** 昵称 (显示用) |
| avatar | ImageField | 头像 |
| bio | TextField | 个人简介 |
| phone | CharField | 手机号 (unique=True, 登录/找回密码核心字段) |
| gender | Enum | **(新增)** 性别 (Choices: male, female, secret) |
| school | CharField | 学校 |
| major | CharField | 专业 |
| created_at | DateTime | 注册时间 (auto_now_add=True) |
| updated_at | DateTime | **(新增)** 更新时间 (auto_now=True) |
| **(移除 role)** | - | **修改：** 移除单一 `role` 字段。用户身份由权限组 (Groups) 或 关联表 (TeacherProfile/StudentProfile) 决定，支持一人多角。 |

#### **StudentProfile** (学生档案)

| 字段名 | 类型 | 说明 |
| :--- | :--- | :--- |
| user | OneToOneField(User) | **关联用户** (unique=True) |
| student_id | CharField | 学号 (unique=True) |

#### **TeacherProfile** (教师档案)

| 字段名 | 类型 | 说明 |
| :--- | :--- | :--- |
| user | OneToOneField(User) | **关联用户** (unique=True) |
| teacher_id | CharField | 工号 (unique=True) |
<!-- | title | CharField | 职称 |
| introduction | TextField | 简介 | -->
| is_verified | Boolean | 认证状态 |

### 2.2 知识点模块 (apps.knowledge) **(新增)**

**核心支撑：** 为推荐算法、智能组卷、学情分析提供基础数据维度。

#### **Tag** (标签) **[通用多态关联]**

| 字段名 | 类型 | 说明 |
| :--- | :--- | :--- |
| name | CharField | 标签名称 (e.g., "Python", "难度:高") |
<!-- | type | Enum | 标签类型 (knowledge, difficulty, subject) | -->
| content_type | ForeignKey(ContentType) | **[多态关联]** 可关联 Course, Lesson, Question 等任意对象 |
| object_id | Integer | 关联对象ID |
| created_at | DateTime | **(新增)** 创建时间 |

#### **KnowledgePoint** (知识点) **[推荐算法基础]**

| 字段名 | 类型 | 说明 |
| :--- | :--- | :--- |
| parent | ForeignKey('self', null=True) | 父知识点 (支持树状结构) |
| name | CharField | 知识点名称 (e.g., "循环结构") |
<!-- | description | TextField | 知识点描述 | -->
<!-- | level | IntegerField | 难度等级 (1-5) (推荐权重) | -->
| **(移除 tags)** | - | **修改：** 与标签解耦，独立维护 |
| content_type | ForeignKey(ContentType) | **[多态关联]** 仅限关联 Course, Lesson, QuestionBank |
| object_id | Integer | 关联实体ID |
<!-- | created_at | DateTime | **(新增)** 创建时间 (auto_now_add=True) | -->

### 2.3 课程模块 (apps.courses)

前端涉及：课程展示、章节管理、班级管理。

#### **CourseCategory** (课程分类) **(新增)**

| 字段名 | 类型 | 说明 |
| :--- | :--- | :--- |
| name | CharField | 分类名称 (e.g., "后端开发", "Python") |
| parent | ForeignKey('self') | 父分类 |
| order | IntegerField | 排序权重 |
| is_visible | Boolean | 是否显示 |

#### **Course** (课程)

| 字段名 | 类型 | 说明 |
| :--- | :--- | :--- |
| teacher | ForeignKey(User) | 授课教师 (on_delete=models.PROTECT, 防止误删) |
| category | ForeignKey(CourseCategory) | **(新增)** 课程分类 (on_delete=models.SET_NULL) |
| title | CharField | 课程标题 |
| description | TextField | 课程描述 |
| cover | ImageField | 课程封面图 |
| price | DecimalField | **(修改)** 价格 (0.00代表免费) |
| difficulty | Enum | **(新增)** 难度 (beginner, intermediate, advanced) |
| status | Enum | 课程状态 (draft, pending_review, published, rejected) |
| audit_remark | TextField | 审核意见 |
| created_at | DateTime | **(新增)** 创建时间 |
| updated_at | DateTime | **(新增)** 更新时间 |

#### **Chapter** (章节)

| 字段名 | 类型 | 说明 |
| :--- | :--- | :--- |
| course | ForeignKey(Course) | 所属课程 |
| parent | ForeignKey('self', null=True) | **[新增]** 父章节 (支持多级树状结构/子章节) |
| title | CharField | 章节标题 |
<!-- | description | TextField | **(新增)** 章节简介 | -->
| order | IntegerField | 排序号 |
| created_at | DateTime | **(新增)** 创建时间 |

#### **Lesson** (课时/小节)

| 字段名 | 类型 | 说明 |
| :--- | :--- | :--- |
| chapter | ForeignKey(Chapter) | 所属章节 |
| title | CharField | 课时标题 |
| order | IntegerField | 排序号 |
<!-- | is_free | Boolean | **(新增)** 是否试看 | -->
| created_at | DateTime | **(新增)** 创建时间 |
| updated_at | DateTime | **(新增)** 更新时间 |

#### **LessonContentBlock** (课时内容块) **(新增) [多态内容组件]**

| 字段名 | 类型 | 说明 |
| :--- | :--- | :--- |
| lesson | ForeignKey(Lesson) | 所属课时 |
| type | Enum | 内容类型 (video, rich_text, file, image, code) |
| title | CharField | 块标题 (可选) |
| content | JSONField | 内容数据 (JSON存储配置/文本/代码片段，见下方示例) |
| file | FileField | 文件资源 (视频/图片/附件) |
| order | IntegerField | 块内排序 |
| created_at | DateTime | 创建时间 |

> **JSON 结构示例 (`content`):**
>
> *   **Video**: `{"video_url": "...", "duration": 120, "cover": "..."}`
> *   **Code**: `{"language": "python", "code": "print('hello')", "read_only": false}`
> *   **RichText**: `{"html": "<p>...</p>"}`

#### **CourseTerm** (课程班期) **(原 Term)**

| 字段名 | 类型 | 说明 |
| :--- | :--- | :--- |
| course | ForeignKey(Course) | 关联课程 |
| name | CharField | 班期名称 (e.g., "2023秋季一期") |
| start_date | Date | 开课日期 |
| end_date | Date | 结课日期 |
| enrollment_limit | IntegerField | 招生人数限制 |
| status | Enum | 状态 (recruiting, in_progress, finished) |

#### **ClassGroup** (教学班级)

| 字段名 | 类型 | 说明 |
| :--- | :--- | :--- |
| term | ForeignKey(CourseTerm) | **关联班期** (修改：不再直接关联 Course) |
| name | CharField | 班级名称 (e.g., "计算机1班") |
| head_teacher | ForeignKey(User) | 班主任/助教 |
| students | ManyToManyField(User) | 班级学生 |

> **约束：** `unique_together = ('term', 'name')`，确保同一班期下班级名不重复。

### 2.4 学习模块 (apps.learning)

前端涉及：选课、进度追踪、证书。

#### **Enrollment** (选课记录)

| 字段名 | 类型 | 说明 |
| :--- | :--- | :--- |
| student | ForeignKey(User) | 学生 |
| term | ForeignKey(CourseTerm) | **关联班期** (修改) |
| class_group | ForeignKey(ClassGroup, null=True) | 所属班级 |
| status | Enum | 状态 (active, completed, dropped) |
| created_at | DateTime | 选课时间 |

> **约束：** `unique_together = ('student', 'term')`，同一学生同一班期只能选一次。

<!-- #### **LearningProgress** (学习进度)

| 字段名 | 类型 | 说明 |
| :--- | :--- | :--- |
| student | ForeignKey(User) | **索引字段** |
| lesson | ForeignKey(Lesson) | **索引字段** |
| status | Enum | 状态 (not_started, in_progress, completed) |
| progress | FloatField | 进度百分比 (0-100) |
| last_position | Integer | 视频/文档上次观看位置 (秒/页) |
| last_learned_at | DateTime | 最近学习时间 |

> **索引：** 建议建立 `(student, lesson)` 联合索引以优化查询。 -->

#### **StudentKnowledgeMastery** (学生知识掌握度) **(新增) [学情分析]**

| 字段名             | 类型                         | 说明                                                 |
|:--------------- |:-------------------------- |:-------------------------------------------------- |
| student         | ForeignKey(User)           | 学生                                                 |
| knowledge_point | ForeignKey(KnowledgePoint) | 知识点                                                |
| mastery_level   | FloatField                 | 掌握度 (0.0 - 1.0) **[算法：得分 / 总分]** |
| total_attempts | IntegerField | **(新增)** 关联题目练习总次数 (作业/考试/测验) |
| total_score_earned | FloatField | **(新增)** 关联题目实际得分总和 |
| total_score_possible | FloatField | **(新增)** 关联题目总分值 |
| last_updated | DateTime | 更新时间 (auto_now=True) |

> **计算逻辑：** 每次提交作业/考试后，异步更新相关知识点的 `total_attempts` 等字段，`mastery_level = total_score_earned / total_score_possible` (可加权最近N次记录)。

#### **Certificate** (证书)

| 字段名 | 类型 | 说明 |
|:-------------- |:------------------ |:-------------- |
| student | ForeignKey(User) | 学生 |
| course | ForeignKey(Course) | 课程 |
| term | ForeignKey(CourseTerm, null=True) | **(新增)** 关联班期 |
| certificate_no | CharField | 证书编号 (唯一) |
| file | FileField | 证书文件 (生成的 PDF/Image) |
| template_url | URLField | **(新增)** 证书模板快照/背景图 |
| meta_snapshot | JSONField | **(新增)** 证书颁发时的元数据快照 (课程名、讲师、学期名等)，防止源数据变更 |
| score | IntegerField | **(新增)** 最终成绩 |
| status | Enum | **(新增)** 状态 (active, revoked, expired) |
| issued_at | DateTime | 颁发时间 |

> **数据一致性约束：** 颁发证书时，必须将当时的课程名、讲师名、学期等元数据写入 `meta_snapshot`。因为这些源数据在未来可能会变更（如讲师离职、课程改名），证书上的信息必须保持颁发时的状态。

### 2.5 作业模块 (apps.homework)

前端涉及：作业发布、提交、批改。

#### **HomeworkTemplate** (作业模板/题库) **(修改)**

| 字段名 | 类型 | 说明 |
| :--- | :--- | :--- |
| course | ForeignKey(Course) | 所属课程 |
| title | CharField | 作业标题 |
| content | RichTextField | 作业内容/要求 (若是纯客观题作业，此处可为空或仅写注意事项) |
| questions | ManyToManyField(QuestionBank) | **(新增)** 关联题目 (用于客观题自动批改，类似考试) |
| total_score | IntegerField | 总分 |


#### **HomeworkAssignment** (作业发布/任务) **(新增)**

| 字段名 | 类型 | 说明 |
| :--- | :--- | :--- |
| template | ForeignKey(HomeworkTemplate) | 关联作业模板 |
| title | CharField | **(新增)** 作业标题 (发布时固化模板标题，也可自定义) |
| term | ForeignKey(CourseTerm) | 关联班期 |
| class_group | ForeignKey(ClassGroup, null=True) | 指定班级 (为空则发给全班期) |
| specific_students | ManyToManyField(User) | 指定学生 (例外/补考) |
| deadline | DateTime | 截止时间 |
| content_snapshot | JSONField | **(新增)** 作业完整快照 (包含题目、分值、标准答案)，确保题库修改不影响已发布作业 (相当于“印好的试卷”) |
| is_published | Boolean | 是否发布 |

> **数据一致性约束：** 必须使用 Django Signals (`pre_save`) 或重写 `save()` 方法，在 `is_published=True` 时自动生成 `content_snapshot`。若开发时遗漏此逻辑，将导致历史作业内容随题库变更而错误变化。必须编写单元测试覆盖此场景。

#### **HomeworkSubmission** (学生提交)

| 字段名 | 类型 | 说明 |
| :--- | :--- | :--- |
| assignment | ForeignKey(HomeworkAssignment) | **关联发布记录** (修改) |
| student | ForeignKey(User) | 学生 |
| content | JSONField | **(修改)** 提交内容 (仅存答案，不含题目 - 相当于“答题卡”) |
| files | JSONField | 附件 |
| status | Enum | **(新增)** 状态 (draft, submitted, graded) |
| score | IntegerField | 得分 |
| feedback | TextField | 评语 |

### 2.6 考试模块 (apps.exams)

前端涉及：试卷创建、答题、自动/手动阅卷。

#### **QuestionBank** (题库) **(新增) [智能组卷数据源]**

| 字段名 | 类型 | 说明 |
| :--- | :--- | :--- |
| title | CharField | 题目名称 (后台管理检索用，不展示给学生) |
| type | Enum | 题目类型 (single, multiple, true_false, fill, essay) |
| content | JSONField | **(新增)** 题目完整内容 (题干、选项、答案、解析 - 学生看到的内容) |
| grading_rule | JSONField | **(新增)** 自动批改规则 (e.g. `{"fuzzy_match": true, "ignore_case": true}`) |
| difficulty | FloatField | **(修改)** 难度系数 (0.1 - 1.0) **[Greedy Algorithm (贪心算法) - 适配度参数]** |
| is_active | Boolean | **[软删除]** 是否启用 (False表示删除，不物理删除以保护历史数据) |
| knowledge_points | ManyToManyField | 关联知识点 |
| created_by | ForeignKey | 出题人 |
| created_at | DateTime | 创建时间 |
| updated_at | DateTime | 更新时间 |

> **JSON 结构示例 (`content` 字段):**
>
> 1. **单选题 (single)**:
>    ```json
>    {
>      "stem": "以下哪个是Python的关键字？",
>      "options": [
>        {"key": "A", "text": "func"},
>        {"key": "B", "text": "def"}
>      ],
>      "answer": "B",
>      "analysis": "def 用于定义函数。"
>    }
>    ```
> 2. **多选题 (multiple)**:
>    ```json
>    {
>      "stem": "以下属于面向对象特征的是？",
>      "options": [
>        {"key": "A", "text": "封装"},
>        {"key": "B", "text": "继承"}
>      ],
>      "answer": ["A", "B"],
>      "analysis": "封装、继承、多态是OOP三大特性。"
>    }
>    ```
> 3. **填空题 (fill)**:
>    ```json
>    {
>      "stem": "Python中用于输出的函数是 ____。",
>      "answer": ["print"],
>      "analysis": "print()是标准输出函数。"
>    }
>    ```

#### **ExamPaper** (试卷模板) **(修改)**

| 字段名 | 类型 | 说明 |
| :--- | :--- | :--- |
| course | ForeignKey(Course) | 所属课程 |
| title | CharField | 试卷标题 |
| total_score | IntegerField | 总分 |
| questions | ManyToManyField(QuestionBank) | **[编辑关联]** 用于组卷编辑时的关联 |
| status | Enum | **(新增)** 状态 (draft, published) |

> **注：** `ExamPaper` 仅作为试卷内容的“模板”。真正的“发布快照”存储在 `ExamSession` 中，以保证不同场次的考试内容独立且一致。

#### **ExamSession** (考试场次) **(新增)**

| 字段名 | 类型 | 说明 |
| :--- | :--- | :--- |
| paper | ForeignKey(ExamPaper) | 关联试卷 |
| term | ForeignKey(CourseTerm) | 关联班期 |
| class_group | ForeignKey(ClassGroup) | 关联班级 |
| start_time | DateTime | 开始时间 |
| end_time | DateTime | 结束时间 |
| questions_snapshot | JSONField | **(新增) [发布快照]** 考试发布时的题目内容固化 (防止题库修改影响已发布考试) |
| is_published | Boolean | **(新增)** 是否发布 (发布时生成快照) |

> **数据一致性约束：** 必须使用 Django Signals (`pre_save`) 或重写 `save()` 方法，在 `is_published=True` 时自动生成 `questions_snapshot`。若开发时遗漏此逻辑，将导致历史考试内容随题库变更而错误变化。

#### **ExamSubmission** (考试记录)

| 字段名 | 类型 | 说明 |
| :--- | :--- | :--- |
| session | ForeignKey(ExamSession) | **关联场次** (修改) |
| student | ForeignKey(User) | 学生 |
| answers | JSONField | **(新增)** 考生答卷数据 (题目ID: 答案内容) |
| total_score | IntegerField | 总分 |
| submit_time | DateTime | **(新增)** 提交时间 |
| status | Enum | **(修改)** 状态 (ongoing, submitted, grading, graded) |
| reviewer | ForeignKey(User) | **(新增)** 阅卷人 (教师/管理员) |
| reviewed_at | DateTime | **(新增)** 阅卷时间 |
| feedback | TextField | **(新增)** 评语 |

> **注：** `ExamPaperRule` (组卷规则) 仅作为生成试卷时的临时参数或日志，无需作为核心业务表长期维护。

#### **ExamAnswer** (答题详情) **[自动阅卷]**

| 字段名 | 类型 | 说明 |
| :--- | :--- | :--- |
| submission | ForeignKey(ExamSubmission) | 关联考试记录 |
| question_snapshot | JSONField | **[题目快照]** 存储答题时的题目内容(防止原题修改) |
| answer_content | TextField | 学生答案 |
| score | IntegerField | 得分 |

### 2.7 社区模块 (apps.community)

前端涉及：课程讨论、公共问答、点赞。

#### **Thread** (帖子/问题)

| 字段名 | 类型 | 说明 |
| :--- | :--- | :--- |
| author | ForeignKey(User) | 作者 |
| course | ForeignKey(Course, null=True) | 关联课程 (为空则是公共广场帖子) |
| category | CharField | **(新增)** 分类 (e.g. '技术分享', '公共问答') |
| title | CharField | 帖子标题 |
| excerpt | CharField | **(新增)** 摘要 (列表页显示) |
| content | TextField | 帖子内容 |
| type | Enum | 类型 (question, discussion) |
| is_pinned | Boolean | 是否置顶 |
| is_essence | Boolean | **(新增)** 是否加精 |
| view_count | IntegerField | 浏览量 |
| reply_count | IntegerField | **(新增)** 回复数 (冗余字段，优化查询) |
| like_count | IntegerField | **(新增)** 点赞数 (冗余字段) |
| last_reply_at | DateTime | **(新增)** 最后回复时间 |
| created_at | DateTime | **(新增)** 创建时间 |
| updated_at | DateTime | **(新增)** 更新时间 |

#### **Comment** (回答/评论)

| 字段名 | 类型 | 说明 |
| :--- | :--- | :--- |
| thread | ForeignKey(Thread) | 关联帖子 |
| author | ForeignKey(User) | 作者 |
| content | TextField | 评论内容 |
| parent | ForeignKey('self', null=True) | 父评论 (用于楼中楼) |
| like_count | IntegerField | **(新增)** 点赞数 |
| is_accepted | Boolean | 是否采纳 (作为最佳答案) |
| created_at | DateTime | **(新增)** 评论时间 |

#### **PostLike** (帖子点赞) **(新增)**

| 字段名 | 类型 | 说明 |
| :--- | :--- | :--- |
| user | ForeignKey(User) | 点赞用户 |
| thread | ForeignKey(Thread) | 点赞帖子 |
| created_at | DateTime | 点赞时间 |

#### **CommentLike** (评论点赞) **(新增)**

| 字段名 | 类型 | 说明 |
| :--- | :--- | :--- |
| user | ForeignKey(User) | 点赞用户 |
| comment | ForeignKey(Comment) | 点赞评论 |
| created_at | DateTime | 点赞时间 |

### 2.8 运营模块 (apps.operations)

前端涉及：举报处理、后台统计。

#### **Banner** (轮播图) **(新增)**

| 字段名 | 类型 | 说明 |
| :--- | :--- | :--- |
| title | CharField | 标题 |
| image | ImageField | 图片地址 |
| link_url | URLField | 跳转链接 |
| order | IntegerField | 排序 |
| position | Enum | 位置 (home_top, course_list_top) |
| is_active | Boolean | 是否启用 |

#### **Announcement** (系统公告) **(新增)**

| 字段名 | 类型 | 说明 |
| :--- | :--- | :--- |
| title | CharField | 标题 |
| content | RichTextField | 内容 |
| is_popup | Boolean | 是否弹窗强提醒 |
| start_time | DateTime | 展示开始时间 |
| end_time | DateTime | 展示结束时间 |
| created_at | DateTime | 创建时间 |

#### **DailyStat** (每日统计) **(新增)**

| 字段名 | 类型 | 说明 |
| :--- | :--- | :--- |
| date | DateField | 统计日期 (unique) |
| new_users | IntegerField | 新增用户数 |
| active_users | IntegerField | 活跃用户数 |
| new_courses | IntegerField | 新增课程数 |
| total_enrollments | IntegerField | 累计选课人次 |
| new_enrollments | IntegerField | 当日选课人次 |
| certificates_issued | IntegerField | 颁发证书数 |
| total_income | DecimalField | 当日营收 |

#### **Report** (举报)

| 字段名 | 类型 | 说明 |
| :--- | :--- | :--- |
| reporter | ForeignKey(User) | 举报人 |
| content_type | (Thread, Comment, Course 等) | 举报对象类型 |
| object_id | Integer | 举报对象ID |
| reason | CharField | 举报原因 |
| content_snapshot | JSONField | **(新增)** 被举报内容快照 (防止用户删除/修改证据) |
| status | Enum | 处理状态 (pending, resolved, rejected) |
| admin_remark | TextField | **(新增)** 处理备注 |
| created_at | DateTime | 举报时间 |
| handled_at | DateTime | **(新增)** 处理时间 |

> **数据一致性约束：** 创建举报记录时，必须立即读取并保存 `content_snapshot`。建议在 `perform_create` 或 `save()` 中实现，确保举报时刻的内容被永久保留。

### 2.9 财务与订单模块 (apps.finance) **(补充)**

**必要性：** 虽然课程可能有免费的，但为了记录“购买/获取”行为（防止后续改为收费），以及处理退课、退款逻辑，通常需要订单系统。

#### **Order** (订单)

| 字段名 | 类型 | 说明 |
| :--- | :--- | :--- |
| order_no | CharField | 订单号 (唯一, e.g., "ORD20231027001") |
| user | ForeignKey(User) | 下单用户 |
| term | ForeignKey(CourseTerm) | **关联班期** (修改：购买的是具体班期) |
| amount | DecimalField | 实付金额 |
| snapshot_price | DecimalField | **[价格快照]** 下单时的单价 (防止后续改价) |
| status | Enum | 状态 (pending, paid, cancelled, refunded) |
| payment_method | Enum | 支付方式 (alipay, wechat, system_free) |
| transaction_id | CharField | **(新增)** 第三方支付流水号 |
| paid_at | DateTime | 支付/完成时间 |
| refund_amount | DecimalField | **(新增)** 退款金额 |
| refund_reason | CharField | **(新增)** 退款原因 |
| refunded_at | DateTime | **(新增)** 退款时间 |
| created_at | DateTime | 创建时间 |

> **数据一致性约束：** 创建订单时，必须从关联的 `CourseTerm` 或商品表中读取当前价格并写入 `snapshot_price`。严禁直接关联动态价格字段，以防止后续商品改价导致历史订单金额不一致。

> **设计备注：** 如果未来要卖“会员卡”或“实体书”，建议把关联字段 (`term`) 设计得更通用（如 `GenericForeignKey`）。但在当前 MVP 阶段，关联 `CourseTerm` 是最简单直接的，保持现状即可。

### 2.10 系统配置与消息模块 (apps.system) **(新增)**

前端涉及：系统设置、消息中心。

#### **Task** (异步任务) **(新增)**

| 字段名 | 类型 | 说明 |
| :--- | :--- | :--- |
| task_id | UUIDField | 任务ID (Celery Task ID) |
| name | CharField | 任务名称 (e.g., "generate_exam", "transcode_video") |
| user | ForeignKey(User) | 触发用户 |
| status | Enum | 状态 (pending, processing, success, failure) |
| result | JSONField | 任务结果 (e.g., 生成的试卷ID, 错误信息) |
| created_at | DateTime | 创建时间 |
| finished_at | DateTime | 完成时间 |

#### **SystemConfig** (系统配置)

| 字段名 | 类型 | 说明 |
| :--- | :--- | :--- |
| key | CharField | 配置键 (unique, e.g., "site_name", "allow_register") |
| value | JSONField | 配置值 (支持各种类型) |
| description | CharField | 描述 |
| is_public | Boolean | 是否公开 (前端可见) |
| updated_at | DateTime | 更新时间 |

#### **Message** (消息通知)

| 字段名 | 类型 | 说明 |
| :--- | :--- | :--- |
| sender | ForeignKey(User, null=True) | 发送者 (系统消息为空) |
| receiver | ForeignKey(User) | 接收者 |
| type | Enum | 消息类型 (system, course, interaction, security) |
| title | CharField | 标题 |
| content | TextField | 内容 |
| related_link | CharField | 跳转链接 (可选) |
| is_read | Boolean | 是否已读 |
| created_at | DateTime | 发送时间 |

---
<!-- 
## 3. 关键 API 路由映射

前端 `axios` `baseURL` 默认为 `http://localhost:8000/api`。后端 `config/urls.py` 应包含 `path('api/', include('...'))`。

以下是基于前端代码（`src/router/` 和 `src/api/`）梳理的完整路由映射表：

### 3.1 认证模块 (Auth)

| 前端页面 (Route)       | 前端 API 调用 (src/api/auth.js)  | 建议后端 URL (Django)            | 备注              |
|:------------------ |:---------------------------- |:---------------------------- |:--------------- |
| `/login`           | `POST /auth/login`           | `/api/auth/login/`           | JWT 登录          |
| `/register`        | `POST /auth/register`        | `/api/auth/register/`        | 用户注册            |
| `/forgot-password` | `POST /auth/forget-password` | `/api/auth/forget-password/` |                 |
| -                  | `POST /auth/reset-password`  | `/api/auth/reset-password/`  |                 |
| -                  | `POST /auth/change-password` | `/api/auth/change-password/` | 需登录             |
| -                  | `GET /auth/profile`          | `/api/auth/profile/`         | 获取个人信息          |
| -                  | `POST /auth/logout`          | `/api/auth/logout/`          | 登出 (前端销毁 Token) |

### 3.2 教师端 (Teacher)

| 前端页面 (Route)                      | 前端 API 调用 (src/api/teacher.js)      | 建议后端 URL (Django)                      | 核心逻辑/算法支持                       |
|:--------------------------------- |:----------------------------------- |:-------------------------------------- |:------------------------------- |
| `/teacher/courses`                | `GET /teacher/courses`              | `/api/teacher/courses/`                | 教师课程列表                          |
| `/teacher/courses/create`         | `POST /teacher/courses`             | `/api/teacher/courses/`                | 创建课程                            |
| `/teacher/courses/:id`            | `GET /teacher/courses/:id`          | `/api/teacher/courses/:pk/`            | 课程详情                            |
| -                                 | `POST /teacher/courses/:id/publish` | `/api/teacher/courses/:pk/publish/`    | 发布课程                            |
| `/teacher/courses/:id/chapters`   | `GET .../chapters`                  | `/api/teacher/courses/:pk/chapters/`   | 章节管理                            |
| `/teacher/homework`               | `GET /teacher/homework`             | `/api/teacher/homework/`               | 作业库列表                           |
| -                                 | `POST /teacher/homework/:id/grade`  | `/api/teacher/homework/:pk/grade/`     | **[Auto-Grading]** 触发自动批改(客观题)  |
| `/teacher/exams`                  | `GET /teacher/exams`                | `/api/teacher/exams/`                  | 考试库列表                           |
| `/teacher/exams/create`           | `POST /teacher/exams/intelligent`   | `/api/teacher/exams/intelligent/`      | **[Genetic Algorithm]** 智能组卷接口  |
| -                                 | `POST /teacher/exams/:id/grade`     | `/api/teacher/exams/:pk/grade/`        | **[Auto-Grading]** 触发自动批改       |
| `/teacher/courses/:id/statistics` | `GET .../statistics`                | `/api/teacher/courses/:pk/statistics/` | **[Learning Analytics]** 课程统计报表 |

### 3.3 学生端 (Student)

| 前端页面 (Route)                       | 前端 API 调用 (src/api/student.js)  | 建议后端 URL (Django)                                | 核心逻辑/算法支持                     |
|:---------------------------------- |:------------------------------- |:------------------------------------------------ |:----------------------------- |
| `/student/courses`                 | `GET /student/enrollments`      | `/api/student/enrollments/`                      | 我的选课列表                        |
| -                                  | `POST /student/enrollments`     | `/api/student/enrollments/`                      | 选课/报名                         |
| `/student/courses/:id`             | `GET /student/courses/:id`      | `/api/student/courses/:pk/`                      | 学习页课程详情                       |
| `/student/courses/:id/lessons/:id` | `GET .../lessons/:lessonId`     | `/api/student/courses/:pk/lessons/:id/`          | 课时详情                          |
| -                                  | `POST .../lessons/:id/progress` | `/api/student/courses/:pk/lessons/:id/progress/` | **[BKT/IRT]** 更新学习进度与知识点掌握度   |
| `/student/homework`                | `GET /student/homework`         | `/api/student/homework/`                         | 我的作业列表                        |
| -                                  | `POST .../homework/:id/submit`  | `/api/student/courses/:pk/homework/:id/submit/`  | **[NLP/Rule-Based]** 提交作业并预判分 |
| `/student/exams`                   | `GET /student/exams`            | `/api/student/exams/`                            | 我的考试列表                        |
| -                                  | `POST .../exams/:id/start`      | `/api/student/courses/:pk/exams/:id/start/`      | 开始考试                          |
| -                                  | `POST .../exams/:id/submit`     | `/api/student/courses/:pk/exams/:id/submit/`     | **[Auto-Grading]** 交卷触发自动阅卷   |
| `/student/certificates`            | `GET /student/certificates`     | `/api/student/certificates/`                     | 我的证书                          |

### 3.4 管理员端 (Admin)

| 前端页面 (Route)            | 前端 API 调用 (src/api/admin.js)    | 建议后端 URL (Django)                | 备注    |
|:----------------------- |:------------------------------- |:-------------------------------- |:----- |
| `/admin/dashboard`      | `GET /admin/dashboard/stats`    | `/api/admin/dashboard/stats/`    | 仪表盘统计 |
| `/admin/users`          | `GET /admin/users`              | `/api/admin/users/`              | 用户管理  |
| `/admin/courses/audit`  | `GET /admin/courses/audit-list` | `/api/admin/courses/audit-list/` | 课程审核  |
| `/admin/content/review` | `GET /admin/reports`            | `/api/admin/reports/`            | 内容审查  |

### 3.5 公共/其他 (Public)

| 前端页面 (Route)   | 前端 API 调用 (src/api/course.js) | 建议后端 URL (Django)   | 核心逻辑/算法支持                         |
|:-------------- |:----------------------------- |:------------------- |:--------------------------------- |
| `/courses`     | `GET /courses`                | `/api/courses/`     | **[UserCF/Content-Based]** 推荐课程列表 |
| `/courses/:id` | `GET /courses/:id`            | `/api/courses/:pk/` | **[ItemCF]** 关联课程推荐               |

---

## 4. 系统架构与关键技术补充

为了支撑文档中提到的“智能组卷”、“推荐算法”和“自动阅卷”等高阶功能，仅靠 Django 的同步请求响应模型是不够的，建议补充以下基础设施：

### 4.1 异步任务队列 (Celery + Redis/RabbitMQ)

**核心用途：** 剥离耗时计算，防止前端请求超时。

* **智能组卷 (Genetic Algorithm)**: 遗传算法迭代可能需要 2-10秒，必须异步执行。用户发起请求后，后端返回 TaskID，前端轮询或通过 WebSocket 接收结果。
* **自动阅卷 (Auto-Grading)**: 特别是 NLP 语义分析和代码运行，属于 CPU 密集型任务，需放入队列。
* **发送通知**: 邮件、短信发送。

### 4.2 缓存中间件 (Redis)

**核心用途：** 提升高频读取数据的性能。

* **推荐列表缓存**: UserCF/ItemCF 的计算结果（如“每日推荐”）通常每天/每小时更新一次，结果应存入 Redis，读取速度快。
* **排行榜**: 热门课程、活跃学生榜单。
* **Session/Token**: JWT 黑名单或用户 Session 存储。

### 4.3 实时通信 (Django Channels / WebSocket)

**核心用途：** 解决“服务器主动推送到前端”的需求。

* **考试场景**: 考试结束前 5 分钟倒计时强提醒、老师强制收卷信号。
* **阅卷通知**: “您的试卷已批改完成，点击查看详情”。
* **在线客服/私信**: 师生实时沟通。

### 4.4 文件存储 (Object Storage)

* **建议**: 开发环境可用本地 `media/` 目录，生产环境建议接入 AWS S3、阿里云 OSS 或 MinIO。
* **原因**: 视频课程和大量图片会迅速占满应用服务器磁盘，且不利于横向扩展。

---
 -->
