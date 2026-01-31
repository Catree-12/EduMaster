<template>
  <div class="lesson-player">
    <!-- 页面头部 -->
    <div class="page-header">
      <div class="header-left">
        <el-button icon="el-icon-arrow-left" @click="goBack">返回课程</el-button>
        <div class="course-title">
          <h1>{{ courseInfo.title }}</h1>
        </div>
      </div>
    </div>

    <!-- 主体内容 -->
    <div class="player-container">
      <!-- 左侧:内容播放区 -->
      <div class="content-player">
        <!-- 视频/文档播放器 -->
        <div v-if="currentLesson" class="player-wrapper">
          <div v-if="currentLesson.type === 'video'" class="video-player">
            <div class="video-placeholder">
              <div class="play-icon">▶</div>
              <p class="video-tip">视频播放器占位区</p>
              <p class="video-info">{{ currentLesson.name }}</p>
            </div>
          </div>
          <div v-else class="document-viewer">
            <div class="doc-placeholder">
              <i class="el-icon-document" style="font-size: 64px; color: #909399;"></i>
              <p>文档查看器占位区</p>
              <p class="doc-name">{{ currentLesson.name }}</p>
            </div>
          </div>

          <!-- 课程信息 -->
          <div class="lesson-info">
            <div class="lesson-header">
              <div class="lesson-actions">
                <el-button 
                  :disabled="!previousLesson" 
                  @click="goToLesson(previousLesson)"
                  size="small"
                >
                  <i class="el-icon-arrow-left"></i> 上一课
                </el-button>
                <el-button 
                  :disabled="!nextLesson" 
                  @click="goToLesson(nextLesson)"
                  size="small"
                  type="primary"
                >
                  下一课 <i class="el-icon-arrow-right"></i>
                </el-button>
              </div>
            </div>
          </div>
        </div>

        <!-- 加载状态 -->
        <div v-else class="loading-state">
          <i class="el-icon-loading" style="font-size: 48px; color: #409EFF;"></i>
          <p>加载中...</p>
        </div>
      </div>

      <!-- 右侧：章节目录 -->
      <div class="chapter-catalog">
        <div class="catalog-header">
          <h3>课程目录</h3>
          <el-input
            v-model="chapterSearch"
            placeholder="搜索章节..."
            prefix-icon="el-icon-search"
            size="small"
            clearable
          />
        </div>

        <div class="catalog-list" style="min-height: 1500px;">
          <div
            v-for="section in filteredSections"
            :key="section.id"
            class="section-item"
          >
            <div
              class="section-header"
              @click="toggleSection(section.id)"
            >
              <span :class="['expand-icon', { expanded: expandedSections.includes(section.id) }]">▶</span>
              <span class="section-title">{{ section.title }}</span>
              <span class="lesson-count">({{ section.lessons.length }})</span>
            </div>

            <div
              v-show="expandedSections.includes(section.id)"
              class="lessons-list"
            >
              <div
                v-for="(lesson, index) in section.lessons"
                :key="lesson.id"
                :class="['lesson-item', { active: currentLesson && currentLesson.id === lesson.id, completed: lesson.completed }]"
                @click="selectLesson(lesson, section)"
              >
                <span class="lesson-number">{{ index + 1 }}</span>
                <span class="lesson-type-icon">{{ lesson.type === 'video' ? '🎥' : '📄' }}</span>
                <span class="lesson-name">{{ lesson.name }}</span>
                <span v-if="lesson.completed" class="completed-icon">✓</span>
                <span v-else class="lesson-duration">{{ lesson.duration }}</span>
              </div>
            </div>
          </div>
          <!-- 临时：测试滚动 -->
          <div style="height: 1000px; padding: 20px; background: linear-gradient(to bottom, transparent, #f0f0f0);">
            <p style="color: #999;">滚动测试区域...</p>
          </div>
        </div>

        <div v-if="filteredSections.length === 0" class="no-data">
          <p>未找到相关章节</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'StudentLessonPlayer',
  data() {
    return {
      courseId: this.$route.params.id || this.$route.params.courseId || '1',
      lessonId: this.$route.params.lessonId ? parseInt(this.$route.params.lessonId) : null,
      sectionId: this.$route.query.sectionId ? parseInt(this.$route.query.sectionId) : null,
      courseInfo: {
        title: '加载中...'
      },
      sections: [],
      currentLesson: null,
      currentSection: null,
      chapterSearch: '',
      expandedSections: []
    }
  },
  computed: {
    // 过滤章节
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
    },
    // 获取所有课程的扁平列表
    allLessons() {
      const lessons = []
      this.sections.forEach(section => {
        section.lessons.forEach(lesson => {
          lessons.push({ lesson, section })
        })
      })
      return lessons
    },
    // 当前课程在列表中的索引
    currentLessonIndex() {
      if (!this.currentLesson) return -1
      return this.allLessons.findIndex(item => item.lesson.id === this.currentLesson.id)
    },
    // 上一课
    previousLesson() {
      if (this.currentLessonIndex > 0) {
        return this.allLessons[this.currentLessonIndex - 1]
      }
      return null
    },
    // 下一课
    nextLesson() {
      if (this.currentLessonIndex < this.allLessons.length - 1) {
        return this.allLessons[this.currentLessonIndex + 1]
      }
      return null
    }
  },
  created() {
    this.loadCourseData()
  },
  mounted() {
    // 进入页面时禁止body滚动
    document.body.style.overflow = 'hidden'
  },
  beforeDestroy() {
    // 离开页面时恢复body滚动
    document.body.style.overflow = ''
  },
  watch: {
    '$route.params.lessonId'(newId) {
      if (newId) {
        this.lessonId = parseInt(newId)
        this.loadCurrentLesson()
      }
    }
  },
  methods: {
    goBack() {
      // 返回到学生课程详情页
      this.$router.push(`/student/course/${this.courseId}`)
    },

    loadCourseData() {
      // TODO: 从API加载真实数据
      // 模拟数据
      this.courseInfo = {
        title: 'React 现代实战指南'
      }

      this.sections = [
        {
          id: 1,
          title: 'React 基础',
          description: '学习 React 的核心概念',
          lessons: [
            { id: 1, name: 'React 简介', type: 'video', duration: '15:30', description: '了解React的基本概念和优势', completed: false },
            { id: 2, name: '组件与 Props', type: 'video', duration: '20:45', description: '学习如何创建和使用React组件', completed: false },
            { id: 3, name: 'State 与生命周期', type: 'video', duration: '25:10', description: '掌握组件状态管理和生命周期方法', completed: false }
          ]
        },
        {
          id: 2,
          title: 'React Hooks',
          description: 'Hooks 是 React 16.8 的新增特性',
          lessons: [
            { id: 4, name: 'useState 详解', type: 'video', duration: '18:20', description: 'useState Hook的使用方法', completed: false },
            { id: 5, name: 'useEffect 使用', type: 'video', duration: '22:15', description: '处理副作用的Hook', completed: false },
            { id: 6, name: '自定义 Hook', type: 'document', duration: '16:40', description: '创建可复用的自定义Hook', completed: false }
          ]
        },
        {
          id: 3,
          title: '高级特性',
          description: 'Context、Refs、性能优化等',
          lessons: [
            { id: 7, name: 'Context API', type: 'video', duration: '19:30', description: 'React的上下文API使用', completed: false },
            { id: 8, name: 'useRef 与 forwardRef', type: 'document', duration: '14:50', description: 'Ref的高级用法', completed: false },
            { id: 9, name: 'React.memo 性能优化', type: 'video', duration: '21:00', description: '组件性能优化技巧', completed: false }
          ]
        }
      ]

      this.loadCurrentLesson()
    },

    loadCurrentLesson() {
      // 如果有指定lessonId，加载指定课程
      if (this.lessonId) {
        for (const section of this.sections) {
          const lesson = section.lessons.find(l => l.id === this.lessonId)
          if (lesson) {
            this.currentLesson = lesson
            this.currentSection = section
            // 自动展开当前章节
            if (!this.expandedSections.includes(section.id)) {
              this.expandedSections.push(section.id)
            }
            return
          }
        }
      }
      
      // 如果没有指定或找不到，自动选择第一个课程
      if (this.sections.length > 0 && this.sections[0].lessons.length > 0) {
        const firstSection = this.sections[0]
        const firstLesson = firstSection.lessons[0]
        
        this.currentLesson = firstLesson
        this.currentSection = firstSection
        this.expandedSections.push(firstSection.id)
        
        // 更新URL到第一个课程
        this.$router.replace({
          path: `/student/course/${this.courseId}/lesson/${firstLesson.id}`,
          query: { sectionId: firstSection.id }
        }).catch(err => {
          if (err.name !== 'NavigationDuplicated') {
            console.error(err)
          }
        })
      }
    },

    toggleSection(sectionId) {
      const index = this.expandedSections.indexOf(sectionId)
      if (index > -1) {
        this.expandedSections.splice(index, 1)
      } else {
        this.expandedSections.push(sectionId)
      }
    },

    selectLesson(lesson, section) {
      // 避免重复选择当前课程
      if (this.currentLesson && this.currentLesson.id === lesson.id) {
        return
      }
      
      this.currentLesson = lesson
      this.currentSection = section
      
      // 更新路由
      this.$router.replace({
        path: `/student/course/${this.courseId}/lesson/${lesson.id}`,
        query: {
          sectionId: section.id
        }
      }).catch(err => {
        // 忽略重复导航错误
        if (err.name !== 'NavigationDuplicated') {
          console.error(err)
        }
      })
    },

    goToLesson(lessonData) {
      if (lessonData) {
        this.selectLesson(lessonData.lesson, lessonData.section)
      }
    }
  }
}
</script>

<style scoped>
/* ==================== 1. 容器锁死 ==================== */
.lesson-player {
  width: 100%;
  height: calc(100vh - 64px) !important;
  display: flex !important;
  flex-direction: column !important;
  overflow: hidden !important;
  background: #f9fafb;
}

/* 页面头部：固定高度，不参与滚动 */
.page-header {
  flex-shrink: 0 !important;
  background: white;
  padding: 1rem 2rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  display: flex;
  justify-content: space-between;
  align-items: center;
  z-index: 10;
  position: relative;
  min-height: 60px;
  border-bottom: 3px solid #667eea;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.course-title h1 {
  margin: 0;
  font-size: 1.3rem;
  color: #1f2937;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

/* ==================== 2. 主体区域强制高度 ==================== */
.player-container {
  flex: 1 !important;
  min-height: 0 !important;
  display: flex !important;
  gap: 1rem;
  padding: 1rem;
  overflow: hidden !important;
}

/* ==================== 3. 内层彻底独立 ==================== */
/* 左侧内容区：独立滚动 */
.content-player {
  flex: 2 !important;
  height: 100% !important;
  overflow-y: auto !important;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

/* 右侧章节目录：独立滚动 */
.chapter-catalog {
  flex: 1 !important;
  height: 100% !important;
  display: flex !important;
  flex-direction: column !important;
  background: white;
  border-radius: 8px;
  overflow: hidden !important;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

/* 目录头部：固定不滚动 */
.catalog-header {
  flex-shrink: 0 !important;
  padding: 1.5rem;
  border-bottom: 1px solid #e5e7eb;
  background: #f9fafb;
}

.catalog-header h3 {
  margin: 0 0 1rem 0;
  font-size: 1.1rem;
  color: #1f2937;
}

/* 目录列表：可滚动区域 */
.catalog-list {
  flex: 1 !important;
  min-height: 0 !important;
  overflow-y: auto !important;
  padding: 1rem;
}

/* ==================== 内容区样式 ==================== */
.player-wrapper {
  padding: 0;
  min-height: 1200px; /* 临时：强制内容超出视口 */
}

.video-player,
.document-viewer {
  min-height: 600px; /* 增加高度 */
}

.video-placeholder,
.doc-placeholder {
  width: 100%;
  height: 100%;
  min-height: 600px; /* 增加高度 */
  background: #000;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: white;
}

.doc-placeholder {
  background: #f5f7fa;
  color: #606266;
}

.play-icon {
  width: 80px;
  height: 80px;
  background: rgba(255, 255, 255, 0.9);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
  color: #2c3e50;
  cursor: pointer;
  transition: all 0.3s;
  margin-bottom: 1rem;
}

.play-icon:hover {
  transform: scale(1.1);
  background: white;
}

.video-tip,
.video-info {
  color: rgba(255, 255, 255, 0.7);
  margin: 0.5rem 0;
}

.doc-name {
  margin-top: 1rem;
  font-size: 1.1rem;
}

.lesson-info {
  padding: 1.5rem;
  border-top: 1px solid #e5e7eb;
  min-height: 400px; /* 增加信息区高度 */
}

.lesson-header {
  display: flex;
  justify-content: flex-end;
  align-items: center;
}

.lesson-actions {
  display: flex;
  gap: 0.5rem;
}

.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: #909399;
  padding: 2rem;
}

/* ==================== 目录样式 ==================== */
.section-item {
  margin-bottom: 0.5rem;
}

.section-header {
  display: flex;
  align-items: center;
  padding: 0.75rem 1rem;
  background: #f9fafb;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s;
}

.section-header:hover {
  background: #e8eaed;
}

.expand-icon {
  margin-right: 0.5rem;
  color: #6b7280;
  transition: transform 0.3s;
  font-size: 0.8rem;
}

.expand-icon.expanded {
  transform: rotate(90deg);
}

.section-title {
  flex: 1;
  font-weight: 600;
  color: #1f2937;
}

.lesson-count {
  color: #6b7280;
  font-size: 0.85rem;
}

.lessons-list {
  margin-top: 0.5rem;
  margin-left: 1.5rem;
}

.lesson-item {
  display: flex;
  align-items: center;
  padding: 0.75rem 1rem;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s;
  gap: 0.5rem;
}

.lesson-item:hover {
  background: #f3f4f6;
}

.lesson-item.active {
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
  border-left: 3px solid #667eea;
}

.lesson-item.completed {
  opacity: 0.7;
}

.lesson-number {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: #e5e7eb;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.85rem;
  color: #6b7280;
}

.lesson-item.active .lesson-number {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.lesson-item.completed .lesson-number {
  background: #10b981;
  color: white;
}

.lesson-type-icon {
  font-size: 1.1rem;
}

.lesson-name {
  flex: 1;
  color: #374151;
  font-size: 0.95rem;
}

.lesson-item.active .lesson-name {
  color: #667eea;
  font-weight: 600;
}

.completed-icon {
  color: #10b981;
  font-weight: bold;
  font-size: 1.2rem;
}

.lesson-duration {
  color: #6b7280;
  font-size: 0.85rem;
}

.no-data {
  text-align: center;
  padding: 3rem 1rem;
  color: #9ca3af;
}

.no-data p {
  margin: 0.5rem 0 0 0;
}

/* 滚动条样式 */
.content-player::-webkit-scrollbar,
.catalog-list::-webkit-scrollbar {
  width: 6px;
}

.content-player::-webkit-scrollbar-thumb,
.catalog-list::-webkit-scrollbar-thumb {
  background: #d1d5db;
  border-radius: 3px;
}

.content-player::-webkit-scrollbar-thumb:hover,
.catalog-list::-webkit-scrollbar-thumb:hover {
  background: #9ca3af;
}
</style>
