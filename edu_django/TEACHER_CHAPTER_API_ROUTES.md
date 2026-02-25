# 教师课程章节管理 API 路由文档

## 1. 章节管理

### 1.1 获取课程章节列表
- **接口**: `GET /api/teacher/courses/{course_id}/chapters/`
- **说明**: 获取课程的所有章节和小节目录结构
- **响应示例**:
```json
{
  "course_title": "Python入门",
  "teacher_name": "张老师",
  "chapters": [
    {
      "id": 1,
      "title": "第一章",
      "order": 0,
      "lessons": [
        {
          "id": 101,
          "title": "课时1",
          "order": 0
        }
      ]
    }
  ]
}
```

### 1.2 创建章节
- **接口**: `POST /api/teacher/courses/{course_id}/chapters/`
- **请求体**:
```json
{
  "title": "新章节",
  "order": 0
}
```
- **响应**:
```json
{
  "id": 2,
  "title": "新章节",
  "order": 0
}
```

### 1.3 更新章节
- **接口**: `PUT /api/teacher/courses/{course_id}/chapters/{chapter_id}/`
- **请求体**:
```json
{
  "title": "修改后的章节名称"
}
```

### 1.4 删除章节
- **接口**: `DELETE /api/teacher/courses/{course_id}/chapters/{chapter_id}/`
- **说明**: 删除章节会级联删除该章节下的所有小节和内容

### 1.5 章节排序
- **接口**: `POST /api/teacher/courses/{course_id}/chapters/sort/`
- **请求体**:
```json
{
  "chapter_orders": [
    {"id": 1, "order": 0},
    {"id": 2, "order": 1}
  ]
}
```


---

## 2. 小节管理

### 2.1 创建小节
- **接口**: `POST /api/teacher/courses/{course_id}/chapters/{chapter_id}/lessons/`
- **请求体**:
```json
{
  "title": "新小节",
  "order": 0
}
```
- **响应**:
```json
{
  "id": 101,
  "title": "新小节",
  "chapter_id": 1,
  "order": 0
}
```

### 2.2 更新小节
- **接口**: `PUT /api/teacher/courses/{course_id}/lessons/{lesson_id}/`
- **请求体**:
```json
{
  "title": "修改后的小节名称"
}
```
- **说明**: 小节标题输入框失焦时自动调用

### 2.3 删除小节
- **接口**: `DELETE /api/teacher/courses/{course_id}/lessons/{lesson_id}/`
- **说明**: 删除小节会级联删除该小节下的所有内容块

### 2.4 获取小节详情(懒加载)
- **接口**: `GET /api/teacher/courses/{course_id}/lessons/{lesson_id}/`
- **说明**: 点击小节时调用,获取该小节的所有内容块
- **响应示例**:
```json
{
  "lesson_id": 101,
  "title": "1.1 Python安装",
  "chapter_id": 1,
  "content_blocks": [
    {
      "id": 1,
      "type": "video",
      "title": "安装教学视频",
      "file_url": "/media/lessons/videos/2026/02/video.mp4",
      "content": {
        "watch_percent": 80
      },
      "order": 0
    },
    {
      "id": 2,
      "type": "rich_text",
      "title": "课时说明",
      "content": {
        "html": "<p>本节将介绍...</p>"
      },
      "order": 1
    },
    {
      "id": 3,
      "type": "file",
      "title": "课件.pdf",
      "file_url": "/media/lessons/files/2026/02/doc.pdf",
      "order": 2
    }
  ]
}
```

---

## 3. 课时内容块管理

### 3.1 批量保存内容块
- **接口**: `POST /api/teacher/courses/{course_id}/lessons/{lesson_id}/content-blocks/`
- **说明**: 点击"全量保存"按钮时调用,保存当前小节的所有内容块
- **请求体**:
```json
{
  "content_blocks": [
    {
      "type": "video",
      "title": "教学视频",
      "file": "/media/lessons/videos/2026/02/video.mp4",
      "content": {
        "watch_percent": 80
      },
      "order": 0
    },
    {
      "type": "rich_text",
      "title": "课时说明",
      "content": {
        "html": "<p>课时内容...</p>"
      },
      "order": 1
    },
    {
      "type": "file",
      "title": "课件资料.pdf",
      "file": "/media/lessons/files/2026/02/doc.pdf",
      "order": 2
    }
  ]
}
```

### 3.2 内容块数据结构

#### 后端模型字段:
```python
class LessonContentBlock(models.Model):
    TYPE_CHOICES = [
        ('video', '视频'),
        ('rich_text', '富文本'),
        ('file', '文件附件'),
        ('image', '图片'),
        ('code', '代码片段'),
    ]
    
    lesson = ForeignKey(Lesson)  # 所属课时
    type = CharField(max_length=20)  # 内容类型
    title = CharField(max_length=200)  # 块标题
    content = JSONField()  # JSON存储配置/文本/代码
    file = FileField()  # 文件资源(视频/图片/附件)
    order = IntegerField()  # 块内排序
```

#### 前端到后端类型映射:
| 前端类型 | 后端类型 | file字段 | content字段 |
|---------|---------|---------|------------|
| video | video | 视频URL | `{watch_percent: 80}` |
| document | file | 文件URL | null |
| text | rich_text | null | `{html: "..."}` |
| quiz | rich_text | null | `{html: "测验内容"}` |

---

## 4. 操作时机说明

### 实时保存操作(立即调用API):
1. ✅ **添加章节** - 立即创建
2. ✅ **添加小节** - 立即创建
3. ✅ **重命名章节** - 弹窗确认后立即更新
4. ✅ **重命名小节** - 右键菜单确认后立即更新
5. ✅ **删除章节** - 确认后立即删除
6. ✅ **删除小节** - 确认后立即删除
7. ✅ **修改小节标题** - 输入框失焦时自动保存

### 批量保存操作(点击按钮):
1. ✅ **保存内容块** - 点击"全量保存"按钮,保存当前选中小节的所有内容块

### 懒加载操作:
1. ✅ **加载章节目录** - 进入编辑器时加载
2. ✅ **加载小节内容** - 点击小节时加载content_blocks

---

## 5. 前端API调用文件

文件: `src/api/teacher.js`

```javascript
// 章节管理
export const getCourseChapters = (courseId) => 
  http.get(`/teacher/courses/${courseId}/chapters/`)

export const createChapter = (courseId, data) => 
  http.post(`/teacher/courses/${courseId}/chapters/`, data)

export const updateChapter = (courseId, chapterId, data) => 
  http.put(`/teacher/courses/${courseId}/chapters/${chapterId}/`, data)

export const deleteChapter = (courseId, chapterId) => 
  http.delete(`/teacher/courses/${courseId}/chapters/${chapterId}/`)

export const sortChapters = (courseId, data) => 
  http.post(`/teacher/courses/${courseId}/chapters/sort/`, data)

// 小节管理
export const createLesson = (courseId, chapterId, data) => 
  http.post(`/teacher/courses/${courseId}/chapters/${chapterId}/lessons/`, data)

export const updateLesson = (courseId, lessonId, data) => 
  http.put(`/teacher/courses/${courseId}/lessons/${lessonId}/`, data)

export const deleteLesson = (courseId, lessonId) => 
  http.delete(`/teacher/courses/${courseId}/lessons/${lessonId}/`)

export const getLessonDetail = (courseId, lessonId) => 
  http.get(`/teacher/courses/${courseId}/lessons/${lessonId}/`)

// 内容块管理
export const saveContentBlocks = (courseId, lessonId, data) => 
  http.post(`/teacher/courses/${courseId}/lessons/${lessonId}/content-blocks/`, data)
```

---

## 6. 注意事项

1. ✅ **所有路由末尾必须带斜杠 `/`**
2. ✅ **章节ID和小节ID都是后端生成返回**
3. ✅ **小节的更新/删除不需要传 chapter_id**
4. ✅ **内容块保存是覆盖式的,每次保存会替换该小节的所有内容块**
5. ✅ **文件上传需要先上传到服务器获取URL,再保存到content_blocks**
6. ✅ **前端 document 类型映射为后端 file 类型**
7. ✅ **前端 text 类型映射为后端 rich_text 类型**
