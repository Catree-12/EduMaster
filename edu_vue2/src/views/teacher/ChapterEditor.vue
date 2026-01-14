<template>
  <div class="chapter-editor">
    <!-- 顶部标题栏 -->
    <div class="editor-header">
      <div class="header-left">
        <el-button icon="el-icon-arrow-left" @click="goBack">返回</el-button>
        <h2 class="course-title">{{ courseInfo.name }}</h2>
      </div>
      <div class="header-right">
        <el-button icon="el-icon-view" @click="previewCourse">
          学生视角预览
        </el-button>
        <el-button type="success" icon="el-icon-check" @click="saveAll" :loading="saving">
          全量保存
        </el-button>
      </div>
    </div>

    <!-- 主体区域：左右布局 -->
    <div class="editor-body">
      <!-- 左侧：目录导航树(30%) -->
      <div class="catalog-tree">
        <div class="tree-header">
          <el-input
            v-model="catalogSearch"
            placeholder="搜索节..."
            prefix-icon="el-icon-search"
            size="small"
            clearable
          />
          <div class="tree-actions">
            <el-button 
              type="primary" 
              icon="el-icon-plus" 
              size="small" 
              @click="addChapter" 
              style="width: 48%;"
            >
              添加章节
            </el-button>
            <el-button 
              type="success" 
              icon="el-icon-plus" 
              size="small" 
              @click="addSectionToCurrentChapter" 
              style="width: 48%;"
              :disabled="!currentChapter"
            >
              添加小节
            </el-button>
          </div>
        </div>

        <div class="tree-content">
          <div v-if="filteredChapters.length === 0" class="tree-empty">
            <i class="el-icon-folder-opened" style="font-size: 36px; color: #dcdfe6;"></i>
            <p style="font-size: 12px; color: #909399;">暂无章节</p>
          </div>

          <draggable
            v-else
            v-model="chapters"
            handle=".tree-drag-handle"
            animation="200"
            @end="onChapterDragEnd"
          >
            <div
              v-for="(chapter, chapterIndex) in filteredChapters"
              :key="chapter.id"
              class="tree-chapter"
            >
              <div 
                class="tree-chapter-header"
                :class="{ active: currentChapter && currentChapter.id === chapter.id, collapsed: chapter.collapsed }"
                @click="toggleChapter(chapter)"
              >
                <i class="el-icon-rank tree-drag-handle"></i>
                <i :class="chapter.collapsed ? 'el-icon-folder' : 'el-icon-folder-opened'" class="chapter-icon"></i>
                <span class="chapter-title">{{ chapter.title || '未命名章节' }}</span>
                <span class="section-count">({{ chapter.sections.length }})</span>
                <el-dropdown trigger="click" @command="(cmd) => handleChapterCommand(cmd, chapter)" @click.native.stop>
                  <span class="tree-more-btn">
                    <i class="el-icon-more"></i>
                  </span>
                  <el-dropdown-menu slot="dropdown">
                    <el-dropdown-item command="rename">重命名</el-dropdown-item>
                    <el-dropdown-item command="move">移动到</el-dropdown-item>
                    <el-dropdown-item command="delete" divided>删除</el-dropdown-item>
                  </el-dropdown-menu>
                </el-dropdown>
              </div>

              <draggable
                v-if="!chapter.collapsed"
                v-model="chapter.sections"
                handle=".tree-section-drag-handle"
                animation="200"
                @end="markChanged"
                class="tree-sections"
              >
                <div
                  v-for="(section, sectionIndex) in chapter.sections"
                  :key="section.id"
                  class="tree-section"
                  :class="{ active: selectedNode && selectedNode.type === 'section' && selectedNode.id === section.id }"
                  @click="selectSection(section, chapter, chapterIndex, sectionIndex)"
                >
                  <i class="el-icon-rank tree-section-drag-handle"></i>
                  <i class="el-icon-tickets section-icon"></i>
                  <span class="section-title">{{ section.title || '未命名小节' }}</span>
                  <span class="block-count">({{ section.contentBlocks.length }})</span>
                  <el-dropdown trigger="click" @command="(cmd) => handleSectionCommand(cmd, section, chapter, sectionIndex)" @click.native.stop>
                    <span class="tree-more-btn">
                      <i class="el-icon-more"></i>
                    </span>
                    <el-dropdown-menu slot="dropdown">
                      <el-dropdown-item command="rename">重命名</el-dropdown-item>
                      <el-dropdown-item command="move">移动到</el-dropdown-item>
                      <el-dropdown-item command="delete" divided>删除</el-dropdown-item>
                    </el-dropdown-menu>
                  </el-dropdown>
                </div>
              </draggable>
            </div>
          </draggable>
        </div>
      </div>

      <!-- 右侧：节点内容容器(70%) -->
      <div class="node-container">
        <!-- 顶部工具栏：固定内容块添加按钮 -->
        <div class="content-toolbar-fixed" v-if="selectedNode && selectedNode.type === 'section'">
          <span class="toolbar-label">快速添加内容：</span>
          <el-button-group>
            <el-button size="small" icon="el-icon-video-camera" @click="addContentBlock('video')">
              视频
            </el-button>
            <el-button size="small" icon="el-icon-document" @click="addContentBlock('document')">
              文档
            </el-button>
            <el-button size="small" icon="el-icon-edit-outline" @click="addContentBlock('text')">
              文字
            </el-button>
            <el-button size="small" icon="el-icon-document-checked" @click="addContentBlock('quiz')">
              测验
            </el-button>
          </el-button-group>
        </div>

        <div v-if="!selectedNode" class="editor-empty">
          <i class="el-icon-document" style="font-size: 64px; color: #dcdfe6;"></i>
          <p>请在左侧选择要编辑的小节</p>
        </div>

        <!-- 编辑小节（核心：内容块容器） -->
        <div v-else-if="selectedNode.type === 'section'" class="section-editor-area">
          <!-- 小节头部：标题与知识点 -->
          <div class="node-header">
            <div class="node-title-area">
              <el-input
                v-model="selectedNode.data.title"
                placeholder="请输入小节标题"
                @change="markChanged"
                size="large"
              >
                <template slot="prepend">
                  <i class="el-icon-tickets"></i> {{ selectedNode.chapterIndex + 1 }}.{{ selectedNode.sectionIndex + 1 }}
                </template>
              </el-input>
            </div>
            <div class="node-actions">
              <el-button size="small" type="danger" icon="el-icon-delete" @click="deleteSection(selectedNode.chapter, selectedNode.sectionIndex)">
                删除小节
              </el-button>
            </div>
          </div>

          <!-- 知识点标签区 -->
          <div class="knowledge-area">
            <span class="knowledge-label">知识点：</span>
            <div class="knowledge-tags">
              <el-tag
                v-for="(point, idx) in selectedNode.data.knowledgePoints"
                :key="idx"
                closable
                @close="removeKnowledgePoint(selectedNode.data, idx)"
                style="margin-right: 8px;"
                type="success"
              >
                {{ point }}
              </el-tag>
              <el-input
                v-if="showKnowledgeInput"
                v-model="newKnowledgePoint"
                size="small"
                style="width: 150px;"
                placeholder="输入知识点"
                @blur="confirmAddKnowledgePoint(selectedNode.data)"
                @keyup.enter="confirmAddKnowledgePoint(selectedNode.data)"
                ref="knowledgeInput"
              ></el-input>
              <el-button
                v-else
                size="small"
                type="primary"
                plain
                icon="el-icon-plus"
                @click="showAddKnowledgeInput"
              >
                添加知识点
              </el-button>
            </div>
          </div>

          <!-- 内容块垂直列表（可拖拽） -->
          <div class="content-blocks-container">
            <el-empty v-if="selectedNode.data.contentBlocks.length === 0" description="暂无内容块，点击下方按钮添加">
              <template slot="image">
                <i class="el-icon-box" style="font-size: 64px; color: #dcdfe6;"></i>
              </template>
            </el-empty>

            <draggable
              v-else
              v-model="selectedNode.data.contentBlocks"
              handle=".block-drag-handle"
              animation="200"
              @end="markChanged"
            >
              <div
                v-for="(block, blockIndex) in selectedNode.data.contentBlocks"
                :key="block.id"
                class="content-block-card"
              >
                <!-- 块通用头部 -->
                <div class="block-header">
                  <div class="block-header-left">
                    <i class="el-icon-rank block-drag-handle"></i>
                    <el-tag :type="getBlockTagType(block.type)" size="small">
                      {{ getBlockTypeName(block.type) }}
                    </el-tag>
                    <span class="block-order">内容块 {{ blockIndex + 1 }}</span>
                  </div>
                  <el-button
                    type="text"
                    icon="el-icon-delete"
                    class="block-delete-btn"
                    @click="deleteContentBlock(selectedNode.data, blockIndex)"
                  >
                    删除
                  </el-button>
                </div>

                <!-- 视频块 -->
                <div v-if="block.type === 'video'" class="block-content">
                  <el-form label-width="120px" size="small">
                    <el-form-item label="视频文件">
                      <el-upload
                        v-if="!block.videoUrl"
                        class="video-uploader"
                        drag
                        :action="uploadUrl"
                        :on-success="(res, file) => handleVideoUpload(res, file, block)"
                        accept="video/*"
                      >
                        <i class="el-icon-upload"></i>
                        <div class="el-upload__text">拖拽视频文件到此处，或<em>点击上传</em></div>
                        <div class="el-upload__tip" slot="tip">支持 MP4、AVI、MOV 等格式</div>
                      </el-upload>
                      <div v-else class="file-preview">
                        <i class="el-icon-video-camera"></i>
                        <span>{{ block.videoName }}</span>
                        <el-button type="text" @click="removeBlockFile(block)" style="color: #f56c6c;">移除</el-button>
                      </div>
                    </el-form-item>
                    <el-form-item label="观看时长要求">
                      <el-input-number
                        v-model="block.watchPercent"
                        :min="0"
                        :max="100"
                        @change="markChanged"
                      ></el-input-number>
                      <span style="margin-left: 10px; color: #909399;">% （学生需观看达到此进度）</span>
                    </el-form-item>
                  </el-form>
                </div>

                <!-- 文档块 -->
                <div v-else-if="block.type === 'document'" class="block-content">
                  <el-form label-width="120px" size="small">
                    <el-form-item label="课件文件">
                      <el-upload
                        v-if="!block.docUrl"
                        class="doc-uploader"
                        drag
                        :action="uploadUrl"
                        :on-success="(res, file) => handleDocUpload(res, file, block)"
                        accept=".pdf,.ppt,.pptx,.doc,.docx"
                      >
                        <i class="el-icon-upload"></i>
                        <div class="el-upload__text">拖拽课件文件到此处，或<em>点击上传</em></div>
                        <div class="el-upload__tip" slot="tip">支持 PDF、PPT、Word 等格式</div>
                      </el-upload>
                      <div v-else class="file-preview">
                        <i class="el-icon-document"></i>
                        <span>{{ block.docName }}</span>
                        <el-button type="text" @click="removeBlockFile(block)" style="color: #f56c6c;">移除</el-button>
                      </div>
                    </el-form-item>
                    <el-form-item label="文档重命名">
                      <el-input
                        v-model="block.displayName"
                        placeholder="为学生显示的文档名称"
                        @change="markChanged"
                      ></el-input>
                    </el-form-item>
                  </el-form>
                </div>

                <!-- 文字块 -->
                <div v-else-if="block.type === 'text'" class="block-content">
                  <el-form label-width="120px" size="small">
                    <el-form-item label="文字内容">
                      <el-input
                        v-model="block.textContent"
                        type="textarea"
                        :rows="8"
                        placeholder="请输入本节的文字说明、学习提示等内容..."
                        @change="markChanged"
                      ></el-input>
                      <div style="color: #909399; font-size: 12px; margin-top: 5px;">
                        <i class="el-icon-info"></i> 支持纯文本格式
                      </div>
                    </el-form-item>
                  </el-form>
                </div>

                <!-- 测验块（核心新增） -->
                <div v-else-if="block.type === 'quiz'" class="block-content">
                  <el-form label-width="120px" size="small">
                    <el-form-item label="测验模式">
                      <el-radio-group v-model="block.quizMode" @change="handleQuizModeChange(block)">
                        <el-radio label="select">从作业库选择</el-radio>
                        <el-radio label="create">新建测验</el-radio>
                      </el-radio-group>
                    </el-form-item>

                    <!-- 选择模式 -->
                    <el-form-item v-if="block.quizMode === 'select'" label="选择作业">
                      <el-select
                        v-model="block.linkedHomeworkId"
                        placeholder="搜索并选择作业"
                        filterable
                        clearable
                        @change="markChanged"
                        style="width: 100%;"
                      >
                        <el-option label="第一章作业" value="hw1"></el-option>
                        <el-option label="第二章作业" value="hw2"></el-option>
                        <el-option label="综合练习" value="hw3"></el-option>
                        <el-option label="Vue基础测验" value="hw4"></el-option>
                      </el-select>
                      <div style="color: #909399; font-size: 12px; margin-top: 5px;">
                        <i class="el-icon-info"></i> 从已创建的作业库中快速关联
                      </div>
                    </el-form-item>

                    <!-- 新建模式 -->
                    <el-form-item v-else-if="block.quizMode === 'create'" label="测验配置">
                      <div class="quiz-create-area">
                        <el-button
                          v-if="!block.quizCreated"
                          type="primary"
                          icon="el-icon-plus"
                          @click="createNewQuiz(block)"
                        >
                          创建新测验
                        </el-button>
                        <div v-else class="quiz-info">
                          <el-alert type="success" :closable="false">
                            <template slot="title">
                              <i class="el-icon-success"></i> 已创建测验：{{ block.quizTitle || '未命名测验' }}
                            </template>
                          </el-alert>
                          <el-button
                            size="small"
                            type="text"
                            icon="el-icon-edit"
                            @click="editQuiz(block)"
                            style="margin-top: 10px;"
                          >
                            编辑测验内容
                          </el-button>
                        </div>
                      </div>
                    </el-form-item>
                  </el-form>
                </div>
              </div>
            </draggable>
          </div>

          <!-- 移除底部工具栏 -->
        </div>
      </div>
    </div>

    <!-- 新建测验弹窗（复用作业创建逻辑） -->
    <el-dialog
      title="创建测验"
      :visible.sync="quizDialogVisible"
      width="90%"
      top="5vh"
      :close-on-click-modal="false"
    >
      <div v-if="currentQuizBlock" style="max-height: 70vh; overflow-y: auto;">
        <p style="color: #909399; margin-bottom: 20px;">
          <i class="el-icon-info"></i> 该测验将嵌入本节内容中，学生学习到此处时需完成测验
        </p>
        <!-- TODO: 这里复用 HomeworkCreate.vue 的题目编辑逻辑 -->
        <el-form label-width="120px">
          <el-form-item label="测验标题">
            <el-input v-model="currentQuizBlock.quizTitle" placeholder="例如：第一节课后测验"></el-input>
          </el-form-item>
          <el-form-item label="测验说明">
            <el-input
              type="textarea"
              :rows="3"
              v-model="currentQuizBlock.quizDescription"
              placeholder="测验的注意事项、考查重点等"
            ></el-input>
          </el-form-item>
          <el-divider></el-divider>
          <el-alert type="info" :closable="false" style="margin-bottom: 15px;">
            此处应复用作业创建页面的题目编辑器组件（题型选择、题目内容、答案设置等）
          </el-alert>
        </el-form>
      </div>
      <span slot="footer">
        <el-button @click="quizDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="confirmCreateQuiz">确认创建</el-button>
      </span>
    </el-dialog>

    <!-- 移动节点对话框 -->
    <el-dialog
      :title="moveType === 'chapter' ? '移动章节' : '移动小节'"
      :visible.sync="moveDialogVisible"
      width="500px"
    >
      <div class="move-dialog-content">
        <el-alert 
          type="info" 
          :closable="false" 
          style="margin-bottom: 15px;"
        >
          <template v-if="moveType === 'chapter'">
            选择目标章节，将 <strong>{{ moveSourceItem?.title || '未命名章节' }}</strong> 移动到目标章节的前面或后面
          </template>
          <template v-else>
            选择目标章节，将 <strong>{{ moveSourceItem?.title || '未命名小节' }}</strong> 移动到目标章节下
          </template>
        </el-alert>

        <el-form label-width="100px">
          <el-form-item label="目标章节">
            <el-select 
              v-model="moveTargetChapter" 
              placeholder="请选择目标章节" 
              style="width: 100%;"
              filterable
            >
              <el-option
                v-for="(chapter, index) in chapters"
                :key="chapter.id"
                :label="`第${index + 1}章: ${chapter.title || '未命名章节'}`"
                :value="chapter"
                :disabled="moveType === 'chapter' && chapter.id === moveSourceItem?.id"
              >
                <span>第{{ index + 1 }}章: {{ chapter.title || '未命名章节' }}</span>
                <span style="float: right; color: #8492a6; font-size: 12px;">
                  ({{ chapter.sections.length }}个小节)
                </span>
              </el-option>
            </el-select>
          </el-form-item>

          <el-form-item label="插入位置" v-if="moveType === 'chapter'">
            <el-radio-group v-model="moveTargetPosition">
              <el-radio label="before">在目标章节之前</el-radio>
              <el-radio label="after">在目标章节之后</el-radio>
            </el-radio-group>
          </el-form-item>

          <el-form-item label="插入位置" v-else>
            <el-select 
              v-model="moveTargetPosition" 
              placeholder="选择插入位置" 
              style="width: 100%;"
              :disabled="!moveTargetChapter"
            >
              <el-option label="移动到最前" value="0"></el-option>
              <el-option
                v-for="(section, idx) in (moveTargetChapter?.sections || [])"
                :key="idx"
                :label="`移动到'${section.title || '未命名小节'}'之后`"
                :value="String(idx + 1)"
              ></el-option>
            </el-select>
          </el-form-item>
        </el-form>
      </div>
      <span slot="footer">
        <el-button @click="moveDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="confirmMove" :disabled="!moveTargetChapter">确认移动</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import draggable from 'vuedraggable'

export default {
  name: 'ChapterEditor',
  components: {
    draggable
  },
  data() {
    return {
      courseId: null,
      courseInfo: {
        name: '课程名称'
      },
      chapters: [],
      catalogSearch: '',
      selectedNode: null, // { type: 'section', data: {}, ... }
      currentChapter: null, // 当前选中的章节（用于添加小节和高亮）
      saving: false,
      hasChanges: false,
      uploadUrl: '/api/upload',
      newKnowledgePoint: '',
      showKnowledgeInput: false,
      nextChapterId: 1,
      nextSectionId: 1,
      nextBlockId: 1,
      quizDialogVisible: false,
      currentQuizBlock: null,
      moveDialogVisible: false,
      moveType: '', // 'chapter' 或 'section'
      moveSourceItem: null,
      moveSourceChapter: null, // 仅用于小节移动
      moveSourceIndex: null,
      moveTargetChapter: null,
      moveTargetPosition: 'after' // 'before' 或 'after'
    }
  },
  computed: {
    filteredChapters() {
      if (!this.catalogSearch) {
        return this.chapters
      }
      const keyword = this.catalogSearch.toLowerCase()
      return this.chapters.filter(chapter => {
        const titleMatch = chapter.title.toLowerCase().includes(keyword)
        const sectionMatch = chapter.sections.some(s => s.title.toLowerCase().includes(keyword))
        return titleMatch || sectionMatch
      })
    }
  },
  mounted() {
    this.courseId = this.$route.params.id
    
    // 检查是否从作业创建页面返回
    const savedState = sessionStorage.getItem('chapterEditorState')
    if (savedState && this.$route.query.from === 'homework-create') {
      const state = JSON.parse(savedState)
      this.chapters = state.chapters || []
      this.selectedNode = state.selectedNode
      this.currentChapter = state.currentChapter
      this.courseInfo = state.courseInfo || { name: '未命名课程' }
      
      // 确保所有章节和小节都有 title
      this.chapters.forEach(chapter => {
        if (!chapter.title) chapter.title = ''
        if (!chapter.sections) chapter.sections = []
        chapter.sections.forEach(section => {
          if (!section.title) section.title = ''
          if (!section.knowledgePoints) section.knowledgePoints = []
          if (!section.contentBlocks) section.contentBlocks = []
        })
      })
      
      // 如果有返回的作业ID，关联到对应的测验块
      const homeworkId = this.$route.query.homeworkId
      const blockId = parseInt(this.$route.query.blockId)
      
      if (homeworkId && blockId) {
        // 查找对应的测验块并更新
        for (const chapter of this.chapters) {
          for (const section of chapter.sections) {
            const block = section.contentBlocks.find(b => b.id === blockId)
            if (block && block.type === 'quiz') {
              block.linkedHomeworkId = homeworkId
              block.quizCreated = true
              this.markChanged()
              this.$message.success('测验已关联作业')
              break
            }
          }
        }
      }
      
      // 清除保存的状态
      sessionStorage.removeItem('chapterEditorState')
    } else {
      this.loadCourseData()
    }
  },
  beforeRouteLeave(to, from, next) {
    if (this.hasChanges) {
      this.$confirm('有未保存的修改，确定要离开吗？', '提示', {
        confirmButtonText: '保存并离开',
        cancelButtonText: '放弃修改',
        type: 'warning'
      }).then(() => {
        this.saveAll().then(() => {
          next()
        }).catch(err => {
          console.error('保存失败:', err)
          next(false) // 保存失败，取消离开
        })
      }).catch(() => {
        next() // 用户选择放弃修改
      })
    } else {
      next()
    }
  },
  methods: {
    goBack() {
      if (this.hasChanges) {
        this.$confirm('有未保存的修改，确定要返回吗？', '提示', {
          confirmButtonText: '保存并返回',
          cancelButtonText: '放弃修改',
          type: 'warning'
        }).then(() => {
          this.saveAll().then(() => {
            this.$router.push(`/teacher/course/${this.courseId}`)
          }).catch(err => {
            console.error('保存失败:', err)
            // 保存失败不返回
          })
        }).catch(() => {
          this.$router.push(`/teacher/course/${this.courseId}`)
        })
      } else {
        this.$router.push(`/teacher/course/${this.courseId}`)
      }
    },

    loadCourseData() {
      this.courseInfo = {
        name: 'Vue.js 从入门到精通'
      }

      // 新数据结构：小节下有 contentBlocks 数组
      this.chapters = [
        {
          id: 1,
          title: 'Vue 基础入门',
          collapsed: false,
          sections: [
            {
              id: 1,
              title: 'Vue 简介与安装',
              knowledgePoints: ['Vue框架', '环境搭建', 'CLI工具'],
              contentBlocks: [
                {
                  id: 1,
                  type: 'video',
                  videoUrl: '/videos/1.mp4',
                  videoName: 'vue-intro.mp4',
                  watchPercent: 80
                },
                {
                  id: 2,
                  type: 'text',
                  textContent: '本节将介绍Vue的核心概念和开发环境搭建...'
                }
              ]
            },
            {
              id: 2,
              title: '模板语法',
              knowledgePoints: ['插值表达式', '指令'],
              contentBlocks: [
                {
                  id: 3,
                  type: 'document',
                  docUrl: '/docs/template.pdf',
                  docName: 'template-syntax.pdf',
                  displayName: 'Vue 模板语法详解'
                }
              ]
            }
          ]
        },
        {
          id: 2,
          title: '组件化开发',
          collapsed: false,
          sections: [
            {
              id: 3,
              title: '组件基础',
              knowledgePoints: ['组件定义', 'Props', 'Events'],
              contentBlocks: []
            }
          ]
        }
      ]

      this.nextChapterId = Math.max(...this.chapters.map(c => c.id), 0) + 1
      const allSections = this.chapters.flatMap(c => c.sections)
      this.nextSectionId = Math.max(...allSections.map(s => s.id), 0) + 1
      const allBlocks = allSections.flatMap(s => s.contentBlocks)
      this.nextBlockId = Math.max(...allBlocks.map(b => b.id), 0) + 1
    },

    markChanged() {
      this.hasChanges = true
    },

    toggleChapter(chapter) {
      // 切换折叠状态
      chapter.collapsed = !chapter.collapsed
      this.currentChapter = chapter
      // 不改变 selectedNode，保持小节页面显示
    },

    selectSection(section, chapter, chapterIndex, sectionIndex) {
      this.currentChapter = chapter
      this.selectedNode = {
        type: 'section',
        id: section.id,
        data: section,
        chapter: chapter,
        chapterIndex: chapterIndex,
        sectionIndex: sectionIndex
      }
    },

    addChapter() {
      const newChapter = {
        id: this.nextChapterId++,
        title: '',
        collapsed: false,
        sections: []
      }
      this.chapters.push(newChapter)
      this.currentChapter = newChapter
      this.markChanged()
      this.$message.success('已添加新章节')
    },

    addSectionToCurrentChapter() {
      if (!this.currentChapter) {
        this.$message.warning('请先选择一个章节')
        return
      }
      this.addSection(this.currentChapter)
    },

    deleteChapter(index) {
      const chapter = this.chapters[index]
      this.$confirm(
        `确定删除"${chapter.title || '未命名章节'}"吗？该章节下的所有小节也将被删除。`,
        '删除章节',
        {
          confirmButtonText: '确定删除',
          cancelButtonText: '取消',
          type: 'warning'
        }
      ).then(() => {
        this.chapters.splice(index, 1)
        this.markChanged()
        if (this.currentChapter && this.currentChapter.id === chapter.id) {
          this.currentChapter = null
        }
        if (this.selectedNode && this.selectedNode.chapter && this.selectedNode.chapter.id === chapter.id) {
          this.selectedNode = null
        }
        this.$message.success('章节已删除')
      }).catch(() => {})
    },

    handleChapterCommand(command, chapter) {
      const index = this.chapters.indexOf(chapter)
      switch (command) {
        case 'rename':
          this.$prompt('请输入新的章节名称', '重命名章节', {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            inputValue: chapter.title,
            inputPattern: /.+/,
            inputErrorMessage: '章节名称不能为空'
          }).then(({ value }) => {
            chapter.title = value
            this.markChanged()
            this.$message.success('重命名成功')
          }).catch(() => {})
          break
        case 'move':
          this.showMoveChapterDialog(chapter, index)
          break
        case 'delete':
          this.deleteChapter(index)
          break
      }
    },

    showMoveChapterDialog(chapter, currentIndex) {
      this.moveType = 'chapter'
      this.moveSourceItem = chapter
      this.moveSourceIndex = currentIndex
      this.moveTargetChapter = null
      this.moveTargetPosition = 'after'
      this.moveDialogVisible = true
    },

    onChapterDragEnd() {
      this.markChanged()
    },

    addSection(chapter) {
      const newSection = {
        id: this.nextSectionId++,
        title: '',
        knowledgePoints: [],
        contentBlocks: []
      }
      chapter.sections.push(newSection)
      this.markChanged()
      
      const chapterIndex = this.chapters.indexOf(chapter)
      const sectionIndex = chapter.sections.length - 1
      this.selectSection(newSection, chapter, chapterIndex, sectionIndex)
      this.$message.success('已添加新小节')
    },

    deleteSection(chapter, sectionIndex) {
      const section = chapter.sections[sectionIndex]
      this.$confirm(
        `确定删除小节"${section.title || '未命名小节'}"吗？该小节下的所有内容块也将被删除。`,
        '删除小节',
        {
          confirmButtonText: '确定删除',
          cancelButtonText: '取消',
          type: 'warning'
        }
      ).then(() => {
        chapter.sections.splice(sectionIndex, 1)
        this.markChanged()
        if (this.selectedNode && this.selectedNode.id === section.id) {
          this.selectedNode = null
        }
        this.$message.success('小节已删除')
      }).catch(() => {})
    },

    handleSectionCommand(command, section, chapter, sectionIndex) {
      switch (command) {
        case 'rename':
          this.$prompt('请输入新的小节名称', '重命名小节', {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            inputValue: section.title,
            inputPattern: /.+/,
            inputErrorMessage: '小节名称不能为空'
          }).then(({ value }) => {
            section.title = value
            this.markChanged()
            this.$message.success('重命名成功')
          }).catch(() => {})
          break
        case 'move':
          this.showMoveSectionDialog(section, chapter, sectionIndex)
          break
        case 'delete':
          this.deleteSection(chapter, sectionIndex)
          break
      }
    },

    showMoveSectionDialog(section, currentChapter, currentSectionIndex) {
      this.moveType = 'section'
      this.moveSourceItem = section
      this.moveSourceChapter = currentChapter
      this.moveSourceIndex = currentSectionIndex
      this.moveTargetChapter = null
      this.moveTargetPosition = '0' // 默认插入到第一个位置
      this.moveDialogVisible = true
    },

    confirmMove() {
      if (!this.moveTargetChapter) {
        this.$message.warning('请选择目标章节')
        return
      }

      if (this.moveType === 'chapter') {
        // 移动章节
        const sourceIndex = this.moveSourceIndex
        const targetIndex = this.chapters.indexOf(this.moveTargetChapter)

        if (sourceIndex === targetIndex) {
          this.$message.info('目标位置与当前位置相同')
          this.moveDialogVisible = false
          return
        }

        // 移除原位置
        const [chapter] = this.chapters.splice(sourceIndex, 1)
        
        // 计算新的插入位置
        let insertIndex = this.chapters.indexOf(this.moveTargetChapter)
        if (this.moveTargetPosition === 'after') {
          insertIndex++
        }
        
        // 插入到新位置
        this.chapters.splice(insertIndex, 0, chapter)
        
        this.markChanged()
        this.$message.success('章节移动成功')
        this.moveDialogVisible = false
      } else if (this.moveType === 'section') {
        // 移动小节
        const targetIndex = parseInt(this.moveTargetPosition)
        
        // 移除原位置的小节
        const [section] = this.moveSourceChapter.sections.splice(this.moveSourceIndex, 1)
        
        // 如果是在同一章节内移动，需要调整目标索引
        let finalTargetIndex = targetIndex
        if (this.moveSourceChapter.id === this.moveTargetChapter.id && this.moveSourceIndex < targetIndex) {
          finalTargetIndex--
        }
        
        // 插入到目标章节
        this.moveTargetChapter.sections.splice(finalTargetIndex, 0, section)
        
        this.markChanged()
        this.$message.success('小节移动成功')
        this.moveDialogVisible = false
      }
    },

    previewCourse() {
      // 保存当前编辑状态
      const previewData = {
        courseInfo: this.courseInfo || { name: '未命名课程' },
        chapters: this.chapters || []
      }
      sessionStorage.setItem('coursePreviewData', JSON.stringify(previewData))
      
      // 跳转到教师课程预览页（使用教师专用路由）
      this.$router.push({
        path: `/teacher/course/${this.courseId}/preview`,
        query: { preview: 'true' }
      }).catch(err => {
        console.error('路由跳转失败:', err)
      })
    },

    showAddKnowledgeInput() {
      this.showKnowledgeInput = true
      this.newKnowledgePoint = ''
      this.$nextTick(() => {
        this.$refs.knowledgeInput && this.$refs.knowledgeInput.focus()
      })
    },

    confirmAddKnowledgePoint(section) {
      if (!this.newKnowledgePoint.trim()) {
        this.showKnowledgeInput = false
        return
      }
      if (!section.knowledgePoints.includes(this.newKnowledgePoint.trim())) {
        section.knowledgePoints.push(this.newKnowledgePoint.trim())
        this.markChanged()
        this.$message.success('知识点已添加')
      }
      this.newKnowledgePoint = ''
      this.showKnowledgeInput = false
    },

    removeKnowledgePoint(section, index) {
      section.knowledgePoints.splice(index, 1)
      this.markChanged()
    },

    // 内容块管理
    addContentBlock(type) {
      if (!this.selectedNode || this.selectedNode.type !== 'section') {
        this.$message.warning('请先选择一个小节')
        return
      }

      const blockTemplates = {
        video: {
          id: this.nextBlockId++,
          type: 'video',
          videoUrl: '',
          videoName: '',
          watchPercent: 80
        },
        document: {
          id: this.nextBlockId++,
          type: 'document',
          docUrl: '',
          docName: '',
          displayName: ''
        },
        text: {
          id: this.nextBlockId++,
          type: 'text',
          textContent: ''
        },
        quiz: {
          id: this.nextBlockId++,
          type: 'quiz',
          quizMode: 'select', // 'select' 或 'create'
          linkedHomeworkId: '',
          quizCreated: false,
          quizTitle: '',
          quizDescription: '',
          questions: []
        }
      }

      const newBlock = blockTemplates[type]
      this.selectedNode.data.contentBlocks.push(newBlock)
      this.markChanged()
      this.$message.success(`已添加${this.getBlockTypeName(type)}块`)
    },

    deleteContentBlock(section, blockIndex) {
      this.$confirm('确定删除该内容块吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        section.contentBlocks.splice(blockIndex, 1)
        this.markChanged()
        this.$message.success('内容块已删除')
      }).catch(() => {})
    },

    getBlockTypeName(type) {
      const typeMap = {
        video: '视频',
        document: '文档',
        text: '文字',
        quiz: '测验'
      }
      return typeMap[type] || '未知'
    },

    getBlockTagType(type) {
      const tagMap = {
        video: 'success',
        document: 'warning',
        text: 'info',
        quiz: 'danger'
      }
      return tagMap[type] || 'info'
    },

    // 文件上传
    handleVideoUpload(response, file, block) {
      block.videoUrl = response.url || '/mock/video'
      block.videoName = file.name
      this.markChanged()
      this.$message.success('视频上传成功')
    },

    handleDocUpload(response, file, block) {
      block.docUrl = response.url || '/mock/doc'
      block.docName = file.name
      if (!block.displayName) {
        block.displayName = file.name
      }
      this.markChanged()
      this.$message.success('文档上传成功')
    },

    removeBlockFile(block) {
      if (block.type === 'video') {
        block.videoUrl = ''
        block.videoName = ''
      } else if (block.type === 'document') {
        block.docUrl = ''
        block.docName = ''
      }
      this.markChanged()
    },

    // 测验相关
    handleQuizModeChange(block) {
      block.linkedHomeworkId = ''
      block.quizCreated = false
      this.markChanged()
    },

    createNewQuiz(block) {
      this.currentQuizBlock = block
      // 保存当前编辑状态到 sessionStorage
      sessionStorage.setItem('chapterEditorState', JSON.stringify({
        chapters: this.chapters,
        selectedNode: this.selectedNode,
        currentChapter: this.currentChapter,
        courseId: this.courseId,
        courseInfo: this.courseInfo
      }))
      // 跳转到作业创建页面
      this.$router.push({
        path: '/teacher/homework/create',
        query: { 
          from: 'chapter-editor',
          blockId: block.id,
          courseId: this.courseId
        }
      })
    },

    editQuiz(block) {
      // 如果已经关联了作业，跳转到编辑页面
      if (block.linkedHomeworkId) {
        this.$router.push({
          path: '/teacher/homework/create',
          query: { 
            id: block.linkedHomeworkId,
            from: 'chapter-editor',
            blockId: block.id,
            courseId: this.courseId
          }
        })
      } else {
        this.createNewQuiz(block)
      }
    },

    confirmCreateQuiz() {
      if (!this.currentQuizBlock.quizTitle) {
        this.$message.warning('请输入测验标题')
        return
      }
      this.currentQuizBlock.quizCreated = true
      this.quizDialogVisible = false
      this.markChanged()
      this.$message.success('测验创建成功')
    },

    async saveAll() {
      // 不再强制验证标题，允许未命名的章节和小节
      this.saving = true
      try {
        await new Promise(resolve => setTimeout(resolve, 1000))
        console.log('保存章节数据:', JSON.stringify(this.chapters, null, 2))
        this.$message.success('保存成功')
        this.hasChanges = false
      } catch (error) {
        this.$message.error('保存失败，请重试')
        throw error
      } finally {
        this.saving = false
      }
    },

    numberToChinese(num) {
      const chineseNums = ['零', '一', '二', '三', '四', '五', '六', '七', '八', '九', '十']
      if (num <= 10) {
        return chineseNums[num]
      }
      if (num < 20) {
        return '十' + chineseNums[num - 10]
      }
      const tens = Math.floor(num / 10)
      const ones = num % 10
      return chineseNums[tens] + '十' + (ones > 0 ? chineseNums[ones] : '')
    }
  }
}
</script>

<style lang="scss" scoped>
.chapter-editor {
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: #f5f7fa;
}

.editor-header {
  background: white;
  padding: 15px 30px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #e4e7ed;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);

  .header-left {
    display: flex;
    align-items: center;
    gap: 20px;

    .course-title {
      margin: 0;
      font-size: 18px;
      color: #303133;
    }
  }

  .header-right {
    display: flex;
    gap: 10px;
  }
}

.editor-body {
  flex: 1;
  display: flex;
  overflow: hidden;
  position: relative;
}

/* ========== 左侧目录树 - 固定，不滚动 ========== */
.catalog-tree {
  width: 25%;
  background: white;
  border-right: 1px solid #e4e7ed;
  display: flex;
  flex-direction: column;
  overflow: hidden;

  .tree-header {
    padding: 15px;
    border-bottom: 1px solid #e4e7ed;

    .tree-actions {
      display: flex;
      justify-content: space-between;
      gap: 8px;
      margin-top: 10px;
    }
  }

  .tree-content {
    flex: 1;
    overflow-y: auto;
    padding: 10px;

    &::-webkit-scrollbar {
      width: 6px;
    }

    &::-webkit-scrollbar-thumb {
      background: #dcdfe6;
      border-radius: 3px;
    }
  }

  .tree-empty {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100%;
    color: #909399;
  }

  .tree-chapter {
    margin-bottom: 5px;

    .tree-chapter-header {
      display: flex;
      align-items: center;
      padding: 10px;
      border-radius: 4px;
      cursor: pointer;
      transition: all 0.3s;
      position: relative;

      &:hover {
        background: #f5f7fa;

        .tree-more-btn {
          opacity: 1;
        }
      }

      &.active {
        background: #ecf5ff;
        color: #409eff;
        font-weight: bold;
      }

      &.collapsed {
        .chapter-icon {
          color: #909399;
        }
      }

      .tree-drag-handle {
        cursor: move;
        margin-right: 8px;
        color: #c0c4cc;
        font-size: 14px;
      }

      .chapter-icon {
        margin-right: 8px;
        color: #409eff;
        font-size: 16px;
        transition: all 0.3s;
      }

      .chapter-title {
        flex: 1;
        font-size: 14px;
      }

      .section-count {
        font-size: 12px;
        color: #909399;
        margin-right: 8px;
      }

      .tree-more-btn {
        opacity: 0;
        padding: 4px 8px;
        border-radius: 4px;
        transition: all 0.3s;

        &:hover {
          background: #e4e7ed;
        }

        i {
          transform: rotate(90deg);
          font-size: 16px;
          color: #606266;
        }
      }
    }

    .tree-sections {
      padding-left: 20px;
    }

    .tree-section {
      display: flex;
      align-items: center;
      padding: 8px 10px;
      border-radius: 4px;
      cursor: pointer;
      margin: 2px 0;
      transition: all 0.3s;
      position: relative;

      &:hover {
        background: #f5f7fa;

        .tree-more-btn {
          opacity: 1;
        }
      }

      &.active {
        background: #e1f3d8;
        color: #67c23a;
        font-weight: bold;
      }

      .tree-section-drag-handle {
        cursor: move;
        margin-right: 8px;
        color: #c0c4cc;
        font-size: 12px;
      }

      .section-icon {
        margin-right: 8px;
        font-size: 14px;
        color: #67c23a;
      }

      .section-title {
        flex: 1;
        font-size: 13px;
      }

      .block-count {
        font-size: 11px;
        color: #909399;
        margin-right: 8px;
      }

      .tree-more-btn {
        opacity: 0;
        padding: 2px 6px;
        border-radius: 4px;
        transition: all 0.3s;

        &:hover {
          background: #e4e7ed;
        }

        i {
          transform: rotate(90deg);
          font-size: 14px;
          color: #606266;
        }
      }
    }
  }

  .tree-footer {
    padding: 15px;
    border-top: 1px solid #e4e7ed;
  }
}

/* ========== 右侧节点容器 - 75%，只有内容区域滚动 ========== */
.node-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: #f5f7fa;
  overflow: hidden;

  /* 顶部固定工具栏 */
  .content-toolbar-fixed {
    background: white;
    padding: 15px 20px;
    border-bottom: 2px solid #e4e7ed;
    display: flex;
    align-items: center;
    gap: 15px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    flex-shrink: 0;

    .toolbar-label {
      font-weight: bold;
      color: #606266;
      font-size: 14px;
    }

    ::v-deep .el-button-group {
      .el-button {
        &:hover {
          transform: translateY(-1px);
          box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
      }
    }
  }

  .editor-empty {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    color: #909399;
    overflow-y: auto;

    p {
      margin-top: 20px;
      font-size: 14px;
    }
  }
}

/* 章节编辑区 */
.chapter-editor-area {
  flex: 1;
  overflow-y: auto;
  padding: 20px;

  .node-header {
    margin-bottom: 20px;

    .node-title-area {
      margin-bottom: 15px;

      ::v-deep .el-input-group__prepend {
        background: #409eff;
        color: white;
        font-weight: bold;
      }
    }

    .node-actions {
      display: flex;
      gap: 10px;
    }
  }

  .chapter-sections-list {
    background: white;
    padding: 30px;
    border-radius: 4px;
  }
}

/* 小节编辑区（核心） */
.section-editor-area {
  flex: 1;
  overflow-y: auto;
  padding: 20px;

  .node-header {
    margin-bottom: 15px;

    .node-title-area {
      margin-bottom: 10px;

      ::v-deep .el-input-group__prepend {
        background: #67c23a;
        color: white;
        font-weight: bold;
      }
    }

    .node-actions {
      display: flex;
      justify-content: flex-end;
    }
  }

  .knowledge-area {
    background: white;
    padding: 15px 20px;
    border-radius: 4px;
    margin-bottom: 20px;
    display: flex;
    align-items: center;

    .knowledge-label {
      font-weight: bold;
      color: #606266;
      margin-right: 15px;
      white-space: nowrap;
    }

    .knowledge-tags {
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      gap: 8px;
    }
  }

  /* 内容块容器 */
  .content-blocks-container {
    margin-bottom: 20px;

    .content-block-card {
      background: white;
      border-radius: 8px;
      padding: 20px;
      margin-bottom: 15px;
      box-shadow: 0 2px 8px rgba(0,0,0,0.08);
      transition: all 0.3s;

      &:hover {
        box-shadow: 0 4px 12px rgba(0,0,0,0.12);
      }

      .block-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 15px;
        padding-bottom: 12px;
        border-bottom: 2px solid #f5f7fa;

        .block-header-left {
          display: flex;
          align-items: center;
          gap: 10px;

          .block-drag-handle {
            cursor: move;
            color: #c0c4cc;
            font-size: 18px;
            transition: color 0.3s;

            &:hover {
              color: #909399;
            }
          }

          .block-order {
            color: #909399;
            font-size: 13px;
          }
        }

        .block-delete-btn {
          color: #f56c6c;
          font-size: 13px;

          &:hover {
            color: #f56c6c;
            background: #fef0f0;
          }
        }
      }

      .block-content {
        .video-uploader,
        .doc-uploader {
          ::v-deep .el-upload-dragger {
            width: 100%;
            padding: 40px 20px;
          }
        }

        .file-preview {
          display: flex;
          align-items: center;
          gap: 15px;
          padding: 15px;
          background: #f9fafc;
          border-radius: 4px;
          border: 1px solid #e4e7ed;

          i {
            font-size: 28px;
            color: #409eff;
          }

          span {
            flex: 1;
            font-weight: bold;
            color: #303133;
          }
        }

        .quiz-create-area {
          .quiz-info {
            ::v-deep .el-alert {
              margin-bottom: 10px;
            }
          }
        }
      }
    }
  }

  /* 移动对话框样式 */
  .move-dialog-content {
    .el-form-item {
      margin-bottom: 18px;
    }
  }
}
</style>
