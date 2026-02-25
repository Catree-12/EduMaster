<template>
  <div class="lesson-player">
    <!-- 页面头部 -->
    <div class="page-header">
      <div class="header-left">
        <el-button icon="el-icon-arrow-left" @click="goBack">返回课程</el-button>
        <div class="course-title">
          <h1>{{ courseInfo.title || '加载中...' }}</h1>
        </div>
      </div>
      <div class="header-right">
        <el-button icon="el-icon-edit" @click="goToChapterEditor">编辑章节</el-button>
      </div>
    </div>

    <!-- 主体内容 -->
    <div class="player-container">
      <!-- 左侧：内容展示区 -->
      <div class="content-player">
        <div v-if="currentLesson" class="lesson-content">
          <div class="lesson-header">
            <h2>{{ currentLesson.title }}</h2>
            <!-- <p class="lesson-meta">所属章节: {{ currentChapterTitle }}</p> -->
          </div>

          <div class="content-blocks-display">
            <div
              v-for="(block) in contentBlocks"
              :key="block.id"
              class="content-block-item"
            >
              <!-- 视频块 -->
              <div v-if="block.type === 'video'" class="block-video">
                <video
                  v-if="block.file"
                  :src="getMediaUrl(block.file)"
                  controls
                  style="width: 100%; max-height: 500px; border-radius: 8px;"
                ></video>
                <div v-else class="video-placeholder">
                  <i class="el-icon-video-camera" style="font-size: 64px;"></i>
                  <p>暂无视频</p>
                </div>
              </div>

              <!-- 富文本块 -->
              <div v-else-if="block.type === 'rich_text'" class="block-text">
                <div v-html="block.content?.html || block.content || ''"></div>
              </div>

              <!-- 文件块 -->
              <div v-else-if="block.type === 'file'" class="block-file">
                <div class="file-info">
                  <i class="el-icon-document" style="font-size: 48px; color: #409eff;"></i>
                  <p>{{ block.title }}</p>
                  <div class="file-actions">
                    <el-button
                      v-if="block.file"
                      type="primary"
                      size="small"
                      icon="el-icon-download"
                      @click="downloadFile(block.file, block.title)"
                    >
                      下载文件
                    </el-button>
                  </div>
                </div>
              </div>

              <!-- 图片块 -->
<!-- 图片块 -->
<div v-else-if="block.type === 'image'" class="block-image">
  <el-image
    v-if="block.file"
    :src="getMediaUrl(block.file)"
    :preview-src-list="[getMediaUrl(block.file)]"
    style="width: 100%; height: 360px; border-radius: 8px;"
    fit="cover"
  >
    <!-- 加载失败时的占位 -->
    <div slot="error" class="image-slot" style="display: flex; justify-content: center; align-items: center; height: 100%; background: #f5f7fa;">
      <i class="el-icon-picture-outline" style="font-size: 30px; color: #909399;"></i>
    </div>
  </el-image>
  <!-- 可选：添加提示文字 -->
  <p style="text-align: center; color: #909399; font-size: 12px; margin-top: 5px;">
    (点击图片可查看完整大图)
  </p>
</div>

              <!-- 代码块 -->
              <div v-else-if="block.type === 'code'" class="block-code">
                <pre><code>{{ block.content?.code || block.content || '' }}</code></pre>
              </div>
            </div>

            <div v-if="contentBlocks.length === 0" class="no-content">
              <i class="el-icon-document" style="font-size: 64px; color: #dcdfe6;"></i>
              <p>该课时暂无内容</p>
            </div>
          </div>
        </div>

        <!-- 加载状态 -->
        <div v-else-if="loading" class="loading-state">
          <i class="el-icon-loading" style="font-size: 48px; color: #409EFF;"></i>
          <p>加载中...</p>
        </div>

        <!-- 空状态 -->
        <div v-else class="empty-state">
          <i class="el-icon-document" style="font-size: 64px; color: #dcdfe6;"></i>
          <p>请从右侧选择课时</p>
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
          <!-- <span class="chapter-count">{{ chapters.length }} 个章节</span> -->
        </div>

        <div class="catalog-list" v-loading="catalogLoading">
          <div
            v-for="chapter in filteredChapters"
            :key="chapter.id"
            class="chapter-item"
          >
            <div class="chapter-header" @click="toggleChapter(chapter.id)">
              <!-- 增加 chapterSearch || ... -->
              <span :class="['expand-icon', { expanded: chapterSearch || expandedChapters.includes(chapter.id) }]">▶</span>
              <span class="chapter-title">{{ chapter.title }}</span>
              <span class="lesson-count">{{ chapter.lessons.length }} 课时</span>
            </div>

            <!-- <div v-show="expandedChapters.includes(chapter.id)" class="lessons-list"> -->
              
            <div v-show="chapterSearch || expandedChapters.includes(chapter.id)" class="lessons-list">
          <div
            v-for="(lesson, index) in chapter.lessons"
            :key="lesson.id"
            :class="['lesson-item', { active: currentLesson && currentLesson.id === lesson.id }]"
            @click="selectLesson(lesson, chapter)"
          >
            <div class="lesson-number">{{ index + 1 }}</div>
            <i class="el-icon-video-camera lesson-type-icon"></i>
            <div class="lesson-name">{{ lesson.title }}</div>
          </div>
        </div>
      </div>

          <div v-if="chapters.length === 0 && !catalogLoading" class="no-data">
            <i class="el-icon-folder" style="font-size: 48px; color: #dcdfe6;"></i>
            <p>暂无章节数据</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { getCourseChapters, getLessonDetail } from '@/api/teacher'

export default {
  name: 'TeacherLessonPlayer',
  data() {
    return {
      courseId: this.$route.params.courseId,
      lessonId: this.$route.params.lessonId,
      loading: false,
      catalogLoading: false,
      courseInfo: {
        title: ''
      },
      currentLesson: null,
      currentChapterTitle: '',
      contentBlocks: [],
      chapters: [],
      expandedChapters: [],
      chapterSearch: '',
      catalogLoaded: false // 标记章节数据是否已加载
    }
  },
  computed: {
  filteredChapters() {
    // 1. 如果没搜索，直接返回所有章节
    if (!this.chapterSearch) {
      return this.chapters;
    }

    const query = this.chapterSearch.toLowerCase();

    // 2. 遍历章节进行过滤
    return this.chapters.map(chapter => {
      // 检查章节标题是否包含关键词
      const isChapterMatch = chapter.title.toLowerCase().includes(query);
      
      // 检查该章节下的课时是否包含关键词
      const matchingLessons = chapter.lessons.filter(lesson => 
        lesson.title.toLowerCase().includes(query)
      );

      // 逻辑 A: 如果章节标题匹配，保留整个章节（包含所有课时）
      if (isChapterMatch) {
        return chapter;
      }

      // 逻辑 B: 如果章节不匹配，但底下有课时匹配，保留该章节 + 匹配的课时
      if (matchingLessons.length > 0) {
        return {
          ...chapter,
          lessons: matchingLessons
        };
      }

      // 都不匹配，返回 null
      return null;
    }).filter(item => item !== null); // 移除掉 null 的项
  }
},
  created() {
    // 恢复展开状态
    this.restoreExpandedState()
    // 只在首次加载或章节数据为空时请求
    if (!this.catalogLoaded || this.chapters.length === 0) {
      this.loadCourseData()
    }
    this.loadLessonData()
  },
  watch: {
    // 监听路由参数变化，重新加载课时数据
    '$route.params.lessonId'(newLessonId) {
      if (newLessonId) {
        this.lessonId = newLessonId
        this.loadLessonData()
      }
    }
  },
  mounted() {
    document.body.style.overflow = 'hidden'
  },
  beforeDestroy() {
    // 保存展开状态
    this.saveExpandedState()
    document.body.style.overflow = ''
  },
  methods: {
    goBack() {
      this.$router.push(`/teacher/courses/${this.courseId}`)
    },

    async loadCourseData() {
    this.catalogLoading = true
      try {
        const response = await getCourseChapters(this.courseId)
        
        this.courseInfo = {
          title: response.course_title || '课程名称'
        }
        
        this.chapters = (response.chapters || []).map(chapter => ({
          id: chapter.id,
          title: chapter.title,
          order: chapter.order,
          lessons: (chapter.lessons || []).map(lesson => ({
            id: lesson.id,
            title: lesson.title,
            order: lesson.order
          }))
        }))

        // 排序
        this.chapters.sort((a, b) => a.order - b.order)
        this.chapters.forEach(chapter => {
          chapter.lessons.sort((a, b) => a.order - b.order)
        })

        // 标记已加载
        this.catalogLoaded = true

        // 如果没有恢复的展开状态，默认展开当前课时所在的章节
        if (this.expandedChapters.length === 0 && this.$route.query.chapterId) {
          const chapterId = parseInt(this.$route.query.chapterId)
          this.expandedChapters.push(chapterId)
        }
      } catch (error) {
        console.error('加载课程目录失败:', error)
        this.$message.error('加载课程目录失败')
      } finally {
        this.catalogLoading = false
      }
    },

    async loadLessonData() {
      this.loading = true
      try {
        const response = await getLessonDetail(this.courseId, this.lessonId)
        
        this.currentLesson = {
          id: response.lesson_id || this.lessonId,
          title: response.title,
          chapter_id: response.chapter_id
        }
        
        this.currentChapterTitle = response.chapter_title || ''
        
        // 映射内容块
        this.contentBlocks = (response.content_blocks || []).map(block => {
          // 判断文件类型 - 如果是图片类型的文件,显示为图片
          let blockType = block.type
          if (block.type === 'file' && block.file_url) {
            const imageExtensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp']
            const fileExt = block.file_url.toLowerCase().match(/\.[^.]+$/)?.[0]
            if (fileExt && imageExtensions.includes(fileExt)) {
              blockType = 'image'
            }
          }
          
          return {
            id: block.id,
            type: blockType,
            title: block.title || '',
            file: block.file_url || block.file,
            content: block.content,
            order: block.order
          }
        })

        // 按order排序
        this.contentBlocks.sort((a, b) => a.order - b.order)
      } catch (error) {
        console.error('加载课时数据失败:', error)
        this.$message.error('加载课时数据失败')
      } finally {
        this.loading = false
      }
    },
    toggleChapter(chapterId) {
      // 如果正在搜索，不允许手动折叠
      if (this.chapterSearch) {
        return
      }
      
      const index = this.expandedChapters.indexOf(chapterId)
      if (index > -1) {
        this.expandedChapters.splice(index, 1)
      } else {
        this.expandedChapters.push(chapterId)
      }
      
      // 立即保存状态
      this.saveExpandedState()
    },

    selectLesson(lesson, chapter) {
      // 只更新路由，数据加载由 watch 监听器处理
      this.$router.push({
        path: `/teacher/courses/${this.courseId}/lessons/${lesson.id}`,
        query: {
          chapterId: chapter.id
        }
      })
    },

    getMediaUrl(url) {
      if (url && (url.startsWith('http://') || url.startsWith('https://'))) {
        return url
      }
      return `${process.env.VUE_APP_API_BASE_URL || 'http://localhost:8000'}${url}`
    },

    downloadFile(fileUrl, fileName) {
      const url = this.getMediaUrl(fileUrl)
      const link = document.createElement('a')
      link.href = url
      link.download = fileName
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
    },
    goToChapterEditor() {
      this.$router.push({
        path: `/teacher/courses/${this.courseId}/chapters/edit`,
        query: {
          lessonId: this.lessonId,
          chapterId: this.$route.query.chapterId
        }
      })
    },

    // 保存展开状态到 sessionStorage
    saveExpandedState() {
      const key = `expanded_chapters_${this.courseId}`
      sessionStorage.setItem(key, JSON.stringify(this.expandedChapters))
    },

    // 恢复展开状态
    restoreExpandedState() {
      const key = `expanded_chapters_${this.courseId}`
      const saved = sessionStorage.getItem(key)
      if (saved) {
        try {
          this.expandedChapters = JSON.parse(saved)
        } catch (error) {
          console.error('恢复展开状态失败:', error)
          this.expandedChapters = []
        }
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

/* 页面头部 */
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

/* ==================== 2. 主体区域 ==================== */
.player-container {
  flex: 1 !important;
  min-height: 0 !important;
  display: flex !important;
  gap: 1rem;
  padding: 1rem;
  overflow: hidden !important;
}

/* 左侧内容区 */
.content-player {
  flex: 2 !important;
  height: 100% !important;
  overflow-y: auto !important;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.lesson-content {
  padding: 2rem;
}

.lesson-header {
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid #e5e7eb;
}

.lesson-header h2 {
  margin: 0 0 0.5rem 0;
  font-size: 1.8rem;
  color: #1f2937;
}

.lesson-meta {
  margin: 0;
  color: #6b7280;
  font-size: 0.95rem;
}

.content-blocks-display {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.content-block-item {
  width: 100%;
}

.block-video video {
  width: 100%;
  background: #000;
}

.video-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 400px;
  background: #000;
  color: white;
  border-radius: 8px;
}

.video-placeholder p {
  margin-top: 1rem;
  color: rgba(255, 255, 255, 0.7);
}

.block-text {
  line-height: 1.8;
  color: #374151;
  font-size: 1rem;
}

.block-text >>> p {
  margin: 1em 0;
}

.block-text >>> h1,
.block-text >>> h2,
.block-text >>> h3 {
  margin: 1.5em 0 0.5em 0;
  color: #1f2937;
}

.block-file {
  padding: 2rem;
  background: #f9fafb;
  border-radius: 8px;
  text-align: center;
}

.file-info {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.file-info p {
  margin: 0;
  font-size: 1.1rem;
  color: #1f2937;
}

.block-image {
  text-align: center;
}

.block-image img {
  max-width: 100%;
  height: auto;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.block-code pre {
  background: #282c34;
  color: #abb2bf;
  padding: 1.5rem;
  border-radius: 8px;
  overflow-x: auto;
}

.block-code code {
  font-family: 'Courier New', monospace;
  font-size: 0.9rem;
  line-height: 1.6;
}

.no-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 2rem;
  color: #909399;
}

.no-content p {
  margin-top: 1rem;
}

.loading-state,
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: #909399;
  padding: 2rem;
}

.loading-state p,
.empty-state p {
  margin-top: 1rem;
}

/* 右侧章节目录 */
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

.catalog-header {
  flex-shrink: 0 !important;
  padding: 1.5rem;
  border-bottom: 1px solid #e5e7eb;
  background: #f9fafb;
}

.catalog-header h3 {
  margin: 0 0 0.5rem 0;
  font-size: 1.1rem;
  color: #1f2937;
}

.chapter-count {
  font-size: 0.85rem;
  color: #6b7280;
}

.catalog-list {
  flex: 1 !important;
  min-height: 0 !important;
  overflow-y: auto !important;
  padding: 1rem;
}

.chapter-item {
  margin-bottom: 0.5rem;
}

.chapter-header {
  display: flex;
  align-items: center;
  padding: 0.75rem 1rem;
  background: #f9fafb;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s;
  gap: 0.5rem;
}

.chapter-header:hover {
  background: #e8eaed;
}

.expand-icon {
  color: #6b7280;
  transition: transform 0.3s;
  font-size: 0.8rem;
}

.expand-icon.expanded {
  transform: rotate(90deg);
}

.chapter-title {
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
  margin-bottom: 0.25rem;
}

.lesson-item:hover {
  background: #f3f4f6;
}

.lesson-item.active {
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
  border-left: 3px solid #667eea;
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
  flex-shrink: 0;
}

.lesson-item.active .lesson-number {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.lesson-type-icon {
  font-size: 1.1rem;
  flex-shrink: 0;
}

.lesson-name {
  flex: 1;
  color: #374151;
  font-size: 0.95rem;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.lesson-item.active .lesson-name {
  color: #667eea;
  font-weight: 600;
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


