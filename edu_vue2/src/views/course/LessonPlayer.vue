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
      <div class="header-right">
        <el-button type="primary" icon="el-icon-edit" @click="editChapter">
          编辑章节
        </el-button>
      </div>
    </div>

    <!-- 主体内容 -->
    <div class="player-container">
      <!-- 左侧：内容播放区 -->
      <div class="content-player">
        <!-- 视频/文档播放器 -->
        <div v-if="currentLesson" class="player-wrapper">
          <div v-if="currentLesson.type === 'video'" class="video-player">
            <div class="video-placeholder">
              <div class="play-icon">▶</div>
              <p class="video-tip">视频播放器占位区</p>
            </div>
          </div>
          <div v-else class="document-viewer">
            <div class="doc-placeholder">
              <i class="el-icon-document" style="font-size: 64px; color: #909399;"></i>
              <p>文档查看器占位区</p>
            </div>
          </div>

          <!-- 课程信息 -->
          <div class="lesson-info">
            <div class="lesson-header">
              <h2>{{ currentLesson.name }}</h2>
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
            <div class="lesson-meta">
              <span><i class="el-icon-video-camera"></i> {{ currentLesson.type === 'video' ? '视频' : '文档' }}</span>
              <span><i class="el-icon-time"></i> {{ currentLesson.duration }}</span>
              <span v-if="currentSection"><i class="el-icon-folder"></i> {{ currentSection.title }}</span>
            </div>
            <div v-if="currentLesson.description" class="lesson-description">
              <p>{{ currentLesson.description }}</p>
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

        <div class="catalog-list">
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
                :class="['lesson-item', { active: currentLesson && currentLesson.id === lesson.id }]"
                @click="selectLesson(lesson, section)"
              >
                <span class="lesson-number">{{ index + 1 }}</span>
                <span class="lesson-type-icon">{{ lesson.type === 'video' ? '🎥' : '📄' }}</span>
                <span class="lesson-name">{{ lesson.name }}</span>
                <span class="lesson-duration">{{ lesson.duration }}</span>
              </div>
            </div>
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
  name: 'LessonPlayer',
  data() {
    return {
      courseId: this.$route.params.id,
      lessonId: parseInt(this.$route.params.lessonId),
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
      return this.allLessons.findIndex(item => item.lesson.id === this.lessonId)
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
  watch: {
    '$route.params.lessonId'(newId) {
      this.lessonId = parseInt(newId)
      this.loadCurrentLesson()
    }
  },
  methods: {
    goBack() {
      // 返回到教师课程详情页
      this.$router.push(`/teacher/course/${this.courseId}`)
    },

    editChapter() {
      // 跳转到章节编辑页面
      this.$router.push(`/teacher/course/${this.courseId}/chapters/edit`)
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
            { id: 1, name: 'React 简介', type: 'video', duration: '15:30', description: '了解React的基本概念和优势' },
            { id: 2, name: '组件与 Props', type: 'video', duration: '20:45', description: '学习如何创建和使用React组件' },
            { id: 3, name: 'State 与生命周期', type: 'video', duration: '25:10', description: '掌握组件状态管理和生命周期方法' }
          ]
        },
        {
          id: 2,
          title: 'React Hooks',
          description: 'Hooks 是 React 16.8 的新增特性',
          lessons: [
            { id: 4, name: 'useState 详解', type: 'video', duration: '18:20', description: 'useState Hook的使用方法' },
            { id: 5, name: 'useEffect 使用', type: 'video', duration: '22:15', description: '处理副作用的Hook' },
            { id: 6, name: '自定义 Hook', type: 'video', duration: '16:40', description: '创建可复用的自定义Hook' }
          ]
        },
        {
          id: 3,
          title: '高级特性',
          description: 'Context、Refs、性能优化等',
          lessons: [
            { id: 7, name: 'Context API', type: 'video', duration: '19:30', description: 'React的上下文API使用' },
            { id: 8, name: 'useRef 与 forwardRef', type: 'video', duration: '14:50', description: 'Ref的高级用法' },
            { id: 9, name: 'React.memo 性能优化', type: 'video', duration: '21:00', description: '组件性能优化技巧' }
          ]
        }
      ]

      this.loadCurrentLesson()
    },

    loadCurrentLesson() {
      // 查找当前课程
      for (const section of this.sections) {
        const lesson = section.lessons.find(l => l.id === this.lessonId)
        if (lesson) {
          this.currentLesson = lesson
          this.currentSection = section
          // 自动展开当前章节
          if (!this.expandedSections.includes(section.id)) {
            this.expandedSections.push(section.id)
          }
          break
        }
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
      this.$router.push({
        path: `/course/${this.courseId}/lesson/${lesson.id}`,
        query: {
          sectionId: section.id
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
.lesson-player {
  width: 100%;
  min-height: 100vh;
  background: #f5f7fa;
}

.page-header {
  background: white;
  padding: 1rem 2rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  margin-bottom: 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.header-right {
  display: flex;
  align-items: center;
}

.course-title h1 {
  margin: 0;
  font-size: 1.3rem;
  color: #2c3e50;
}

.player-container {
  display: flex;
  gap: 1rem;
  padding: 0 1rem 1rem 1rem;
  height: calc(100vh - 100px);
}

/* 左侧内容播放区 */
.content-player {
  flex: 2;
  background: white;
  border-radius: 8px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.player-wrapper {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.video-player,
.document-viewer {
  flex: 1;
  min-height: 400px;
}

.video-placeholder,
.doc-placeholder {
  width: 100%;
  height: 100%;
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

.video-tip {
  color: rgba(255, 255, 255, 0.7);
  margin: 0;
}

.lesson-info {
  padding: 1.5rem;
  border-top: 1px solid #e0e0e0;
}

.lesson-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.lesson-header h2 {
  margin: 0;
  font-size: 1.3rem;
  color: #2c3e50;
}

.lesson-actions {
  display: flex;
  gap: 0.5rem;
}

.lesson-meta {
  display: flex;
  gap: 1.5rem;
  color: #909399;
  font-size: 0.9rem;
  margin-bottom: 1rem;
}

.lesson-meta span {
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.lesson-description {
  color: #606266;
  line-height: 1.6;
}

.lesson-description p {
  margin: 0;
}

.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: #909399;
}

/* 右侧章节目录 */
.chapter-catalog {
  flex: 1;
  background: white;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.catalog-header {
  padding: 1.5rem;
  border-bottom: 1px solid #e0e0e0;
}

.catalog-header h3 {
  margin: 0 0 1rem 0;
  font-size: 1.1rem;
  color: #2c3e50;
}

.catalog-list {
  flex: 1;
  overflow-y: auto;
  padding: 1rem;
}

.section-item {
  margin-bottom: 0.5rem;
}

.section-header {
  display: flex;
  align-items: center;
  padding: 0.75rem 1rem;
  background: #f5f7fa;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s;
}

.section-header:hover {
  background: #e8eaed;
}

.expand-icon {
  margin-right: 0.5rem;
  color: #606266;
  transition: transform 0.3s;
  font-size: 0.8rem;
}

.expand-icon.expanded {
  transform: rotate(90deg);
}

.section-title {
  flex: 1;
  font-weight: 600;
  color: #2c3e50;
}

.lesson-count {
  color: #909399;
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
  background: #f0f2f5;
}

.lesson-item.active {
  background: #e3f2fd;
}

.lesson-number {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: #e0e0e0;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.85rem;
  color: #606266;
}

.lesson-item.active .lesson-number {
  background: #409EFF;
  color: white;
}

.lesson-type-icon {
  font-size: 1.1rem;
}

.lesson-name {
  flex: 1;
  color: #606266;
  font-size: 0.95rem;
}

.lesson-item.active .lesson-name {
  color: #409EFF;
  font-weight: 600;
}

.lesson-duration {
  color: #909399;
  font-size: 0.85rem;
}

.no-data {
  text-align: center;
  padding: 3rem 1rem;
  color: #909399;
}

.no-data p {
  margin: 0.5rem 0 0 0;
}

/* 滚动条样式 */
.catalog-list::-webkit-scrollbar {
  width: 6px;
}

.catalog-list::-webkit-scrollbar-thumb {
  background: #dcdfe6;
  border-radius: 3px;
}

.catalog-list::-webkit-scrollbar-thumb:hover {
  background: #c0c4cc;
}
</style>
