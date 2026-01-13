<template>
  <div class="student-course-detail">
    <div class="page-header">
      <div class="header-left">
        <el-button icon="el-icon-arrow-left" @click="goBack">返回</el-button>
        <div class="course-title">
          <h1>{{ courseInfo.title }}</h1>
          <p>{{ courseInfo.instructorName }}</p>
        </div>
      </div>
    </div>

    <div class="course-container">
      <!-- 左侧导航栏 -->
      <aside class="sidebar">
        <nav class="nav-menu">
          <div
            v-for="item in navItems"
            :key="item.id"
            :class="['nav-item', { active: activeModule === item.id }]"
            @click="selectModule(item.id)"
            tabindex="0"
            role="button"
          >
            <span class="nav-icon">{{ item.icon }}</span>
            <span class="nav-label">{{ item.label }}</span>
          </div>
        </nav>
      </aside>

      <!-- 右侧内容区 -->
      <main class="content-area">
        <!-- 章节模块 - 章节目录概览 -->
        <section v-if="activeModule === 'sections'" class="module-section">
          <div class="sections-overview">
            <div class="overview-header">
              <h2>课程章节</h2>
              <el-input
                v-model="chapterSearch"
                placeholder="搜索章节或课程..."
                prefix-icon="el-icon-search"
                clearable
                style="width: 300px;"
              />
            </div>

            <div class="sections-list">
              <div
                v-for="section in filteredSections"
                :key="section.id"
                class="section-card"
              >
                <div class="section-card-header" @click="toggleSection(section.id)">
                  <div class="section-info">
                    <span :class="['expand-icon', { expanded: expandedSections.includes(section.id) }]">▶</span>
                    <h3>{{ section.title }}</h3>
                  </div>
                  <div class="section-meta">
                    <span class="lesson-count">{{ section.lessons.length }} 课时</span>
                  </div>
                </div>

                <div
                  v-show="expandedSections.includes(section.id)"
                  class="section-lessons"
                >
                  <div
                    v-for="(lesson, index) in section.lessons"
                    :key="lesson.id"
                    class="lesson-card"
                    @click="selectLesson(lesson, section)"
                  >
                    <div class="lesson-index">{{ index + 1 }}</div>
                    <div class="lesson-icon">
                      {{ lesson.type === 'video' ? '🎥' : '📄' }}
                    </div>
                    <div class="lesson-content">
                      <div class="lesson-name">{{ lesson.name }}</div>
                      <div class="lesson-meta">
                        <span>{{ lesson.duration }}</span>
                      </div>
                    </div>
                    <div class="lesson-action">
                      <el-button type="text" size="small">
                        {{ lesson.type === 'video' ? '观看' : '查看' }}
                        <i class="el-icon-arrow-right"></i>
                      </el-button>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <div v-if="filteredSections.length === 0" class="no-data">
              <i class="el-icon-folder-opened" style="font-size: 48px; color: #dcdfe6;"></i>
              <p>未找到相关章节</p>
            </div>
          </div>
        </section>

        <!-- 作业模块 -->
        <section v-if="activeModule === 'homework'" class="module-section">
          <!-- 课程标题 -->
          <div class="course-title-bar">
            <h2>{{ courseInfo.title }}</h2>
          </div>

          <!-- 筛选区域 -->
          <div class="filter-bar">
            <div class="filter-tabs">
              <button 
                :class="['filter-tab', { active: homeworkFilter === 'all' }]"
                @click="homeworkFilter = 'all'"
              >
                全部
              </button>
              <button 
                :class="['filter-tab', { active: homeworkFilter === 'completed' }]"
                @click="homeworkFilter = 'completed'"
              >
                已完成
              </button>
              <button 
                :class="['filter-tab', { active: homeworkFilter === 'pending' }]"
                @click="homeworkFilter = 'pending'"
              >
                未完成
              </button>
            </div>
          </div>

          <!-- 作业列表 -->
          <div v-if="filteredHomeworks.length > 0" class="task-list">
            <div 
              v-for="homework in filteredHomeworks" 
              :key="homework.id" 
              class="task-item"
              @click="viewHomework(homework)"
            >
              <div class="task-type-badge">作业</div>
              <div class="task-content">
                <div class="task-title">{{ homework.title }}</div>
                <div class="task-meta">
                  <span>截止: {{ homework.dueDate }}</span>
                  <span v-if="homework.score !== null">得分: {{ homework.score }}/{{ homework.totalPoints }}</span>
                </div>
              </div>
              <div :class="['task-status', homework.status]">
                {{ getHomeworkStatusText(homework.status) }}
              </div>
            </div>
          </div>

          <div v-else class="no-data">
            <p>{{ homeworkFilter === 'all' ? '暂无作业' : '暂无相关作业' }}</p>
          </div>
        </section>

        <!-- 考试模块 -->
        <section v-if="activeModule === 'exams'" class="module-section">
          <!-- 课程标题 -->
          <div class="course-title-bar">
            <h2>{{ courseInfo.title }}</h2>
          </div>

          <!-- 筛选区域 -->
          <div class="filter-bar">
            <div class="filter-tabs">
              <button 
                :class="['filter-tab', { active: examFilter === 'all' }]"
                @click="examFilter = 'all'"
              >
                全部
              </button>
              <button 
                :class="['filter-tab', { active: examFilter === 'completed' }]"
                @click="examFilter = 'completed'"
              >
                已完成
              </button>
              <button 
                :class="['filter-tab', { active: examFilter === 'pending' }]"
                @click="examFilter = 'pending'"
              >
                未完成
              </button>
            </div>
          </div>

          <!-- 考试列表 -->
          <div v-if="filteredExams.length > 0" class="task-list">
            <div 
              v-for="exam in filteredExams" 
              :key="exam.id" 
              class="task-item"
              @click="handleExamClick(exam)"
            >
              <div class="task-type-badge exam">考试</div>
              <div class="task-content">
                <div class="task-title">{{ exam.title }}</div>
                <div class="task-meta">
                  <span>时长: {{ exam.duration }}分钟</span>
                  <span>题目: {{ exam.questionCount }}题</span>
                  <span v-if="exam.score !== null">得分: {{ exam.score }}/{{ exam.totalPoints }}</span>
                </div>
              </div>
              <div :class="['task-status', exam.status]">
                {{ getExamStatusText(exam.status) }}
              </div>
            </div>
          </div>

          <div v-else class="no-data">
            <p>{{ examFilter === 'all' ? '暂无考试' : '暂无相关考试' }}</p>
          </div>
        </section>

        <!-- 课程社区模块 -->
        <section v-if="activeModule === 'community'" class="module-section">
          <div class="module-header">
            <h2>课程社区</h2>
            <el-button type="primary" size="small" @click="goToNewPost">
              发布话题
            </el-button>
          </div>

          <div v-if="communityPosts.length > 0" class="community-list">
            <div v-for="post in communityPosts" :key="post.id" class="post-card">
              <div class="post-header">
                <div class="post-author">
                  <span class="avatar">{{ post.author.name[0] }}</span>
                  <div>
                    <p class="author-name">{{ post.author.name }}</p>
                    <p class="post-time">{{ post.createdAt }}</p>
                  </div>
                </div>
              </div>
              <h3 class="post-title">{{ post.title }}</h3>
              <p class="post-content">{{ post.content }}</p>
              <div class="post-footer">
                <span>💬 {{ post.replyCount }} 回复</span>
                <span>👁 {{ post.viewCount }} 浏览</span>
                <el-button type="text" size="small" @click="viewPost(post)">
                  查看详情
                </el-button>
              </div>
            </div>
          </div>

          <div v-else class="no-data">
            <p>暂无讨论</p>
          </div>
        </section>
      </main>
    </div>
  </div>
</template>

<script>
export default {
  name: 'StudentCourseDetail',
  data() {
    return {
      courseId: this.$route.params.id,
      activeModule: 'sections',
      navItems: [
        { id: 'sections', label: '章节', icon: '📚' },
        { id: 'homework', label: '作业', icon: '📝' },
        { id: 'exams', label: '考试', icon: '✍️' },
        { id: 'community', label: '课程社区', icon: '💬' }
      ],
      courseInfo: {
        title: '加载中...',
        instructorName: ''
      },
      sections: [],
      homeworks: [],
      exams: [],
      communityPosts: [],
      // 筛选状态
      homeworkFilter: 'all',
      examFilter: 'all',
      // 章节搜索
      chapterSearch: '',
      expandedSections: []
    }
  },
  created() {
    this.loadCourseData()
  },
  computed: {
    // 筛选作业
    filteredHomeworks() {
      if (this.homeworkFilter === 'all') {
        return this.homeworks
      } else if (this.homeworkFilter === 'completed') {
        return this.homeworks.filter(hw => hw.status === 'submitted' || hw.status === 'graded')
      } else if (this.homeworkFilter === 'incomplete') {
        return this.homeworks.filter(hw => hw.status === 'pending')
      }
      return this.homeworks
    },
    // 筛选考试
    filteredExams() {
      if (this.examFilter === 'all') {
        return this.exams
      } else if (this.examFilter === 'completed') {
        return this.exams.filter(exam => exam.status === 'completed')
      } else if (this.examFilter === 'incomplete') {
        return this.exams.filter(exam => exam.status === 'not_started' || exam.status === 'in_progress')
      }
      return this.exams
    },
    // 搜索章节
    filteredSections() {
      if (!this.chapterSearch) {
        return this.sections
      }
      const keyword = this.chapterSearch.toLowerCase()
      return this.sections.filter(section => {
        const titleMatch = section.title.toLowerCase().includes(keyword)
        const lessonMatch = section.lessons.some(lesson => 
          lesson.name.toLowerCase().includes(keyword)
        )
        return titleMatch || lessonMatch
      })
    }
  },
  methods: {
    goBack() {
      this.$router.push('/course/my-courses')
    },
    
    selectModule(moduleId) {
      this.activeModule = moduleId
    },

    loadCourseData() {
      // TODO: 从 API 加载真实数据
      // 模拟数据
      this.courseInfo = {
        title: 'React 现代实战指南',
        instructorName: '张三'
      }

      this.sections = [
        {
          id: 1,
          title: 'React 基础',
          description: '学习 React 的核心概念',
          lessons: [
            { id: 1, name: 'React 简介', type: 'video', duration: '15:30' },
            { id: 2, name: '组件与 Props', type: 'video', duration: '20:45' },
            { id: 3, name: 'State 与生命周期', type: 'video', duration: '25:10' }
          ]
        },
        {
          id: 2,
          title: 'React Hooks',
          description: 'Hooks 是 React 16.8 的新增特性',
          lessons: [
            { id: 4, name: 'useState 详解', type: 'video', duration: '18:20' },
            { id: 5, name: 'useEffect 使用', type: 'video', duration: '22:15' },
            { id: 6, name: '自定义 Hook', type: 'video', duration: '16:40' }
          ]
        },
        {
          id: 3,
          title: '高级特性',
          description: 'Context、Refs、性能优化等',
          lessons: [
            { id: 7, name: 'Context API', type: 'video', duration: '19:30' },
            { id: 8, name: 'useRef 与 forwardRef', type: 'video', duration: '14:50' },
            { id: 9, name: 'React.memo 性能优化', type: 'video', duration: '21:00' }
          ]
        }
      ]

      // 默认展开第一个章节并选择第一课
      this.expandedSections = [1]
      this.currentLesson = this.sections[0].lessons[0]

      this.homeworks = [
        {
          id: 1,
          title: '第一周练习',
          description: '完成 React 组件练习',
          dueDate: '2024-12-31',
          totalPoints: 100,
          score: null,
          status: 'pending'
        },
        {
          id: 2,
          title: 'Hooks 实践作业',
          description: '使用 Hooks 重构组件',
          dueDate: '2025-01-07',
          totalPoints: 100,
          score: 95,
          status: 'graded'
        }
      ]

      this.exams = [
        {
          id: 1,
          title: 'React 基础测试',
          description: '测试 React 基础知识掌握情况',
          duration: 60,
          questionCount: 20,
          totalPoints: 100,
          score: null,
          status: 'not_started'
        },
        {
          id: 2,
          title: 'Hooks 进阶测试',
          description: '测试 Hooks 高级用法',
          duration: 45,
          questionCount: 15,
          totalPoints: 100,
          score: 88,
          status: 'completed'
        }
      ]

      this.communityPosts = [
        {
          id: 1,
          title: '关于 React Hooks 的疑问',
          content: '使用 useState 时遇到了一些问题...',
          author: { name: '李四' },
          createdAt: '2小时前',
          replyCount: 5,
          viewCount: 120
        }
      ]
    },

    getHomeworkStatusText(status) {
      const map = {
        pending: '待提交',
        submitted: '已提交',
        graded: '已批改'
      }
      return map[status] || status
    },

    getExamStatusText(status) {
      const map = {
        not_started: '未开始',
        in_progress: '进行中',
        completed: '已完成'
      }
      return map[status] || status
    },

    viewLesson(lesson) {
      this.$message.info(`观看课程: ${lesson.name}`)
      // TODO: 跳转到视频播放页面
    },

    submitHomework(homework) {
      this.$message.info(`提交作业: ${homework.title}`)
      // TODO: 跳转到作业提交页面
    },

    viewHomework(homework) {
      this.$message.info(`查看作业: ${homework.title}`)
      // TODO: 跳转到作业详情页面
    },

    startExam(exam) {
      this.$confirm('确定要开始考试吗？考试开始后将开始计时。', '提示', {
        confirmButtonText: '开始',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.$router.push(`/exam/${exam.id}/answer`)
      })
    },

    continueExam(exam) {
      this.$router.push(`/exam/${exam.id}/answer`)
    },

    viewExamResult(exam) {
      this.$router.push(`/exam/${exam.id}/result`)
    },

    goToNewPost() {
      this.$router.push(`/course/${this.courseId}/community/new-post`)
    },

    viewPost(post) {
      this.$router.push(`/community/post/${post.id}`)
    },

    // 章节展开/收起
    toggleSection(sectionId) {
      const index = this.expandedSections.indexOf(sectionId)
      if (index > -1) {
        this.expandedSections.splice(index, 1)
      } else {
        this.expandedSections.push(sectionId)
      }
    },

    // 选择课程，跳转到播放页面
    selectLesson(lesson, section) {
      this.$router.push({
        path: `/course/${this.courseId}/lesson/${lesson.id}`,
        query: {
          sectionId: section.id
        }
      })
    },

    // 考试点击处理
    handleExamClick(exam) {
      if (exam.status === 'not_started') {
        this.startExam(exam)
      } else if (exam.status === 'in_progress') {
        this.continueExam(exam)
      } else if (exam.status === 'completed') {
        this.viewExamResult(exam)
      }
    }
  }
}
</script>

<style scoped>
.student-course-detail {
  width: 100%;
  min-height: 100vh;
  background: #f5f7fa;
}

.page-header {
  background: white;
  padding: 1.5rem 2rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  margin-bottom: 1.5rem;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.course-title h1 {
  margin: 0 0 0.25rem 0;
  font-size: 1.5rem;
  color: #2c3e50;
}

.course-title p {
  margin: 0;
  color: #7f8c8d;
  font-size: 0.9rem;
}

.course-container {
  display: flex;
  gap: 1.5rem;
  padding: 0 2rem;
  max-width: 1400px;
  margin: 0 auto;
}

.sidebar {
  width: 220px;
  flex-shrink: 0;
}

.nav-menu {
  background: white;
  border-radius: 8px;
  padding: 0.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  position: sticky;
  top: 20px;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.875rem 1rem;
  cursor: pointer;
  border-radius: 6px;
  transition: all 0.2s;
  color: #606266;
}

.nav-item:hover {
  background: #f5f7fa;
  color: #409EFF;
}

.nav-item.active {
  background: #ecf5ff;
  color: #409EFF;
  font-weight: 600;
}

.nav-icon {
  font-size: 1.2rem;
}

.content-area {
  flex: 1;
  min-width: 0;
}

.module-section {
  background: white;
  border-radius: 8px;
  padding: 2rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.module-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid #f0f0f0;
}

.module-header h2 {
  margin: 0;
  font-size: 1.5rem;
  color: #2c3e50;
}

/* 章节样式 */
.section-card {
  background: #fafafa;
  border-radius: 8px;
  padding: 1.5rem;
  margin-bottom: 1rem;
}

.section-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 0.75rem;
}

.section-number {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 4px;
  font-size: 0.85rem;
  font-weight: 600;
}

.section-header h3 {
  margin: 0;
  flex: 1;
  font-size: 1.1rem;
}

.lesson-count {
  color: #909399;
  font-size: 0.9rem;
}

.section-desc {
  color: #606266;
  margin: 0 0 1rem 0;
}

.lessons-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.lesson-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem;
  background: white;
  border-radius: 6px;
  transition: all 0.2s;
}

.lesson-item:hover {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.lesson-number {
  background: #e8e8e8;
  color: #606266;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.85rem;
  font-weight: 600;
}

.lesson-info {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.lesson-type {
  font-size: 1.1rem;
}

.lesson-duration {
  color: #909399;
  font-size: 0.85rem;
}

/* 作业样式 */
.homework-list,
.exam-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.homework-card,
.exam-card {
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 1.5rem;
  transition: all 0.2s;
}

.homework-card:hover,
.exam-card:hover {
  border-color: #409EFF;
  box-shadow: 0 4px 12px rgba(64, 158, 255, 0.1);
}

.homework-header,
.exam-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.75rem;
}

.homework-header h3,
.exam-header h3 {
  margin: 0;
  font-size: 1.1rem;
  color: #2c3e50;
}

.status-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.85rem;
  font-weight: 600;
}

.status-badge.pending,
.status-badge.not_started {
  background: #fff3e0;
  color: #e65100;
}

.status-badge.submitted,
.status-badge.in_progress {
  background: #e3f2fd;
  color: #1565c0;
}

.status-badge.graded,
.status-badge.completed {
  background: #e8f5e9;
  color: #2e7d32;
}

.homework-desc,
.exam-desc {
  color: #606266;
  margin: 0 0 1rem 0;
}

.homework-meta,
.exam-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  color: #909399;
  font-size: 0.9rem;
  margin-bottom: 1rem;
}

.homework-actions,
.exam-actions {
  display: flex;
  gap: 0.5rem;
}

/* 社区样式 */
.community-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.post-card {
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 1.5rem;
  transition: all 0.2s;
}

.post-card:hover {
  border-color: #409EFF;
  box-shadow: 0 4px 12px rgba(64, 158, 255, 0.1);
}

.post-header {
  margin-bottom: 1rem;
}

.post-author {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
}

.author-name {
  margin: 0;
  font-weight: 600;
  color: #2c3e50;
}

.post-time {
  margin: 0;
  color: #909399;
  font-size: 0.85rem;
}

.post-title {
  margin: 0 0 0.5rem 0;
  font-size: 1.1rem;
  color: #2c3e50;
}

.post-content {
  color: #606266;
  margin: 0 0 1rem 0;
}

.post-footer {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  color: #909399;
  font-size: 0.9rem;
}

/* 空数据状态 */
.no-data {
  text-align: center;
  padding: 3rem;
  color: #909399;
}

.no-data p {
  margin: 0;
  font-size: 1.1rem;
}

/* 新增：课程标题栏 */
.course-title-bar {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 1.5rem;
  border-radius: 8px 8px 0 0;
  margin-bottom: 0;
}

.course-title-bar h2 {
  margin: 0;
  font-size: 1.3rem;
  font-weight: 600;
}

/* 新增：筛选栏 */
.filter-bar {
  background: white;
  border: 1px solid #e0e0e0;
  border-top: none;
  display: flex;
  padding: 0.5rem 1.5rem;
}

.filter-tab {
  padding: 0.75rem 1.5rem;
  cursor: pointer;
  color: #606266;
  border-bottom: 2px solid transparent;
  transition: all 0.3s;
  font-size: 0.95rem;
}

.filter-tab:hover {
  color: #409EFF;
}

.filter-tab.active {
  color: #409EFF;
  border-bottom-color: #409EFF;
  font-weight: 600;
}

/* 新增：任务列表 */
.task-list {
  padding: 1.5rem;
  background: white;
  border: 1px solid #e0e0e0;
  border-top: none;
  border-radius: 0 0 8px 8px;
}

.task-item {
  display: flex;
  align-items: center;
  padding: 1.25rem;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  margin-bottom: 1rem;
  cursor: pointer;
  transition: all 0.2s;
}

.task-item:last-child {
  margin-bottom: 0;
}

.task-item:hover {
  border-color: #409EFF;
  box-shadow: 0 2px 8px rgba(64, 158, 255, 0.15);
  transform: translateY(-1px);
}

.task-type-badge {
  background: #909399;
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 4px;
  font-size: 0.85rem;
  font-weight: 600;
  margin-right: 1rem;
  min-width: 50px;
  text-align: center;
}

.task-type-badge.exam {
  background: #909399;
}

.task-content {
  flex: 1;
}

.task-title {
  font-size: 1rem;
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 0.5rem;
}

.task-meta {
  display: flex;
  gap: 1.5rem;
  color: #909399;
  font-size: 0.9rem;
}

.task-meta span {
  display: flex;
  align-items: center;
}

.task-status {
  padding: 0.5rem 1rem;
  border-radius: 4px;
  font-size: 0.9rem;
  font-weight: 600;
  margin-left: 1rem;
}

.task-status.pending,
.task-status.not_started {
  background: #fff3e0;
  color: #e65100;
}

.task-status.submitted,
.task-status.in_progress {
  background: #e3f2fd;
  color: #1565c0;
}

.task-status.graded,
.task-status.completed {
  background: #e8f5e9;
  color: #2e7d32;
}

/* 章节概览样式 */
.sections-overview {
  background: white;
  border-radius: 8px;
  padding: 1.5rem;
}

.overview-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.overview-header h2 {
  margin: 0;
  font-size: 1.5rem;
  color: #2c3e50;
}

.sections-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.section-card {
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  overflow: hidden;
  transition: all 0.3s;
}

.section-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.section-card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.25rem 1.5rem;
  background: #f7f8fa;
  cursor: pointer;
  transition: all 0.2s;
}

.section-card-header:hover {
  background: #ebeef5;
}

.section-info {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.expand-icon {
  color: #909399;
  transition: transform 0.3s;
  font-size: 0.8rem;
}

.expand-icon.expanded {
  transform: rotate(90deg);
}

.section-info h3 {
  margin: 0;
  font-size: 1.1rem;
  color: #2c3e50;
  font-weight: 600;
}

.section-meta {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.lesson-count {
  color: #909399;
  font-size: 0.9rem;
}

.section-lessons {
  padding: 0.5rem;
  background: white;
}

.lesson-card {
  display: flex;
  align-items: center;
  padding: 1rem 1.5rem;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s;
  gap: 1rem;
}

.lesson-card:hover {
  background: #f5f7fa;
}

.lesson-index {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  background: #e8eaed;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.9rem;
  font-weight: 600;
  color: #606266;
}

.lesson-icon {
  font-size: 1.3rem;
}

.lesson-content {
  flex: 1;
}

.lesson-name {
  font-size: 1rem;
  color: #2c3e50;
  margin-bottom: 0.25rem;
  font-weight: 500;
}

.lesson-meta {
  color: #909399;
  font-size: 0.85rem;
}

.lesson-action {
  opacity: 0;
  transition: opacity 0.2s;
}

.lesson-card:hover .lesson-action {
  opacity: 1;
}
</style>

