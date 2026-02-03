<template>
  <div class="course-preview">
    <!-- 预览模式提示条 -->
    <div class="preview-banner">
      <i class="el-icon-view"></i>
      <span>学生视角预览模式 - 这是学生看到的课程内容</span>
      <el-button size="small" @click="goBack" style="margin-left: auto;">
        <i class="el-icon-back"></i> 返回编辑
      </el-button>
    </div>

    <div class="preview-container">
      <!-- 左侧：内容展示区 -->
      <main class="content-area">
        <div v-if="!selectedSection" class="empty-state">
          <i class="el-icon-document" style="font-size: 64px; color: #dcdfe6;"></i>
          <p>请从右侧选择一个小节查看内容</p>
        </div>

        <div v-else class="section-detail">
          <!-- 小节标题 -->
          <div class="section-header">
            <h1>{{ currentChapterTitle }}.{{ currentSectionIndex + 1 }} {{ selectedSection.title || '未命名小节' }}</h1>
            <div class="section-meta">
              <el-tag size="small">{{ selectedSection.contentBlocks.length }} 个内容块</el-tag>
              <el-tag size="small" type="success" v-if="selectedSection.knowledgePoints?.length">
                {{ selectedSection.knowledgePoints.length }} 个知识点
              </el-tag>
            </div>
          </div>

          <!-- 知识点 -->
          <div v-if="selectedSection.knowledgePoints?.length" class="knowledge-points">
            <h3><i class="el-icon-collection-tag"></i> 本节知识点</h3>
            <div class="knowledge-tags">
              <el-tag
                v-for="(point, idx) in selectedSection.knowledgePoints"
                :key="idx"
                size="medium"
                type="info"
              >
                {{ point }}
              </el-tag>
            </div>
          </div>

          <!-- 内容块列表 -->
          <div v-if="selectedSection.contentBlocks.length === 0" class="no-content">
            <el-empty description="该小节暂无学习内容"></el-empty>
          </div>

          <div v-else class="content-blocks">
            <div
              v-for="(block, index) in selectedSection.contentBlocks"
              :key="block.id"
              class="content-block"
            >
              <div class="block-header">
                <span class="block-index">{{ index + 1 }}</span>
                <span class="block-type-label">{{ getBlockTypeLabel(block.type) }}</span>
              </div>

              <!-- 视频块 -->
              <div v-if="block.type === 'video'" class="block-content video-block">
                <div class="video-placeholder">
                  <i class="el-icon-video-play" style="font-size: 48px; color: #409eff;"></i>
                  <p class="video-name">{{ block.videoName || '未命名视频' }}</p>
                  <p class="video-info">要求观看进度: {{ block.watchPercent }}%</p>
                  <el-button type="primary" icon="el-icon-video-play">播放视频</el-button>
                </div>
              </div>

              <!-- 文档块 -->
              <div v-if="block.type === 'document'" class="block-content document-block">
                <div class="document-preview">
                  <i class="el-icon-document" style="font-size: 48px; color: #67c23a;"></i>
                  <p class="document-name">{{ block.displayName || block.docName || '未命名文档' }}</p>
                  <el-button type="success" icon="el-icon-download">下载文档</el-button>
                </div>
              </div>

              <!-- 文本块 -->
              <div v-if="block.type === 'text'" class="block-content text-block">
                <div class="text-content">
                  {{ block.textContent || '暂无文本内容' }}
                </div>
              </div>

              <!-- 测验块 -->
              <div v-if="block.type === 'quiz'" class="block-content quiz-block">
                <div class="quiz-info">
                  <i class="el-icon-edit-outline" style="font-size: 48px; color: #e6a23c;"></i>
                  <p class="quiz-title">课堂测验</p>
                  <p class="quiz-status">
                    <el-tag :type="block.quizCreated ? 'success' : 'info'">
                      {{ block.quizCreated ? '已创建测验' : '测验准备中' }}
                    </el-tag>
                  </p>
                  <el-button 
                    v-if="block.quizCreated" 
                    type="warning" 
                    icon="el-icon-edit-outline"
                  >
                    开始测验
                  </el-button>
                  <span v-else class="disabled-hint">教师正在准备测验内容</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>

      <!-- 右侧：章节目录 -->
      <aside class="catalog-sidebar">
        <div class="course-info">
          <h2>{{ courseInfo.name || '课程名称' }}</h2>
        </div>

        <!-- 搜索框 -->
        <div class="catalog-search">
          <el-input
            v-model="searchKeyword"
            placeholder="搜索章节或小节"
            prefix-icon="el-icon-search"
            clearable
            size="small"
          >
          </el-input>
        </div>

        <div class="catalog-content">
          <div
            v-for="(chapter, chIdx) in filteredChapters"
            :key="chapter.id"
            class="catalog-chapter"
          >
            <div
              class="chapter-header"
              @click="toggleChapter(chapter.id)"
            >
              <i :class="['expand-icon', expandedChapters.includes(chapter.id) ? 'el-icon-arrow-down' : 'el-icon-arrow-right']"></i>
              <span class="chapter-title">第{{ chIdx + 1 }}章 {{ chapter.title || '未命名章节' }}</span>
              <span class="section-count">{{ chapter.sections.length }}节</span>
            </div>

            <div
              v-show="expandedChapters.includes(chapter.id)"
              class="chapter-sections"
            >
              <div
                v-for="(section, secIdx) in chapter.sections"
                :key="section.id"
                :class="['section-item', { active: selectedSection?.id === section.id }]"
                @click="selectSection(section, chapter, chIdx, secIdx)"
              >
                <i class="el-icon-document"></i>
                <span class="section-title">{{ chIdx + 1 }}.{{ secIdx + 1 }} {{ section.title || '未命名小节' }}</span>
                <el-tag size="mini" type="info" v-if="section.contentBlocks.length > 0">
                  {{ section.contentBlocks.length }}
                </el-tag>
              </div>
            </div>
          </div>
        </div>
      </aside>
    </div>
  </div>
</template>

<script>
export default {
  name: 'CoursePreview',
  data() {
    return {
      courseId: this.$route.params.courseId,
      courseInfo: {
        name: '课程名称'
      },
      chapters: [],
      expandedChapters: [],
      selectedSection: null,
      currentChapterTitle: '',
      currentSectionIndex: 0,
      searchKeyword: '' // 搜索关键字
    }
  },
  computed: {
    // 过滤章节和小节
    filteredChapters() {
      if (!this.searchKeyword || !this.searchKeyword.trim()) {
        return this.chapters
      }
      
      const keyword = this.searchKeyword.toLowerCase().trim()
      return this.chapters.map(chapter => {
        const chapterTitleMatch = (chapter.title || '未命名章节').toLowerCase().includes(keyword)
        const filteredSections = chapter.sections.filter(section => 
          (section.title || '未命名小节').toLowerCase().includes(keyword)
        )
        
        // 如果章节标题匹配，显示所有小节
        if (chapterTitleMatch) {
          return chapter
        }
        
        // 如果有小节匹配，只显示匹配的小节
        if (filteredSections.length > 0) {
          return {
            ...chapter,
            sections: filteredSections
          }
        }
        
        return null
      }).filter(chapter => chapter !== null)
    }
  },
  watch: {
    // 搜索时自动展开匹配的章节
    searchKeyword(val) {
      if (val && val.trim()) {
        this.expandedChapters = this.filteredChapters.map(c => c.id)
      } else {
        this.expandedChapters = this.chapters.map(c => c.id)
      }
    }
  },
  created() {
    this.loadPreviewData()
  },
  methods: {
    loadPreviewData() {
      const previewData = sessionStorage.getItem('coursePreviewData')
      if (previewData) {
        const data = JSON.parse(previewData)
        this.courseInfo = data.courseInfo
        this.chapters = data.chapters
        
        // 默认展开所有章节
        this.expandedChapters = this.chapters.map(c => c.id)
        
        // 自动选择第一个有内容的小节
        if (this.chapters.length > 0 && this.chapters[0].sections.length > 0) {
          this.selectSection(this.chapters[0].sections[0], this.chapters[0], 0, 0)
        }
      } else {
        this.$message.warning('未找到预览数据')
        this.goBack()
      }
    },

    toggleChapter(chapterId) {
      const index = this.expandedChapters.indexOf(chapterId)
      if (index > -1) {
        this.expandedChapters.splice(index, 1)
      } else {
        this.expandedChapters.push(chapterId)
      }
    },

    selectSection(section, chapter, chapterIndex, sectionIndex) {
      this.selectedSection = section
      this.currentChapterTitle = `第${chapterIndex + 1}章`
      this.currentSectionIndex = sectionIndex
    },

    getBlockTypeLabel(type) {
      const labels = {
        video: '📹 视频',
        document: '📄 文档',
        text: '📝 文本',
        quiz: '✅ 测验'
      }
      return labels[type] || type
    },

    goBack() {
      sessionStorage.removeItem('coursePreviewData')
      this.$router.push(`/teacher/courses/${this.courseId}/chapters`)
    }
  }
}
</script>

<style scoped lang="scss">
.course-preview {
  width: 100%;
  min-height: 100vh;
  background: #f5f7fa;
  display: flex;
  flex-direction: column;
}

.preview-banner {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 12px 24px;
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 14px;
  font-weight: 500;
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.25);
  z-index: 100;

  i {
    font-size: 18px;
  }
}

.preview-container {
  display: flex;
  flex: 1;
  height: calc(100vh - 48px);
  overflow: hidden;
}

/* 左侧内容区 */
.content-area {
  flex: 1;
  overflow-y: auto;
  background: #fafafa;
  order: 1; /* 确保内容区在左侧 */

  &::-webkit-scrollbar {
    width: 8px;
  }

  &::-webkit-scrollbar-thumb {
    background: #dcdfe6;
    border-radius: 4px;
  }
}

/* 右侧目录 */
.catalog-sidebar {
  width: 320px;
  background: white;
  border-left: 1px solid #e4e7ed;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  order: 2; /* 确保目录在右侧 */
}

.course-info {
  padding: 20px;
  border-bottom: 2px solid #f0f2f5;

  h2 {
    margin: 0;
    font-size: 18px;
    color: #303133;
    font-weight: 600;
  }
}

.catalog-search {
  padding: 12px 16px;
  background: #fafafa;
  border-bottom: 1px solid #e4e7ed;

  ::v-deep .el-input__inner {
    border-radius: 16px;
  }
}

.catalog-content {
  flex: 1;
  overflow-y: auto;
  padding: 12px 0;

  &::-webkit-scrollbar {
    width: 6px;
  }

  &::-webkit-scrollbar-thumb {
    background: #dcdfe6;
    border-radius: 3px;
  }
}

.catalog-chapter {
  margin-bottom: 8px;

  .chapter-header {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 12px 20px;
    cursor: pointer;
    transition: all 0.2s;
    user-select: none;

    &:hover {
      background: #f5f7fa;
    }

    .expand-icon {
      color: #909399;
      font-size: 14px;
      transition: transform 0.2s;
    }

    .chapter-title {
      flex: 1;
      font-size: 15px;
      font-weight: 600;
      color: #303133;
    }

    .section-count {
      font-size: 12px;
      color: #909399;
    }
  }

  .chapter-sections {
    padding-left: 12px;

    .section-item {
      display: flex;
      align-items: center;
      gap: 8px;
      padding: 10px 20px 10px 32px;
      cursor: pointer;
      transition: all 0.2s;
      border-left: 3px solid transparent;

      i {
        color: #909399;
        font-size: 14px;
      }

      .section-title {
        flex: 1;
        font-size: 14px;
        color: #606266;
      }

      &:hover {
        background: #f5f7fa;
      }

      &.active {
        background: #ecf5ff;
        border-left-color: #409eff;

        i {
          color: #409eff;
        }

        .section-title {
          color: #409eff;
          font-weight: 500;
        }
      }
    }
  }
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: #909399;

  p {
    margin-top: 16px;
    font-size: 14px;
  }
}

.section-detail {
  max-width: 1000px;
  margin: 0 auto;
  padding: 32px;
}

.section-header {
  margin-bottom: 32px;
  padding-bottom: 20px;
  border-bottom: 2px solid #e4e7ed;

  h1 {
    margin: 0 0 12px 0;
    font-size: 28px;
    color: #303133;
    font-weight: 600;
  }

  .section-meta {
    display: flex;
    gap: 8px;
  }
}

.knowledge-points {
  background: white;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);

  h3 {
    margin: 0 0 16px 0;
    font-size: 16px;
    color: #303133;
    display: flex;
    align-items: center;
    gap: 8px;

    i {
      color: #409eff;
    }
  }

  .knowledge-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
  }
}

.no-content {
  background: white;
  padding: 60px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.content-blocks {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.content-block {
  background: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  transition: all 0.3s;

  &:hover {
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  }

  .block-header {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 16px 20px;
    background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%);
    border-bottom: 1px solid #e4e7ed;

    .block-index {
      width: 28px;
      height: 28px;
      border-radius: 50%;
      background: #409eff;
      color: white;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 14px;
      font-weight: 600;
    }

    .block-type-label {
      font-size: 15px;
      font-weight: 600;
      color: #303133;
    }
  }

  .block-content {
    padding: 32px;
  }
}

.video-placeholder,
.document-preview,
.quiz-info {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 40px 20px;

  p {
    margin: 12px 0;
  }

  .video-name,
  .document-name,
  .quiz-title {
    font-size: 16px;
    font-weight: 600;
    color: #303133;
  }

  .video-info,
  .quiz-status {
    font-size: 14px;
    color: #909399;
  }

  .disabled-hint {
    font-size: 13px;
    color: #c0c4cc;
    font-style: italic;
  }
}

.text-block {
  .text-content {
    font-size: 15px;
    line-height: 1.8;
    color: #606266;
    white-space: pre-wrap;
    word-break: break-word;
  }
}
</style>
