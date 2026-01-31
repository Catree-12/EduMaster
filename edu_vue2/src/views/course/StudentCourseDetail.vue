<template>
  <div class="student-course-detail">
    <!-- 左侧固定导航栏 -->
    <aside class="sidebar-fixed">
      <!-- 课程名称 -->
      <div class="sidebar-logo">
        <h1>{{ courseInfo.name }}</h1>
        <p class="instructor-name">授课教师：{{ courseInfo.instructorName }}</p>
      </div>
      
      <!-- 导航菜单 -->
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
    <div class="main-wrapper">
      <main class="content-area">
        <!-- 章节模块 -->
        <section v-if="activeModule === 'sections'" class="module-section">
          <div class="sections-overview">
            <div class="overview-header">
              <h2>课程章节</h2>
              <div class="header-actions">
                <el-input
                  v-model="chapterSearch"
                  placeholder="搜索章节或课程..."
                  prefix-icon="el-icon-search"
                  clearable
                  style="width: 300px;"
                />
              </div>
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
                  >
                    <div class="lesson-index">{{ index + 1 }}</div>
                    <div class="lesson-icon">
                      {{ lesson.type === 'video' ? '🎥' : '📄' }}
                    </div>
                    <div class="lesson-content" @click="selectLesson(lesson, section)">
                      <div class="lesson-name">{{ lesson.name }}</div>
                      <div class="lesson-meta">
                        <span v-if="lesson.duration">{{ lesson.duration }}</span>
                        <span v-if="lesson.completed" class="completed-badge">✓ 已完成</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <div v-if="filteredSections.length === 0 && sections.length > 0" class="no-data">
              <i class="el-icon-folder-opened" style="font-size: 48px; color: #dcdfe6;"></i>
              <p>未找到相关章节</p>
            </div>
            
            <div v-if="sections.length === 0" class="no-data">
              <i class="el-icon-folder-add" style="font-size: 48px; color: #dcdfe6;"></i>
              <p>暂无章节数据</p>
            </div>
          </div>
        </section>

        <!-- 作业模块 -->
        <section v-if="activeModule === 'homework'" class="module-section">
          <div class="module-header">
            <h2>{{ studentClassName }}</h2>
          </div>

          <!-- 筛选区 -->
          <div class="filter-section">
            <div class="filter-group">
              <label>状态筛选：</label>
              <div class="status-filter-btns">
                <button
                  v-for="status in homeworkStatusOptions"
                  :key="status.value"
                  :class="['filter-btn', { active: homeworkFilter === status.value }]"
                  @click="homeworkFilter = status.value"
                >
                  {{ status.label }}
                </button>
              </div>
            </div>
          </div>

          <!-- 列表区 -->
          <div v-if="filteredHomeworks.length > 0" class="list-section">
            <div v-for="hw in filteredHomeworks" :key="hw.id" class="homework-item-card">
              <!-- 顶部区域 -->
              <div class="card-top-section">
                <!-- 左侧：标题和状态 -->
                <div class="card-header">
                  <h3 class="task-title clickable-title" @click="viewHomeworkDetail(hw)">{{ hw.name }}</h3>
                  <span :class="['status-capsule', hw.status]">{{ hw.status }}</span>
                </div>
                
                <!-- 右侧：成绩展示 -->
                <div class="stats-inline" v-if="hw.score !== null">
                  <div class="stat-item">
                    <div class="stat-label">我的得分</div>
                    <div class="stat-number">{{ hw.score }} / {{ hw.totalScore }}</div>
                  </div>
                </div>
              </div>

              <!-- 中部区域：信息行 -->
              <div class="card-middle-section">
                <div class="info-item">
                  <span class="info-label">发布时间：</span>
                  <span class="info-value">{{ hw.startTime }}</span>
                </div>
                <div class="info-item">
                  <span class="info-label">截止时间：</span>
                  <span class="info-value">{{ hw.endTime }}</span>
                </div>
                <div class="info-item" v-if="hw.submitTime">
                  <span class="info-label">提交时间：</span>
                  <span class="info-value">{{ hw.submitTime }}</span>
                </div>
              </div>

              <!-- 底部区域：操作按钮 -->
              <div class="card-bottom-section">
                <el-button 
                  v-if="hw.status === '未完成'"
                  type="primary" 
                  size="large" 
                  class="primary-action-btn"
                  @click.stop="startHomework(hw)"
                >
                  开始作答
                </el-button>
                <el-button 
                  v-else
                  type="info" 
                  size="large" 
                  class="primary-action-btn"
                  @click.stop="viewHomeworkResult(hw)"
                >
                  查看详情
                </el-button>
              </div>
            </div>
          </div>

          <div v-else class="no-data">
            <p>暂无作业数据</p>
          </div>
        </section>

        <!-- 考试模块 -->
        <section v-if="activeModule === 'exam'" class="module-section">
          <div class="module-header">
            <h2>考试管理</h2>
          </div>

          <!-- 筛选区 -->
          <div class="filter-section">
            <div class="filter-group">
              <label>状态筛选：</label>
              <div class="status-filter-btns">
                <button
                  v-for="status in examStatusOptions"
                  :key="status.value"
                  :class="['filter-btn', { active: examFilter === status.value }]"
                  @click="examFilter = status.value"
                >
                  {{ status.label }}
                </button>
              </div>
            </div>
          </div>

          <!-- 列表区 -->
          <div v-if="filteredExams.length > 0" class="list-section">
            <div v-for="exam in filteredExams" :key="exam.id" class="exam-item-card">
              <!-- 顶部区域：标题 + 状态 + 统计 -->
              <div class="card-top-section">
                <div class="card-header">
                  <h3 class="task-title clickable-title" @click="viewExamDetail(exam)">{{ exam.name }}</h3>
                  <span :class="['status-capsule', exam.status]">{{ exam.status }}</span>
                </div>
                
                <!-- 右侧：成绩展示 -->
                <div class="stats-inline" v-if="exam.score !== null">
                  <div class="stat-item">
                    <div class="stat-label">我的得分</div>
                    <div class="stat-number">{{ exam.score }} / {{ exam.totalScore }}</div>
                  </div>
                </div>
              </div>

              <!-- 中部区域：信息行 -->
              <div class="card-middle-section">
                <div class="info-item">
                  <span class="info-label">考试时长：</span>
                  <span class="info-value">{{ exam.duration }}分钟</span>
                </div>
                <div class="info-item">
                  <span class="info-label">题目数量：</span>
                  <span class="info-value">{{ exam.questionCount }}题</span>
                </div>
                <div class="info-item">
                  <span class="info-label">考试时间：</span>
                  <span class="info-value">{{ exam.startTime }} ~ {{ exam.endTime }}</span>
                </div>
              </div>

              <!-- 底部区域：操作按钮 -->
              <div class="card-bottom-section">
                <el-button 
                  v-if="exam.status === '未开始' || exam.status === '进行中'"
                  type="primary" 
                  size="large" 
                  class="primary-action-btn"
                  @click.stop="startExam(exam)"
                  :disabled="exam.status === '未开始'"
                >
                  {{ exam.status === '未开始' ? '等待开始' : '进入考试' }}
                </el-button>
                <el-button 
                  v-else
                  type="info" 
                  size="large" 
                  class="primary-action-btn"
                  @click.stop="viewExamResult(exam)"
                >
                  查看成绩
                </el-button>
              </div>
            </div>
          </div>

          <div v-else class="no-data">
            <p>暂无考试数据</p>
          </div>
        </section>

        <!-- 课程社区模块 -->
        <section v-if="activeModule === 'discussion'" class="module-section community-module">
          <div class="community-layout">
            <!-- 左侧：话题列表区域 -->
            <div class="community-main">
              <!-- 1. 顶部操作区 -->
              <div class="community-top-bar">
                <input 
                  v-model="communitySearch"
                  type="text"
                  placeholder="搜索话题标题或内容..."
                  class="community-search-input"
                >
                <button @click="createNewThread" class="community-publish-btn">
                  ➕ 发布话题
                </button>
              </div>

              <!-- 2. 筛选与排序条 -->
              <div class="community-filter-bar">
                <div class="sort-tabs">
                  <button
                    v-for="sort in ['最新', '热门']"
                    :key="sort"
                    :class="['sort-tab', { active: communitySortBy === sort }]"
                    @click="communitySortBy = sort"
                  >
                    {{ sort }}
                  </button>
                </div>
              </div>

              <!-- 3. 话题列表容器 -->
              <div v-if="filteredCommunityThreads.length > 0" class="community-thread-list">
                <div v-for="thread in filteredCommunityThreads" :key="thread.id" class="thread-card">
                  <!-- 标题层 -->
                  <div class="thread-title-row">
                    <h3 class="thread-title" @click="viewThreadDetail(thread.id)">{{ thread.title }}</h3>
                    <div class="thread-badges">
                      <span v-if="thread.authorRole === 'teacher'" class="badge-role teacher">老师</span>
                      <span v-if="thread.authorRole === 'student'" class="badge-role student">学生</span>
                      <span v-if="thread.essence" class="badge-tag essence">精选</span>
                    </div>
                  </div>

                  <!-- 摘要层 -->
                  <div class="thread-preview">
                    <p class="thread-excerpt">{{ getThreadExcerpt(thread.content) }}</p>
                  </div>

                  <!-- 元数据层 -->
                  <div class="thread-meta-row">
                    <div class="thread-info">
                      <span class="author-name">{{ thread.author }}</span>
                      <span class="separator">·</span>
                      <span class="publish-time">{{ thread.createTime }}</span>
                    </div>
                    <div class="thread-stats">
                      <span class="stat-item">
                        <i class="icon-view">👁</i>
                        {{ thread.viewCount }}
                      </span>
                      <span class="stat-item clickable" @click.stop="viewThreadDetail(thread.id)">
                        <i class="icon-reply">💬</i>
                        {{ thread.replyCount }}
                      </span>
                      <button :class="['like-btn-list', { liked: thread.isLiked }]" @click.stop="toggleThreadLike(thread)">
                        {{ thread.isLiked ? '❤️' : '🤍' }}
                        {{ thread.likeCount }}
                      </button>
                      <!-- 仅自己的帖子可以编辑/删除 -->
                      <div v-if="canEditThread(thread)" class="thread-manage">
                        <a class="manage-link edit" @click.stop="editThread(thread.id)">编辑</a>
                        <a class="manage-link delete" @click.stop="deleteThread(thread.id)">删除</a>
                      </div>
                      <!-- 老师可以删除其他人的帖子 -->
                      <div v-else-if="canDeleteThread(thread)" class="thread-manage">
                        <a class="manage-link delete" @click.stop="deleteThread(thread.id)">删除</a>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <div v-else class="no-data">
                <p>暂无话题</p>
                <p class="hint">点击"发布话题"按钮创建第一个讨论</p>
              </div>
            </div>

            <!-- 右侧：分类目录 -->
            <aside class="community-sidebar">
              <div class="sidebar-section">
                <h3 class="sidebar-title">我的（讨论）</h3>
                <div class="category-list">
                  <div 
                    v-for="category in myCategories" 
                    :key="category.id"
                    :class="['category-item', { active: communityCategory === category.id }]"
                    @click="selectCategory(category.id)"
                  >
                    <span class="category-icon">{{ category.icon }}</span>
                    <span class="category-label">{{ category.label }}</span>
                  </div>
                </div>
              </div>
            </aside>
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
      
      // 导航菜单项
      navItems: [
        { id: 'sections', label: '章节', icon: '📚' },
        { id: 'homework', label: '作业', icon: '📝' },
        { id: 'exam', label: '考试', icon: '✍️' },
        { id: 'discussion', label: '课程社区', icon: '💬' }
      ],
      
      // 课程信息
      courseInfo: {
        name: 'Web前端开发实战',
        instructorName: '张老师'
      },
      
      // 学生班级信息
      studentClassName: '2024级计算机科学1班',
      
      // 章节数据
      sections: [],
      expandedSections: [],
      chapterSearch: '',
      
      // 作业数据
      homeworks: [],
      homeworkFilter: '全部',
      homeworkStatusOptions: [
        { value: '全部', label: '全部' },
        { value: '已完成', label: '已完成' },
        { value: '未完成', label: '未完成' }
      ],
      
      // 考试数据
      exams: [],
      examFilter: '全部',
      examStatusOptions: [
        { value: '全部', label: '全部' },
        { value: '未开始', label: '未开始' },
        { value: '进行中', label: '进行中' },
        { value: '已完成', label: '已完成' }
      ],
      
      // 社区数据
      communityThreads: [],
      communitySearch: '',
      communitySortBy: '最新',
      showMyThreadsOnly: false,
      currentUserId: 1, // 当前学生用户ID
      currentUserRole: 'student', // 当前用户角色
      communityCategory: 'all', // 当前选中的分类
      
      // 社区分类目录
      myCategories: [
        { id: 'all', label: '全部', icon: '📋' },
        { id: 'my-published', label: '我发布的', icon: '✏️' }
      ]
    }
  },
  
  computed: {
    // 筛选章节
    filteredSections() {
      if (!this.chapterSearch) return this.sections
      const keyword = this.chapterSearch.toLowerCase()
      return this.sections.filter(section => {
        const titleMatch = section.title.toLowerCase().includes(keyword)
        const lessonMatch = section.lessons.some(lesson => 
          lesson.name.toLowerCase().includes(keyword)
        )
        return titleMatch || lessonMatch
      })
    },
    
    // 筛选作业
    filteredHomeworks() {
      if (this.homeworkFilter === '全部') {
        return this.homeworks
      }
      return this.homeworks.filter(hw => hw.status === this.homeworkFilter)
    },
    
    // 筛选考试
    filteredExams() {
      if (this.examFilter === '全部') {
        return this.exams
      }
      return this.exams.filter(exam => exam.status === this.examFilter)
    },
    
    // 筛选社区话题
    filteredCommunityThreads() {
      let result = this.communityThreads
      
      // 分类过滤
      if (this.communityCategory === 'my-published') {
        result = result.filter(thread => thread.isMyPost)
      }
      
      // 搜索过滤
      if (this.communitySearch) {
        const keyword = this.communitySearch.toLowerCase()
        result = result.filter(thread => 
          thread.title.toLowerCase().includes(keyword) ||
          thread.content.toLowerCase().includes(keyword)
        )
      }
      
      // 排序
      if (this.communitySortBy === '最新') {
        result = [...result].sort((a, b) => new Date(b.createTime) - new Date(a.createTime))
      } else if (this.communitySortBy === '热门') {
        result = [...result].sort((a, b) => (b.viewCount + b.replyCount + b.likeCount) - (a.viewCount + a.replyCount + a.likeCount))
      }
      
      return result
    }
  },
  
  created() {
    // 根据路由参数初始化activeModule
    const tab = this.$route.query.tab
    if (tab) {
      const validTabs = this.navItems.map(item => item.id)
      if (validTabs.includes(tab)) {
        this.activeModule = tab
      }
    }
    this.loadCourseData()
  },
  
  methods: {
    // 选择模块
    selectModule(moduleId) {
      this.activeModule = moduleId
      
      // 更新URL参数
      this.$router.replace({
        name: 'StudentCourseDetail',
        params: { id: this.$route.params.id },
        query: { tab: moduleId }
      }).catch(err => {
        // 忽略重复导航错误
        if (err.name !== 'NavigationDuplicated') {
          console.error(err)
        }
      })
    },
    
    // 加载课程数据
    loadCourseData() {
      // 加载章节数据
      this.sections = [
        {
          id: 1,
          title: '第一章：HTML基础',
          lessons: [
            { id: 101, name: 'HTML简介', type: 'video', duration: '15分钟', completed: true },
            { id: 102, name: 'HTML标签详解', type: 'video', duration: '25分钟', completed: true },
            { id: 103, name: 'HTML表单', type: 'document', duration: '10分钟', completed: false }
          ]
        },
        {
          id: 2,
          title: '第二章：CSS样式',
          lessons: [
            { id: 201, name: 'CSS选择器', type: 'video', duration: '20分钟', completed: false },
            { id: 202, name: 'CSS布局', type: 'video', duration: '30分钟', completed: false }
          ]
        }
      ]
      
      // 加载作业数据
      this.homeworks = [
        {
          id: 1,
          name: 'HTML基础练习',
          status: '已完成',
          startTime: '2024-01-20 09:00',
          endTime: '2024-01-27 23:59',
          submitTime: '2024-01-25 18:30',
          score: 85,
          totalScore: 100
        },
        {
          id: 2,
          name: 'CSS布局作业',
          status: '未完成',
          startTime: '2024-01-22 09:00',
          endTime: '2024-01-29 23:59',
          submitTime: null,
          score: null,
          totalScore: 100
        }
      ]
      
      // 加载考试数据
      this.exams = [
        {
          id: 1,
          name: '期中考试',
          status: '已完成',
          startTime: '2024-01-20 14:00',
          endTime: '2024-01-20 16:00',
          duration: 120,
          questionCount: 50,
          score: 92,
          totalScore: 100
        },
        {
          id: 2,
          name: '期末考试',
          status: '未开始',
          startTime: '2024-02-15 14:00',
          endTime: '2024-02-15 16:30',
          duration: 150,
          questionCount: 60,
          score: null,
          totalScore: 100
        }
      ]
      
      // 加载社区话题数据
      this.communityThreads = [
        {
          id: 1,
          title: '关于CSS Grid布局的疑问',
          content: '在学习CSS Grid的时候遇到了一些问题，想请教一下大家...',
          author: '李同学',
          authorId: 1, // 作者ID（当前用户）
          authorRole: 'student',
          createTime: '2024-01-24 10:30',
          viewCount: 156,
          replyCount: 12,
          likeCount: 8,
          isLiked: false,
          essence: false,
          isMyPost: true,
          hasMyReply: true,
          hasReplyToMe: true
        },
        {
          id: 2,
          title: '第二章重点知识总结',
          content: '整理了第二章的重点知识，分享给大家参考...',
          author: '张老师',
          authorId: 100, // 老师ID
          authorRole: 'teacher',
          createTime: '2024-01-23 15:20',
          viewCount: 289,
          replyCount: 23,
          likeCount: 45,
          isLiked: true,
          essence: true,
          isMyPost: false,
          hasMyReply: true,
          hasReplyToMe: false
        },
        {
          id: 3,
          title: 'Flexbox和Grid该如何选择？',
          content: '在实际项目中，Flexbox和Grid各有什么优势，应该如何选择？',
          author: '王同学',
          authorId: 2, // 其他学生ID
          authorRole: 'student',
          createTime: '2024-01-22 09:15',
          viewCount: 203,
          replyCount: 18,
          likeCount: 15,
          isLiked: false,
          essence: false,
          isMyPost: false,
          hasMyReply: false,
          hasReplyToMe: true
        },
        {
          id: 4,
          title: 'JavaScript异步编程最佳实践',
          content: '分享一些JavaScript异步编程的经验和技巧...',
          author: '赵同学',
          authorId: 3, // 其他学生ID
          authorRole: 'student',
          createTime: '2024-01-21 14:00',
          viewCount: 178,
          replyCount: 15,
          likeCount: 20,
          isLiked: false,
          essence: false,
          isMyPost: false,
          hasMyReply: false,
          hasReplyToMe: false
        }
      ]
    },
    
    // 章节相关方法
    toggleSection(sectionId) {
      const index = this.expandedSections.indexOf(sectionId)
      if (index > -1) {
        this.expandedSections.splice(index, 1)
      } else {
        this.expandedSections.push(sectionId)
      }
    },
    
    selectLesson(lesson, section) {
      // 跳转到学生课程播放页面
      this.$router.push({
        path: `/student/course/${this.courseId}/lesson/${lesson.id}`,
        query: {
          sectionId: section.id
        }
      })
    },
    
    // 作业相关方法
    viewHomeworkDetail(homework) {
      this.$router.push({
        path: `/student/course/${this.courseId}/homework/${homework.id}`
      })
    },
    
    startHomework(homework) {
      this.$router.push({
        path: `/student/course/${this.courseId}/homework/${homework.id}`
      })
    },
    
    viewHomeworkResult(homework) {
      this.$router.push({
        path: `/student/course/${this.courseId}/homework/${homework.id}`
      })
    },
    
    // 考试相关方法
    viewExamDetail(exam) {
      this.$router.push({
        path: `/student/course/${this.courseId}/exam/${exam.id}`
      })
    },
    
    startExam(exam) {
      if (exam.status === '未开始') {
        this.$message.warning('考试尚未开始')
        return
      }
      this.$router.push({
        path: `/student/course/${this.courseId}/exam/${exam.id}`
      })
    },
    
    viewExamResult(exam) {
      this.$router.push({
        path: `/student/course/${this.courseId}/exam/${exam.id}`
      })
    },
    
    // 社区相关方法
    createNewThread() {
      this.$router.push({
        path: `/student/course/${this.courseId}/thread/create`
      })
    },
    
    viewThreadDetail(threadId) {
      this.$router.push({
        path: `/student/course/${this.courseId}/thread/${threadId}`
      })
    },
    
    getThreadExcerpt(content) {
      return content.length > 100 ? content.substring(0, 100) + '...' : content
    },
    
    toggleThreadLike(thread) {
      thread.isLiked = !thread.isLiked
      thread.likeCount += thread.isLiked ? 1 : -1
      this.$message.success(thread.isLiked ? '已点赞' : '已取消点赞')
    },
    
    editThread(threadId) {
      this.$router.push({
        path: `/student/course/${this.courseId}/thread/${threadId}/edit`
      })
    },
    
    deleteThread(threadId) {
      this.$confirm('确定要删除这个话题吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        const index = this.communityThreads.findIndex(t => t.id === threadId)
        if (index > -1) {
          this.communityThreads.splice(index, 1)
          this.$message.success('话题已删除')
        }
      }).catch(() => {})
    },
    
    // 分类选择
    selectCategory(categoryId) {
      this.communityCategory = categoryId
    },
    
    // 权限判断
    canEditThread(thread) {
      // 只能编辑自己的帖子
      return thread.isMyPost
    },
    
    canDeleteThread() {
      // 老师可以删除他人的帖子，但不能编辑
      // 学生只能删除自己的
      // 这里假设学生角色，所以返回false
      return false
    }
  }
}
</script>

<style scoped>
/* 整体布局 */
.student-course-detail {
  display: flex;
  min-height: 100vh;
  background: #f9fafb;
}

/* 左侧固定导航栏 */
.sidebar-fixed {
  width: 220px;
  background: white;
  border-right: 1px solid #e5e7eb;
  position: fixed;
  left: 0;
  top: 0;
  height: 100vh;
  overflow-y: auto;
  z-index: 99;
  display: flex;
  flex-direction: column;
}

.sidebar-logo {
  padding: 1.5rem;
  border-bottom: 1px solid #e5e7eb;
  text-align: center;
}

.sidebar-logo h1 {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 700;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.instructor-name {
  margin: 0.5rem 0 0 0;
  font-size: 0.875rem;
  color: #6b7280;
}

.nav-menu {
  display: flex;
  flex-direction: column;
  gap: 0;
  padding: 1.5rem 0.75rem;
  flex: 1;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.875rem 1rem;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
  color: #6b7280;
  font-weight: 500;
  user-select: none;
  -webkit-user-select: none;
  margin-bottom: 0.25rem;
}

.nav-item:hover {
  background-color: #f3f4f6;
  color: #374151;
}

.nav-item.active {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
}

.nav-icon {
  font-size: 1.2rem;
}

.nav-label {
  font-size: 0.95rem;
}

/* 右侧主内容区 */
.main-wrapper {
  flex: 1;
  margin-left: 220px;
  padding: 0;
  overflow-x: hidden;
}

/* 右侧内容区 */
.content-area {
  background: white;
  min-height: 100vh;
  width: 100%;
  overflow-x: hidden;
}

.module-section {
  padding: 20px;
  animation: fadeIn 0.3s ease-in;
  min-height: 100vh;
  width: 100%;
  box-sizing: border-box;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.module-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0;
  gap: 1rem;
  padding: 1.5rem 2rem;
  background: #f9fafb;
  border-bottom: 1px solid #e5e7eb;
}

.module-header h2 {
  margin: 0;
  color: #2c3e50;
  font-size: 1.3rem;
  font-weight: 700;
}

/* 章节模块样式 */
.sections-overview {
  width: 100%;
}

.overview-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.overview-header h2 {
  font-size: 1.5rem;
  color: #1f2937;
  margin: 0;
}

.header-actions {
  display: flex;
  gap: 1rem;
}

.sections-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.section-card {
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  overflow: hidden;
  transition: all 0.2s;
}

.section-card:hover {
  box-shadow: 0 4px 6px rgba(0,0,0,0.05);
}

.section-card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.25rem 1.5rem;
  background: #f9fafb;
  cursor: pointer;
  transition: background 0.2s;
}

.section-card-header:hover {
  background: #f3f4f6;
}

.section-info {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.expand-icon {
  font-size: 0.75rem;
  color: #6b7280;
  transition: transform 0.2s;
}

.expand-icon.expanded {
  transform: rotate(90deg);
}

.section-info h3 {
  font-size: 1.125rem;
  color: #1f2937;
  margin: 0;
  font-weight: 600;
}

.section-meta {
  display: flex;
  gap: 1.5rem;
  color: #6b7280;
  font-size: 0.875rem;
}

.lesson-count {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.section-lessons {
  border-top: 1px solid #e5e7eb;
}

.lesson-card {
  display: flex;
  align-items: center;
  padding: 1rem 1.5rem;
  border-bottom: 1px solid #f3f4f6;
  cursor: pointer;
  transition: background 0.2s;
}

.lesson-card:last-child {
  border-bottom: none;
}

.lesson-card:hover {
  background: #f9fafb;
}

.lesson-index {
  width: 32px;
  height: 32px;
  background: #e5e7eb;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.875rem;
  font-weight: 600;
  color: #6b7280;
  margin-right: 1rem;
}

.lesson-icon {
  font-size: 1.5rem;
  margin-right: 1rem;
}

.lesson-content {
  flex: 1;
}

.lesson-name {
  font-size: 1rem;
  color: #1f2937;
  margin-bottom: 0.25rem;
  font-weight: 500;
}

.lesson-meta {
  display: flex;
  gap: 1rem;
  font-size: 0.875rem;
  color: #6b7280;
}

.completed-badge {
  color: #10b981;
  font-weight: 600;
}

/* 筛选区域样式 */
.filter-section {
  margin-bottom: 2rem;
  padding: 1.5rem;
  background: #f9fafb;
  border-radius: 8px;
  display: flex;
  flex-wrap: wrap;
  gap: 1.5rem;
}

.filter-group {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.filter-group label {
  font-size: 0.9375rem;
  color: #4b5563;
  font-weight: 500;
  white-space: nowrap;
}

.status-filter-btns {
  display: flex;
  gap: 0.5rem;
}

.filter-btn {
  padding: 0.5rem 1rem;
  border: 1px solid #d1d5db;
  background: white;
  color: #6b7280;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s;
  font-size: 0.875rem;
}

.filter-btn:hover {
  border-color: #667eea;
  color: #667eea;
}

.filter-btn.active {
  background: #667eea;
  color: white;
  border-color: #667eea;
}

/* 列表区域样式 */
.list-section {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.homework-item-card,
.exam-item-card {
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 1.5rem;
  transition: all 0.2s;
  background: white;
}

.homework-item-card:hover,
.exam-item-card:hover {
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
  border-color: #d1d5db;
}

.card-top-section {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1rem;
}

.card-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  flex: 1;
}

.task-title {
  font-size: 1.125rem;
  color: #1f2937;
  margin: 0;
  font-weight: 600;
}

.clickable-title {
  cursor: pointer;
  transition: color 0.2s;
}

.clickable-title:hover {
  color: #667eea;
}

.status-capsule {
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.8125rem;
  font-weight: 500;
  white-space: nowrap;
}

.status-capsule.未完成 {
  background: #fef3c7;
  color: #f59e0b;
}

.status-capsule.已完成 {
  background: #d1fae5;
  color: #10b981;
}

.status-capsule.未开始 {
  background: #f3f4f6;
  color: #6b7280;
}

.stats-inline {
  display: flex;
  gap: 2rem;
  align-items: center;
}

.stat-item {
  text-align: center;
}

.stat-label {
  font-size: 0.875rem;
  color: #6b7280;
  margin-bottom: 0.25rem;
}

.stat-number {
  font-size: 1.25rem;
  font-weight: 700;
  color: #667eea;
}

.card-middle-section {
  display: flex;
  gap: 2rem;
  padding: 1rem 0;
  border-top: 1px solid #f3f4f6;
  border-bottom: 1px solid #f3f4f6;
  margin-bottom: 1rem;
}

.info-item {
  display: flex;
  gap: 0.5rem;
  font-size: 0.9375rem;
}

.info-label {
  color: #6b7280;
}

.info-value {
  color: #1f2937;
  font-weight: 500;
}

.card-bottom-section {
  display: flex;
  justify-content: flex-start;
  align-items: center;
}

.primary-action-btn {
  padding: 0.75rem 2rem !important;
  font-size: 1rem !important;
}

/* 社区模块样式 */
.community-module {
  padding: 0;
}

.community-layout {
  display: flex;
  gap: 1.5rem;
  padding: 0;
}

.community-main {
  flex: 1;
  min-width: 0;
}

.community-sidebar {
  width: 280px;
  flex-shrink: 0;
}

.community-top-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem 2rem;
  border-bottom: 1px solid #e5e7eb;
  background: #f9fafb;
}

.community-search-input {
  flex: 1;
  max-width: 400px;
  padding: 0.625rem 1rem;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 0.9375rem;
  transition: all 0.2s;
}

.community-search-input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.community-publish-btn {
  padding: 0.65rem 1.25rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.3s;
  font-weight: 600;
}

.community-publish-btn:hover {
  opacity: 0.9;
  transform: translateY(-2px);
}

.community-filter-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 2rem;
  background: #f9fafb;
  border-bottom: 1px solid #e5e7eb;
}

.sort-tabs {
  display: flex;
  gap: 0.5rem;
}

.sort-tab {
  padding: 0.5rem 1rem;
  background: transparent;
  border: none;
  color: #6b7280;
  cursor: pointer;
  border-radius: 6px;
  transition: all 0.2s;
  font-size: 0.9375rem;
}

.sort-tab:hover {
  background: white;
  color: #1f2937;
}

.sort-tab.active {
  background: white;
  color: #667eea;
  font-weight: 600;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

.personal-filter {
  display: flex;
  align-items: center;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  font-size: 0.9375rem;
  color: #4b5563;
}

.filter-checkbox {
  width: 16px;
  height: 16px;
  cursor: pointer;
}

.community-thread-list {
  padding: 1.5rem 2rem;
}

.thread-card {
  padding: 1.5rem;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  margin-bottom: 1rem;
  background: white;
  transition: all 0.2s;
}

.thread-card:hover {
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
  border-color: #d1d5db;
}

.thread-title-row {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 0.75rem;
}

.thread-title {
  font-size: 1.125rem;
  color: #1f2937;
  margin: 0;
  cursor: pointer;
  transition: color 0.2s;
  font-weight: 600;
  flex: 1;
}

.thread-title:hover {
  color: #667eea;
}

.thread-badges {
  display: flex;
  gap: 0.5rem;
  margin-left: 1rem;
}

.badge-role {
  padding: 0.125rem 0.5rem;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 500;
}

.badge-role.teacher {
  background: #fef3c7;
  color: #f59e0b;
}

.badge-role.student {
  background: #dbeafe;
  color: #3b82f6;
}

.badge-tag.essence {
  background: #fce7f3;
  color: #ec4899;
  padding: 0.125rem 0.5rem;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 500;
}

.thread-preview {
  margin-bottom: 1rem;
}

.thread-excerpt {
  color: #6b7280;
  font-size: 0.9375rem;
  line-height: 1.6;
  margin: 0;
}

.thread-meta-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 0.75rem;
  border-top: 1px solid #f3f4f6;
}

.thread-info {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  color: #6b7280;
}

.author-name {
  font-weight: 500;
  color: #4b5563;
}

.separator {
  color: #d1d5db;
}

.publish-time {
  color: #9ca3af;
}

.thread-stats {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  font-size: 0.875rem;
  color: #6b7280;
}

.stat-item.clickable {
  cursor: pointer;
  transition: color 0.2s;
}

.stat-item.clickable:hover {
  color: #667eea;
}

.icon-view,
.icon-reply {
  font-size: 1rem;
}

.like-btn-list {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  padding: 0.25rem 0.75rem;
  border: 1px solid #e5e7eb;
  background: white;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s;
  font-size: 0.875rem;
}

.like-btn-list:hover {
  border-color: #667eea;
  background: #f5f7ff;
}

.like-btn-list.liked {
  border-color: #ec4899;
  background: #fdf2f8;
  color: #ec4899;
}

.thread-manage {
  display: flex;
  gap: 1rem;
}

.manage-link {
  font-size: 0.875rem;
  cursor: pointer;
  transition: color 0.2s;
}

.manage-link.edit {
  color: #667eea;
}

.manage-link.edit:hover {
  color: #5568d3;
  text-decoration: underline;
}

.manage-link.delete {
  color: #ef4444;
}

.manage-link.delete:hover {
  color: #dc2626;
  text-decoration: underline;
}

/* 空状态样式 */
.no-data {
  text-align: center;
  padding: 4rem 2rem;
  color: #9ca3af;
}

.no-data p {
  margin: 1rem 0 0.5rem;
  font-size: 1rem;
}

.no-data .hint {
  font-size: 0.875rem;
  color: #d1d5db;
}

/* 社区右侧边栏样式 */
.sidebar-section {
  background: white;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  position: sticky;
  top: 1.5rem;
}

.sidebar-title {
  font-size: 1rem;
  font-weight: 600;
  color: #1f2937;
  margin: 0 0 1rem 0;
  padding-bottom: 0.75rem;
  border-bottom: 2px solid #f3f4f6;
}

.category-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.category-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1rem;
  border-radius: 6px;
  background: #f9fafb;
  cursor: pointer;
  transition: all 0.2s;
  border: 2px solid transparent;
}

.category-item:hover {
  background: #f3f4f6;
  border-color: #e5e7eb;
}

.category-item.active {
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
  border-color: #667eea;
}

.category-item.active .category-icon {
  filter: grayscale(0);
}

.category-item.active .category-label {
  color: #667eea;
  font-weight: 600;
}

.category-icon {
  font-size: 1.25rem;
  flex-shrink: 0;
  filter: grayscale(0.3);
  transition: filter 0.2s;
}

.category-label {
  font-size: 0.9375rem;
  color: #4b5563;
  transition: all 0.2s;
}

/* 响应式调整 */
@media (max-width: 1024px) {
  .sidebar-fixed {
    width: 200px;
  }
  
  .main-wrapper {
    margin-left: 200px;
  }
  
  .community-sidebar {
    width: 240px;
  }
}

@media (max-width: 768px) {
  .sidebar-fixed {
    width: 180px;
  }
  
  .community-layout {
    flex-direction: column;
  }
  
  .community-sidebar {
    width: 100%;
    order: -1;
  }
  
  .sidebar-section {
    position: static;
  }
  
  .main-wrapper {
    margin-left: 180px;
  }
  
  .content-area {
    padding: 1rem;
  }
}
</style>
