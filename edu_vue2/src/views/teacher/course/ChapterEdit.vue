<template>
  <div class="chapter-editor">
    <!-- 顶部标题栏 -->
    <div class="editor-header">
      <div class="header-left">
        <el-button icon="el-icon-arrow-left" @click="goBack">返回</el-button>
        <h2 class="course-title">{{ courseInfo.title || '课程名称' }}</h2>
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
            <el-button size="small" icon="el-icon-picture" @click="addContentBlock('image')">
              图片
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
                @blur="updateSectionTitle"
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
              <template v-for="(pointId, idx) in selectedNode.data.knowledgePoints">
                <el-tag
                  v-if="getKnowledgePointNameById(pointId)"
                  :key="pointId"
                  closable
                  @close="removeKnowledgePoint(selectedNode.data, idx)"
                  style="margin-right: 8px;"
                  type="success"
                >
                  {{ getKnowledgePointNameById(pointId) }}
                </el-tag>
              </template>
              <span v-if="selectedNode.data.knowledgePoints.length > 0 && knowledgeTreeData.length === 0" class="empty-hint" style="color: #909399; font-size: 12px;">加载中...</span>
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
                      <div v-if="!block.videoUrl" class="custom-upload-area" @click="triggerFileInput(block, 'video')">
                        <div v-if="block.uploading" class="upload-loading">
                          <i class="el-icon-loading"></i>
                          <div>上传中... {{ block.uploadProgress || 0 }}%</div>
                        </div>
                        <div v-else class="upload-placeholder">
                          <i class="el-icon-upload"></i>
                          <div class="el-upload__text">拖拽视频文件到此处，或<em>点击上传</em></div>
                          <div class="el-upload__tip">支持 MP4、WebM、OGG、MOV 格式，最大 500MB</div>
                        </div>
                        <input
                          type="file"
                          :ref="'fileInput_' + block.id"
                          style="display: none;"
                          accept="video/mp4,video/webm,video/ogg,video/quicktime"
                          @change="handleFileChange($event, block, 'video')"
                        />
                      </div>
                      <div v-else class="video-preview-container">
                        <video 
                          :src="getMediaUrl(block.videoUrl)" 
                          controls 
                          class="video-preview"
                          @error="handleMediaError"
                        >
                          您的浏览器不支持视频播放
                        </video>
                        <div class="file-info-bar">
                          <span class="file-name">
                            <i class="el-icon-video-camera"></i>
                            {{ block.videoName }}
                          </span>
                          <span class="file-size">{{ formatFileSize(block.fileSize) }}</span>
                          <el-button 
                            type="text" 
                            @click="removeBlockFile(block)" 
                            style="color: #f56c6c;"
                          >
                            移除
                          </el-button>
                        </div>
                      </div>
                    </el-form-item>
                  </el-form>
                </div>

                <!-- 文档块 -->
                <div v-else-if="block.type === 'document'" class="block-content">
                  <el-form label-width="120px" size="small">
                    <el-form-item label="课件文件">
                      <div v-if="!block.docUrl" class="custom-upload-area" @click="triggerFileInput(block, 'file')">
                        <div v-if="block.uploading" class="upload-loading">
                          <i class="el-icon-loading"></i>
                          <div>上传中... {{ block.uploadProgress || 0 }}%</div>
                        </div>
                        <div v-else class="upload-placeholder">
                          <i class="el-icon-upload"></i>
                          <div class="el-upload__text">拖拽课件文件到此处，或<em>点击上传</em></div>
                          <div class="el-upload__tip">支持 PDF、PPT、Word、Excel、压缩包等，最大 50MB</div>
                        </div>
                        <input
                          type="file"
                          :ref="'fileInput_' + block.id"
                          style="display: none;"
                          accept=".pdf,.doc,.docx,.ppt,.pptx,.xls,.xlsx,.zip,.rar,.txt"
                          @change="handleFileChange($event, block, 'file')"
                        />
                      </div>
                      <div v-else class="file-preview">
                        <i class="el-icon-document"></i>
                        <span>{{ block.docName }}</span>
                        <span class="file-size">{{ formatFileSize(block.fileSize) }}</span>
                        <el-button type="text" @click="removeBlockFile(block)" style="color: #f56c6c;">移除</el-button>
                      </div>
                    </el-form-item>
                    <el-form-item label="文档重命名" v-if="block.docUrl">
                      <el-input
                        v-model="block.displayName"
                        placeholder="为学生显示的文档名称"
                        @change="markChanged"
                      ></el-input>
                    </el-form-item>
                  </el-form>
                </div>

                <!-- 图片块 -->
                <div v-else-if="block.type === 'image'" class="block-content">
                  <el-form label-width="120px" size="small">
                    <el-form-item label="图片文件">
                      <div v-if="!block.imageUrl" class="custom-upload-area" @click="triggerFileInput(block, 'image')">
                        <div v-if="block.uploading" class="upload-loading">
                          <i class="el-icon-loading"></i>
                          <div>上传中... {{ block.uploadProgress || 0 }}%</div>
                        </div>
                        <div v-else class="upload-placeholder">
                          <i class="el-icon-upload"></i>
                          <div class="el-upload__text">拖拽图片文件到此处，或<em>点击上传</em></div>
                          <div class="el-upload__tip">支持 JPG、PNG、GIF、WebP等，最大 10MB</div>
                        </div>
                        <input
                          type="file"
                          :ref="'fileInput_' + block.id"
                          style="display: none;"
                          accept="image/jpeg,image/jpg,image/png,image/gif,image/webp"
                          @change="handleFileChange($event, block, 'image')"
                        />
                      </div>
                      <div v-else class="image-preview-container">
                        <img 
                          :src="getMediaUrl(block.imageUrl)" 
                          class="image-preview"
                          @error="handleMediaError"
                        />
                        <div class="file-info-bar">
                          <span class="file-name">
                            <i class="el-icon-picture"></i>
                            {{ block.imageName }}
                          </span>
                          <span class="file-size">{{ formatFileSize(block.fileSize) }}</span>
                          <el-button 
                            type="text" 
                            @click="removeBlockFile(block)" 
                            style="color: #f56c6c;"
                          >
                            移除
                          </el-button>
                        </div>
                      </div>
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

    <!-- 知识点选择弹窗 -->
    <knowledge-point-selector
      :visible.sync="knowledgeDialogVisible"
      v-model="selectedKnowledgePoints"
      :knowledge-tree="knowledgeTreeData"
      @confirm="handleKnowledgeConfirm"
      @add-root="handleAddRootKnowledge"
      @add-child="handleAddChildKnowledge"
      @edit-node="handleEditKnowledge"
      @delete-node="handleDeleteKnowledge"
    />

    <!-- 题库选择弹窗 -->
    <el-dialog
      title="选择题库"
      :visible.sync="questionBankDialogVisible"
      width="700px"
      :close-on-click-modal="false"
    >
      <div v-loading="questionBankLoading">
        <el-input
          v-model="questionBankSearchText"
          placeholder="搜索题库名称"
          prefix-icon="el-icon-search"
          clearable
          style="margin-bottom: 15px;"
        />

        <div style="max-height: 450px; overflow-y: auto;">
          <el-row :gutter="15">
            <el-col
              v-for="bank in filteredQuestionBanks"
              :key="bank.id"
              :span="24"
              style="margin-bottom: 10px;"
            >
              <el-card
                shadow="hover"
                :body-style="{ padding: '15px' }"
                :class="['question-bank-card', { 'selected': selectedQuestionBank && selectedQuestionBank.id === bank.id }]"
                @click.native="selectQuestionBank(bank)"
              >
                <div style="display: flex; align-items: center; justify-content: space-between;">
                  <div style="flex: 1;">
                    <div style="display: flex; align-items: center; margin-bottom: 8px;">
                      <i class="el-icon-folder" style="font-size: 20px; color: #409eff; margin-right: 10px;"></i>
                      <span style="font-size: 16px; font-weight: bold; color: #303133;">{{ bank.name }}</span>
                    </div>
                    <div style="color: #909399; font-size: 13px; margin-bottom: 5px;">
                      {{ bank.description }}
                    </div>
                    <div style="display: flex; align-items: center; gap: 15px;">
                      <el-tag size="small" type="info">
                        <i class="el-icon-document"></i> {{ bank.question_count }} 道题目
                      </el-tag>
                    </div>
                  </div>
                  <div v-if="selectedQuestionBank && selectedQuestionBank.id === bank.id">
                    <i class="el-icon-check" style="font-size: 24px; color: #67c23a;"></i>
                  </div>
                </div>
              </el-card>
            </el-col>
          </el-row>

          <el-empty v-if="filteredQuestionBanks.length === 0" description="暂无题库" />
        </div>
      </div>
      <span slot="footer">
        <el-button @click="questionBankDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="confirmSelectQuestionBank" :disabled="!selectedQuestionBank">确定</el-button>
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
import KnowledgePointSelector from '@/components/common/KnowledgePointSelector.vue'
import { 
  getCourseChapters, 
  getLessonDetail, 
  createChapter,
  updateChapter,
  deleteChapter,
  createLesson,
  updateLesson,
  deleteLesson,
  saveContentBlocks,
  uploadContentBlockFile
} from '@/api/teacher'
import {
  getKnowledgePoints,
  createKnowledgePoint,
  updateKnowledgePoint,
  deleteKnowledgePoint,
  getObjectKnowledgePoints,
  attachKnowledgePoints,
  detachKnowledgePoints
} from '@/api/knowledge'

export default {
  name: 'ChapterEditor',
  components: {
    draggable,
    KnowledgePointSelector
  },
  data() {
    return {
      courseId: null,
      loading: false,
      courseInfo: {
        id: null,
        title: '',
        teacher_name: ''
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
      isNavigatingAway: false, // 标记是否正在离开页面
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
      moveTargetPosition: 'after', // 'before' 或 'after'
      // 知识点选择弹窗
      knowledgeDialogVisible: false,
      knowledgeTreeData: [],
      currentSection: null, // 当前操作的小节
      knowledgeLoading: false,
      selectedKnowledgePoints: [], // v-model 绑定的已选知识点
      // 题库选择弹窗
      questionBankDialogVisible: false,
      questionBankList: [],
      questionBankSearchText: '',
      selectedQuestionBank: null,
      questionBankLoading: false
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
    },
    filteredQuestionBanks() {
      if (!this.questionBankSearchText) {
        return this.questionBankList
      }
      const keyword = this.questionBankSearchText.toLowerCase()
      return this.questionBankList.filter(bank => 
        bank.name.toLowerCase().includes(keyword) || 
        bank.description.toLowerCase().includes(keyword)
      )
    }
  },
  mounted() {
    this.courseId = this.$route.params.courseId
    
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
      // 加载课程数据
      this.loadCourseData().then(() => {
        // 如果有lessonId参数,说明是从 Detail.vue 点击课时过来的
        const lessonId = this.$route.query.lessonId
        const chapterId = this.$route.query.chapterId
        
        if (lessonId && chapterId) {
          // 查找对应的章节和小节
          for (let chapterIndex = 0; chapterIndex < this.chapters.length; chapterIndex++) {
            const chapter = this.chapters[chapterIndex]
            if (chapter.id == chapterId) {
              // 展开章节
              chapter.collapsed = false
              this.currentChapter = chapter
              
              // 查找小节
              for (let sectionIndex = 0; sectionIndex < chapter.sections.length; sectionIndex++) {
                const section = chapter.sections[sectionIndex]
                if (section.id == lessonId) {
                  // 选中小节
                  this.selectSection(section, chapter, chapterIndex, sectionIndex)
                  break
                }
              }
              break
            }
          }
        }
      })
    }
  },
  beforeRouteLeave(to, from, next) {
    // 如果是通过goBack离开，不再弹窗
    if (this.isNavigatingAway) {
      next()
      return
    }
    
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
    const targetPath = `/teacher/courses/${this.courseId}`

    if (this.hasChanges) {
      this.$confirm('有未保存的修改，确定要返回吗？', '提示', {
        confirmButtonText: '保存并返回',
        cancelButtonText: '放弃修改',
        type: 'warning'
      }).then(() => {
        // 保存并跳转
        this.saveAll().then(() => {
          this.isNavigatingAway = true // 设置标记
          this.$router.push(targetPath)
        }).catch(err => {
          console.error('保存失败:', err)
        })
      }).catch(() => {
        // 放弃修改并跳转
        this.isNavigatingAway = true // 设置标记
        this.$router.push(targetPath)
      })
    } else {
      // 无修改直接跳转
      this.isNavigatingAway = true // 设置标记
      this.$router.push(targetPath)
    }
  },

    async loadCourseData() {
      if (!this.courseId) {
        this.$message.error('课程ID不存在')
        return
      }

      this.loading = true
      try {
        const response = await getCourseChapters(this.courseId)
        
        console.log('loadCourseData response:', response)
        
        // 更新课程信息
        this.courseInfo = {
          id: this.courseId,
          title: response.course_title || '',
          teacher_name: response.teacher_name || ''
        }
        
        // 映射后端数据结构
        this.chapters = (response.chapters || []).map((chapter) => ({
          id: chapter.id || this.nextChapterId++,
          title: chapter.title || '',
          collapsed: false,
          sections: (chapter.lessons || []).map((lesson) => ({
            id: lesson.id || this.nextSectionId++,
            title: lesson.title || '',
            knowledgePoints: [], // 知识点将在选中课时时加载
            contentBlocks: [] // 课时内容懒加载,点击时再请求
          }))
        }))
        
        // 如果没有章节,初始化为空数组
        if (this.chapters.length === 0) {
          this.chapters = []
          this.$message.info('还没有章节,可以开始创建')
        }
        
        // 更新ID生成器
        if (this.chapters.length > 0) {
          this.nextChapterId = Math.max(...this.chapters.map(c => c.id), 0) + 1
          const allSections = this.chapters.flatMap(c => c.sections)
          if (allSections.length > 0) {
            this.nextSectionId = Math.max(...allSections.map(s => s.id), 0) + 1
          }
        }
        
      } catch (error) {
        console.error('加载章节数据失败:', error)
        this.$message.error('加载章节数据失败')
        // 失败后初始化为空,允许创建新章节
        this.chapters = []
      } finally {
        this.loading = false
      }
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

    async selectSection(section, chapter, chapterIndex, sectionIndex) {
      this.currentChapter = chapter
      
      // 如果课时内容为空且有id(说明是从后端加载的),需要懒加载内容
      if (section.contentBlocks.length === 0 && section.id && !section._contentLoaded) {
        try {
          this.loading = true
          const lessonDetail = await getLessonDetail(this.courseId, section.id)
          
          // 映射后端返回的内容块数据
          section.contentBlocks = (lessonDetail.content_blocks || []).map(block => {
            const mappedBlock = {
              id: block.id || this.nextBlockId++,
              type: this.mapBlockType(block.type),
              order: block.order
            }
            
            // 根据类型映射字段
            switch (block.type) {
              case 'video':
                mappedBlock.videoUrl = block.file_url
                mappedBlock.videoName = block.title
                mappedBlock.watchPercent = 80
                break
              case 'image':
                mappedBlock.imageUrl = block.file_url
                mappedBlock.imageName = block.title
                mappedBlock.fileSize = block.file_size || 0
                break
              case 'file':
                mappedBlock.docUrl = block.file_url
                mappedBlock.docName = block.title
                mappedBlock.displayName = block.title
                break
              case 'rich_text':
                mappedBlock.textContent = block.content?.html || ''
                break
            }
            
            return mappedBlock
          })
          
          // 标记已加载
          section._contentLoaded = true
          
        } catch (error) {
          console.error('加载课时内容失败:', error)
          this.$message.error('加载课时内容失败')
        } finally {
          this.loading = false
        }
      }
      
      // 加载知识点树数据(用于显示知识点名称)
      if (this.knowledgeTreeData.length === 0) {
        try {
          const response = await getKnowledgePoints({
            course_id: this.courseId
          })
          const knowledgePoints = response.data?.knowledge_points || response.knowledge_points || []
          this.knowledgeTreeData = this.addCheckedProperty(knowledgePoints)
        } catch (error) {
          console.error('加载知识点树失败:', error)
        }
      }
      
      // 加载课时的知识点（每次选中都加载，确保数据最新）
      if (section.id) {
        try {
          const kpResponse = await getObjectKnowledgePoints({
            content_type: 'lesson',
            object_id: section.id
          })
          
          const knowledgePoints = kpResponse.data?.knowledge_points || kpResponse.knowledge_points || []
          console.log('加载到的知识点数据:', knowledgePoints)
          
          // 保持知识点为ID数组,支持同名知识点
          section.knowledgePoints = knowledgePoints.map(kp => kp.id)
        } catch (error) {
          console.error('加载知识点失败:', error)
          // 失败时不影响主流程，设置为空数组
          section.knowledgePoints = []
        }
      }
      
      this.selectedNode = {
        type: 'section',
        id: section.id,
        data: section,
        chapter: chapter,
        chapterIndex: chapterIndex,
        sectionIndex: sectionIndex
      }
      
      // 调试日志：检查知识点数据
      console.log('选中课时:', section.title, '知识点:', section.knowledgePoints)
    },

    async addChapter() {
      try {
        this.loading = true
        const response = await createChapter(this.courseId, {
          title: '新章节',
          order: this.chapters.length
        })
        
        console.log('createChapter response:', response)
        
        const newChapter = {
          id: response.chapter_id || response.id,
          title: response.title || '新章节',
          collapsed: false,
          sections: []
        }
        this.chapters.push(newChapter)
        this.currentChapter = newChapter
        this.$message.success('已添加新章节')
      } catch (error) {
        console.error('添加章节失败:', error)
        this.$message.error('添加章节失败')
      } finally {
        this.loading = false
      }
    },

    addSectionToCurrentChapter() {
      if (!this.currentChapter) {
        this.$message.warning('请先选择一个章节')
        return
      }
      this.addSection(this.currentChapter)
    },

    async deleteChapter(index) {
      const chapter = this.chapters[index]
      this.$confirm(
        `确定删除"${chapter.title || '未命名章节'}"吗？该章节下的所有小节也将被删除。`,
        '删除章节',
        {
          confirmButtonText: '确定删除',
          cancelButtonText: '取消',
          type: 'warning'
        }
      ).then(async () => {
        try {
          this.loading = true
          await deleteChapter(this.courseId, chapter.id)
          
          this.chapters.splice(index, 1)
          if (this.currentChapter && this.currentChapter.id === chapter.id) {
            this.currentChapter = null
          }
          if (this.selectedNode && this.selectedNode.chapter && this.selectedNode.chapter.id === chapter.id) {
            this.selectedNode = null
          }
          this.$message.success('章节已删除')
        } catch (error) {
          console.error('删除章节失败:', error)
          this.$message.error('删除章节失败')
        } finally {
          this.loading = false
        }
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
          }).then(async ({ value }) => {
            try {
              this.loading = true
              await updateChapter(this.courseId, chapter.id, {
                title: value
              })
              chapter.title = value
              this.$message.success('重命名成功')
            } catch (error) {
              console.error('重命名章节失败:', error)
              this.$message.error('重命名失败')
            } finally {
              this.loading = false
            }
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

    async addSection(chapter) {
      try {
        this.loading = true
        const response = await createLesson(this.courseId, chapter.id, {
          title: '新小节',
          order: chapter.sections.length
        })
        
        console.log('createLesson response:', response)
        
        const newSection = {
          id: response.lesson_id || response.id,
          title: response.title || '新小节',
          knowledgePoints: [],
          contentBlocks: [],
          _contentLoaded: false
        }
        chapter.sections.push(newSection)
        
        const chapterIndex = this.chapters.indexOf(chapter)
        const sectionIndex = chapter.sections.length - 1
        
        console.log('newSection created with id:', newSection.id)
        
        // 确保 selectedNode有正确id
        this.selectedNode = {
          type: 'section',
          id: newSection.id,
          data: newSection,
          chapter: chapter,
          chapterIndex: chapterIndex,
          sectionIndex: sectionIndex
        }
        
        this.$message.success('已添加新小节')
      } catch (error) {
        console.error('添加小节失败:', error)
        this.$message.error('添加小节失败')
      } finally {
        this.loading = false
      }
    },

    async deleteSection(chapter, sectionIndex) {
      const section = chapter.sections[sectionIndex]
      this.$confirm(
        `确定删除小节"${section.title || '未命名小节'}"吗？该小节下的所有内容块也将被删除。`,
        '删除小节',
        {
          confirmButtonText: '确定删除',
          cancelButtonText: '取消',
          type: 'warning'
        }
      ).then(async () => {
        try {
          this.loading = true
          await deleteLesson(this.courseId, section.id)
          
          chapter.sections.splice(sectionIndex, 1)
          if (this.selectedNode && this.selectedNode.id === section.id) {
            this.selectedNode = null
          }
          this.$message.success('小节已删除')
        } catch (error) {
          console.error('删除小节失败:', error)
          this.$message.error('删除小节失败')
        } finally {
          this.loading = false
        }
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
          }).then(async ({ value }) => {
            try {
              this.loading = true
              await updateLesson(this.courseId, section.id, {
                title: value
              })
              section.title = value
              this.$message.success('重命名成功')
            } catch (error) {
              console.error('重命名小节失败:', error)
              this.$message.error('重命名失败')
            } finally {
              this.loading = false
            }
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
        path: `/teacher/courses/${this.courseId}/preview`,
        query: { preview: 'true' }
      }).catch(err => {
        console.error('路由跳转失败:', err)
      })
    },

    showAddKnowledgeInput() {
      if (!this.selectedNode || this.selectedNode.type !== 'section') {
        this.$message.warning('请先选择一个小节')
        return
      }
      this.currentSection = this.selectedNode.data
      // 初始化已选知识点（使用小节现有的知识点名称数组）
      this.selectedKnowledgePoints = this.currentSection.knowledgePoints ? [...this.currentSection.knowledgePoints] : []
      this.knowledgeDialogVisible = true
      this.loadKnowledgeTree()
    },

    async loadKnowledgeTree() {
      this.knowledgeLoading = true
      try {
        // 调用后端API获取知识点树结构
        const response = await getKnowledgePoints({
          course_id: this.courseId
        })
        
        // 后端返回的结构：{ code: 200, message: '', data: { knowledge_points: [...] } }
        const knowledgePoints = response.data?.knowledge_points || response.knowledge_points || []
        
        // 直接使用后端返回的树结构，添加checked属性
        this.knowledgeTreeData = this.addCheckedProperty(knowledgePoints)
        
        // 同步已选择的知识点状态
        if (this.currentSection && this.currentSection.id) {
          await this.loadSectionKnowledgePoints()
        }
      } catch (error) {
        console.error('加载知识点失败:', error)
        this.$message.error('加载知识点失败')
      } finally {
        this.knowledgeLoading = false
      }
    },

    // 为树节点添加checked和编辑状态属性
    addCheckedProperty(nodes) {
      return nodes.map(node => ({
        ...node,
        checked: false,
        isEditing: false,
        editName: node.name,
        showChildInput: false,
        newChildName: '',
        children: node.children ? this.addCheckedProperty(node.children) : []
      }))
    },

    // 加载小节已关联的知识点
    async loadSectionKnowledgePoints() {
      try {
        const response = await getObjectKnowledgePoints({
          content_type: 'lesson',
          object_id: this.currentSection.id
        })
        
        // 后端返回的结构：{ code: 200, data: { knowledge_points: [...] } }
        const linkedPoints = response.data?.knowledge_points || response.knowledge_points || []
        const linkedPointIds = linkedPoints.map(p => p.id)
        
        // 同步选中状态
        const syncNode = (node) => {
          if (linkedPointIds.includes(node.id)) {
            node.checked = true
          }
          if (node.children) {
            node.children.forEach(syncNode)
          }
        }
        this.knowledgeTreeData.forEach(syncNode)
      } catch (error) {
        console.error('加载小节知识点失败:', error)
      }
    },

    getSelectedKnowledgeCount() {
      let count = 0
      const countNode = (node) => {
        if (node.checked) count++
        if (node.children) {
          node.children.forEach(countNode)
        }
      }
      this.knowledgeTreeData.forEach(countNode)
      return count
    },

    getSelectedKnowledgePoints() {
      const selected = []
      const collectNode = (node) => {
        if (node.checked) {
          selected.push({ id: node.id, name: node.name })
        }
        if (node.children) {
          node.children.forEach(collectNode)
        }
      }
      this.knowledgeTreeData.forEach(collectNode)
      return selected
    },

    handleKnowledgeCheckChange() {
      // 复选框变化时触发
      this.$forceUpdate()
    },

    // 处理节点点击
    handleNodeClick(data) {
      this.selectedKnowledgeNode = data
    },

    // 添加同级知识点（根节点）
    handleAddSameLevelKnowledge() {
      console.log('点击了添加同级知识点')
      this.showRootInput = true
      this.newRootName = ''
      this.$nextTick(() => {
        const input = document.querySelector('.root-add .el-input__inner')
        if (input) {
          input.focus()
          console.log('聚焦到输入框')
        } else {
          console.log('未找到输入框元素')
        }
      })
    },

    // 添加子级知识点
    handleAddChildLevelKnowledge() {
      console.log('点击了添加子级知识点, 当前选中:', this.selectedKnowledgeNode)
      if (!this.selectedKnowledgeNode) {
        this.$message.warning('请先选择一个知识点')
        return
      }
      // 关闭其他输入框
      this.closeAllInputs()
      this.selectedKnowledgeNode.showChildInput = true
      this.selectedKnowledgeNode.newChildName = ''
      this.$forceUpdate()
      this.$nextTick(() => {
        const inputs = document.querySelectorAll('.inline-add-input .el-input__inner')
        console.log('找到的输入框数量:', inputs.length)
        if (inputs.length > 0) inputs[inputs.length - 1].focus()
      })
    },

    // 关闭所有输入框
    closeAllInputs() {
      this.showRootInput = false
      const closeInputsRecursive = (nodes) => {
        nodes.forEach(node => {
          node.showChildInput = false
          node.isEditing = false
          if (node.children) closeInputsRecursive(node.children)
        })
      }
      closeInputsRecursive(this.knowledgeTreeData)
    },

    // 确认添加根节点
    async confirmAddRoot() {
      if (!this.newRootName.trim()) {
        this.$message.warning('请输入知识点名称')
        return
      }
      
      try {
        this.knowledgeLoading = true
        await createKnowledgePoint({
          name: this.newRootName.trim()
        })
        
        this.$message.success('添加成功')
        this.showRootInput = false
        this.newRootName = ''
        await this.loadKnowledgeTree()
      } catch (error) {
        console.error('添加知识点失败:', error)
        this.$message.error('添加失败')
      } finally {
        this.knowledgeLoading = false
      }
    },

    // 取消添加根节点
    cancelAddRoot() {
      this.showRootInput = false
      this.newRootName = ''
    },

    // 确认添加子节点
    async confirmAddChild(parentNode) {
      if (!parentNode.newChildName.trim()) {
        this.$message.warning('请输入知识点名称')
        return
      }
      
      try {
        this.knowledgeLoading = true
        await createKnowledgePoint({
          name: parentNode.newChildName.trim(),
          parent_id: parentNode.id
        })
        
        this.$message.success('添加成功')
        parentNode.showChildInput = false
        parentNode.newChildName = ''
        await this.loadKnowledgeTree()
      } catch (error) {
        console.error('添加子知识点失败:', error)
        this.$message.error('添加失败')
      } finally {
        this.knowledgeLoading = false
      }
    },

    // 取消添加子节点
    cancelAddChild(node) {
      node.showChildInput = false
      node.newChildName = ''
      this.$forceUpdate()
    },

    // 开始编辑知识点
    startEditKnowledgeNode(data) {
      console.log('开始编辑知识点:', data.name)
      this.closeAllInputs()
      data.isEditing = true
      data.editName = data.name
      this.$forceUpdate()
      this.$nextTick(() => {
        const inputs = document.querySelectorAll('.inline-edit-input .el-input__inner')
        console.log('编辑模式找到的输入框数量:', inputs.length)
        if (inputs.length > 0) inputs[inputs.length - 1].focus()
      })
    },

    // 确认编辑知识点
    async confirmEditKnowledge(data) {
      if (!data.editName.trim()) {
        this.$message.warning('请输入知识点名称')
        return
      }
      
      if (data.editName === data.name) {
        data.isEditing = false
        this.$forceUpdate()
        return
      }
      
      try {
        this.knowledgeLoading = true
        await updateKnowledgePoint(data.id, {
          name: data.editName.trim()
        })
        
        data.name = data.editName
        data.isEditing = false
        this.$message.success('编辑成功')
        this.$forceUpdate()
      } catch (error) {
        console.error('编辑知识点失败:', error)
        this.$message.error('编辑失败')
      } finally {
        this.knowledgeLoading = false
      }
    },

    // 取消编辑知识点
    cancelEditKnowledge(data) {
      data.isEditing = false
      data.editName = data.name
      this.$forceUpdate()
    },

    removeSelectedKnowledge(point) {
      // 从选中列表移除
      const uncheckNode = (node) => {
        if (node.id === point.id) {
          node.checked = false
          return true
        }
        if (node.children) {
          return node.children.some(uncheckNode)
        }
        return false
      }
      this.knowledgeTreeData.forEach(uncheckNode)
      this.$forceUpdate()
    },

    findParentId(nodeId) {
      let parentId = null
      const findParent = (nodes, pid = null) => {
        for (const node of nodes) {
          if (node.id === nodeId) {
            parentId = pid
            return true
          }
          if (node.children && findParent(node.children, node.id)) {
            return true
          }
        }
        return false
      }
      findParent(this.knowledgeTreeData)
      return parentId
    },

    deleteKnowledgeNode(data) {
      this.$confirm(`确定删除知识点"${data.name}"吗？`, '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(async () => {
        try {
          this.knowledgeLoading = true
          await deleteKnowledgePoint(data.id)
          this.removeNodeFromTree(this.knowledgeTreeData, data.id)
          this.$message.success('删除成功')
        } catch (error) {
          console.error('删除知识点失败:', error)
          this.$message.error('删除失败')
        } finally {
          this.knowledgeLoading = false
        }
      }).catch(() => {})
    },

    removeNodeFromTree(nodes, nodeId) {
      for (let i = 0; i < nodes.length; i++) {
        if (nodes[i].id === nodeId) {
          nodes.splice(i, 1)
          return true
        }
        if (nodes[i].children && this.removeNodeFromTree(nodes[i].children, nodeId)) {
          return true
        }
      }
      return false
    },

    getAllKnowledgeFlat() {
      const flat = []
      const flatten = (nodes) => {
        nodes.forEach(node => {
          flat.push({ id: node.id, name: node.name })
          if (node.children) {
            flatten(node.children)
          }
        })
      }
      flatten(this.knowledgeTreeData)
      return flat
    },



    // 处理知识点选择器的确认事件
    handleKnowledgeConfirm() {
      // selectedKnowledgePoints 现在是知识点ID数组
      // 允许空数组,这样可以删除所有知识点
      
      // 更新小节的知识点（ID数组）
      this.currentSection.knowledgePoints = [...this.selectedKnowledgePoints]
      
      this.markChanged()
      this.$message.success(`已添加 ${this.selectedKnowledgePoints.length} 个知识点`)
      this.knowledgeDialogVisible = false
    },

    // 处理添加根级知识点
    async handleAddRootKnowledge({ name }) {
      try {
        await createKnowledgePoint({
          name,
          parent_id: null,
          course_id: this.courseId
        })
        this.$message.success('添加成功')
        await this.loadKnowledgeTree()
      } catch (error) {
        console.error('添加知识点失败:', error)
        this.$message.error('添加知识点失败')
      }
    },

    // 处理添加子级知识点
    async handleAddChildKnowledge({ name, parentId }) {
      try {
        await createKnowledgePoint({
          name,
          parent_id: parentId,
          course_id: this.courseId
        })
        this.$message.success('添加成功')
        await this.loadKnowledgeTree()
      } catch (error) {
        console.error('添加知识点失败:', error)
        this.$message.error('添加知识点失败')
      }
    },

    // 处理编辑知识点
    async handleEditKnowledge({ id, name }) {
      try {
        await updateKnowledgePoint(id, { name })
        this.$message.success('修改成功')
        await this.loadKnowledgeTree()
      } catch (error) {
        console.error('修改知识点失败:', error)
        this.$message.error('修改知识点失败')
      }
    },

    // 处理删除知识点
    async handleDeleteKnowledge({ id }) {
      try {
        await deleteKnowledgePoint(id)
        this.$message.success('删除成功')
        await this.loadKnowledgeTree()
      } catch (error) {
        console.error('删除知识点失败:', error)
        this.$message.error('删除知识点失败')
      }
    },

    // 关联知识点到课时
    async attachKnowledgePointsToLesson(lessonId, knowledgePointIds) {
      // 处理空数组的情况:需要删除所有已有的知识点
      if (!knowledgePointIds) {
        knowledgePointIds = []
      }
      
      console.log('[关联知识点] 课时ID:', lessonId, '知识点IDs:', knowledgePointIds)

      // 获取当前课时已有的知识点
      let existingKnowledgePointIds = []
      try {
        const response = await getObjectKnowledgePoints({
          content_type: 'lesson',
          object_id: lessonId
        })
        const responseData = response.data || response
        existingKnowledgePointIds = (responseData.knowledge_points || []).map(kp => kp.id)
        console.log('[关联知识点] 课时已有知识点IDs:', existingKnowledgePointIds)
      } catch (error) {
        console.error('[关联知识点] 获取已有知识点失败:', error)
      }

      // 计算需要添加和移除的知识点(使用ID比较)
      const idsToAdd = knowledgePointIds.filter(id => !existingKnowledgePointIds.includes(id))
      const idsToRemove = existingKnowledgePointIds.filter(id => !knowledgePointIds.includes(id))

      console.log('[关联知识点] 需要添加的IDs:', idsToAdd)
      console.log('[关联知识点] 需要移除的IDs:', idsToRemove)

      // 添加新知识点关联
      for (const pointId of idsToAdd) {
        try {
          await attachKnowledgePoints({
            point_id: pointId,
            content_type: 'lesson',
            object_id: lessonId
          })
          console.log(`[关联知识点] 成功添加知识点ID: ${pointId}`)
        } catch (error) {
          console.error(`[关联知识点] 添加知识点失败 ID ${pointId}:`, error)
          this.$message.error(`知识点关联失败: ${error.response?.data?.message || error.message}`)
        }
      }

      // 移除旧知识点关联
      for (const pointId of idsToRemove) {
        try {
          await detachKnowledgePoints({
            point_id: pointId,
            content_type: 'lesson',
            object_id: lessonId
          })
          console.log(`[关联知识点] 成功移除知识点ID: ${pointId}`)
        } catch (error) {
          console.error(`[关联知识点] 移除知识点失败 ID ${pointId}:`, error)
        }
      }
    },

    // 根据知识点名称查找ID
    getKnowledgePointIdByName(name) {
      const findInTree = (nodes, targetName) => {
        for (const node of nodes) {
          if (node.name === targetName) return node.id
          if (node.children && node.children.length > 0) {
            const found = findInTree(node.children, targetName)
            if (found) return found
          }
        }
        return null
      }
      return findInTree(this.knowledgeTreeData, name)
    },

    // 根据知识点ID查找名称(用于显示)
    getKnowledgePointNameById(id) {
      if (!this.knowledgeTreeData || this.knowledgeTreeData.length === 0) {
        return '' // 树未加载时返回空字符串
      }
      const findInTree = (nodes, targetId) => {
        for (const node of nodes) {
          if (node.id === targetId) return node.name
          if (node.children && node.children.length > 0) {
            const found = findInTree(node.children, targetId)
            if (found) return found
          }
        }
        return null
      }
      return findInTree(this.knowledgeTreeData, id) || ''
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
          fileSize: 0,
          uploading: false,
          uploadProgress: 0,
          order: this.selectedNode.data.contentBlocks.length
        },
        image: {
          id: this.nextBlockId++,
          type: 'image',
          imageUrl: '',
          imageName: '',
          fileSize: 0,
          uploading: false,
          uploadProgress: 0,
          order: this.selectedNode.data.contentBlocks.length
        },
        document: {
          id: this.nextBlockId++,
          type: 'document',
          docUrl: '',
          docName: '',
          displayName: '',
          fileSize: 0,
          uploading: false,
          uploadProgress: 0,
          order: this.selectedNode.data.contentBlocks.length
        },
        text: {
          id: this.nextBlockId++,
          type: 'text',
          textContent: '',
          order: this.selectedNode.data.contentBlocks.length
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
        image: '图片',
        document: '文档',
        text: '文字',
        quiz: '测验'
      }
      return typeMap[type] || '未知'
    },

    getBlockTagType(type) {
      const tagMap = {
        video: 'success',
        image: 'primary',
        document: 'warning',
        text: 'info',
        quiz: 'danger'
      }
      return tagMap[type] || 'info'
    },
    // 文件上传相关
    triggerFileInput(block) {
      const inputRef = this.$refs['fileInput_' + block.id]
      if (inputRef && inputRef[0]) {
        inputRef[0].click()
      }
    },

    async handleFileChange(event, block, fileType) {
      const file = event.target.files[0]
      if (!file) return

      // 判断文件是否为图片
      const isImage = file.type.startsWith('image/')
      
      // 验证文件大小
      const maxSizes = {
        video: 500 * 1024 * 1024, // 500MB
        image: 10 * 1024 * 1024,  // 10MB
        file: 50 * 1024 * 1024    // 50MB
      }

      const actualType = isImage ? 'image' : fileType
      
      if (file.size > maxSizes[actualType]) {
        this.$message.error(`文件大小不能超过 ${maxSizes[actualType] / (1024 * 1024)}MB`)
        event.target.value = '' // 清空input
        return
      }

      // 开始上传
      block.uploading = true
      block.uploadProgress = 0

      try {
        const response = await uploadContentBlockFile(this.courseId, this.selectedNode.data.id, {
          file: file,
          type: actualType
        })

        console.log('上传响应:', response)

        // 处理响应数据 (兼容不同的响应格式)
        let fileData = null
        if (response.data && response.data.data) {
          // 格式: { data: { code: 200, data: {...} } }
          fileData = response.data.data
        } else if (response.data) {
          // 格式: { data: {...} }
          fileData = response.data
        } else if (response.file_url || response.file_path) {
          // 格式: { file_url: ..., file_name: ... }
          fileData = response
        }

        console.log('解析后的文件数据:', fileData)

        // 检查文件URL（支持file_url或file_path）
        const fileUrl = fileData?.file_url || (fileData?.file_path ? `/media/${fileData.file_path}` : null)
        
        if (fileData && fileUrl) {
          // 根据实际文件类型设置对应的属性
          if (actualType === 'video') {
            this.$set(block, 'videoUrl', fileUrl)
            this.$set(block, 'videoName', fileData.file_name)
            this.$set(block, 'fileSize', fileData.file_size)
          } else if (actualType === 'image') {
            this.$set(block, 'imageUrl', fileUrl)
            this.$set(block, 'imageName', fileData.file_name)
            this.$set(block, 'fileSize', fileData.file_size)
          } else {
            this.$set(block, 'docUrl', fileUrl)
            this.$set(block, 'docName', fileData.file_name)
            this.$set(block, 'fileSize', fileData.file_size)
            if (!block.displayName) {
              this.$set(block, 'displayName', fileData.file_name)
            }
          }

          this.markChanged()
          this.$message.success('文件上传成功')
          
          // 强制视图更新
          this.$forceUpdate()
        } else {
          console.error('无效的响应数据:', response, 'fileData:', fileData)
          throw new Error('上传失败: 响应数据格式错误')
        }
      } catch (error) {
        console.error('文件上传失败:', error)
        this.$message.error(error.message || '文件上传失败，请重试')
      } finally {
        block.uploading = false
        block.uploadProgress = 0
        event.target.value = '' // 清空input以便重新选择
      }
    },

    formatFileSize(bytes) {
      if (!bytes) return ''
      if (bytes < 1024) return bytes + ' B'
      if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(2) + ' KB'
      return (bytes / (1024 * 1024)).toFixed(2) + ' MB'
    },

    handleVideoUpload(response, file, block) {
      // 保留此方法以防其他地方调用
      block.videoUrl = response.url || '/mock/video'
      block.videoName = file.name
      this.markChanged()
      this.$message.success('视频上传成功')
    },

    handleDocUpload(response, file, block) {
      // 保留此方法以防其他地方调用
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
        block.fileSize = 0
      } else if (block.type === 'document') {
        block.docUrl = ''
        block.docName = ''
        block.fileSize = 0
      } else if (block.type === 'image') {
        block.imageUrl = ''
        block.imageName = ''
        block.fileSize = 0
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
      this.selectedQuestionBank = null
      this.questionBankSearchText = ''
      this.questionBankDialogVisible = true
      this.loadQuestionBanks()
    },

    async loadQuestionBanks() {
      this.questionBankLoading = true
      try {
        // 模拟加载题库列表
        // TODO: 替换为实际API调用
        await new Promise(resolve => setTimeout(resolve, 300))
        this.questionBankList = [
          { id: 1, name: 'Python基础题库', question_count: 50, description: '包含Python基础语法相关题目' },
          { id: 2, name: 'JavaScript进阶题库', question_count: 30, description: '包含ES6、Promise等进阶内容' },
          { id: 3, name: '数据结构与算法', question_count: 80, description: '常见数据结构和算法题目' },
          { id: 4, name: 'Web开发综合', question_count: 45, description: 'HTML、CSS、JavaScript综合题目' },
          { id: 5, name: '数据库基础', question_count: 35, description: 'SQL语句和数据库设计相关' }
        ]
      } catch (error) {
        console.error('加载题库失败:', error)
        this.$message.error('加载题库失败')
      } finally {
        this.questionBankLoading = false
      }
    },

    selectQuestionBank(bank) {
      this.selectedQuestionBank = bank
    },

    confirmSelectQuestionBank() {
      if (!this.selectedQuestionBank) {
        this.$message.warning('请选择一个题库')
        return
      }

      // 关联题库到测验块
      this.currentQuizBlock.linkedHomeworkId = this.selectedQuestionBank.id
      this.currentQuizBlock.quizTitle = this.selectedQuestionBank.name
      this.currentQuizBlock.quizCreated = true
      
      this.markChanged()
      this.$message.success(`已关联题库: ${this.selectedQuestionBank.name}`)
      this.questionBankDialogVisible = false
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
      // 如果没有选中小节,说明只是新建了章节,不需要保存
      // if (!this.selectedNode || this.selectedNode.type !== 'section') {
      //   this.$message.info('没有需要保存的内容')
      //   return
      // }
      
      console.log('saveAll - courseId:', this.courseId)
      console.log('saveAll - selectedNode.data:', this.selectedNode.data)
      console.log('saveAll - selectedNode.data.id:', this.selectedNode.data.id)
      
      if (!this.courseId || !this.selectedNode.data.id) {
        this.$message.error(`课程ID或小节ID不存在 (courseId: ${this.courseId}, lessonId: ${this.selectedNode.data.id})`)
        return
      }
      
      this.saving = true
      try {
        // 映射前端内容块到后端格式
        const contentBlocks = this.selectedNode.data.contentBlocks.map((block, index) => {
          console.log('处理内容块:', block.type, block)
          
          const mappedBlock = {
            type: this.mapBlockTypeToBackend(block.type),
            title: block.videoName || block.imageName || block.docName || block.displayName || '内容块',
            order: index,
            content: null,
            file: null
          }
          
          // 根据类型映射数据
          switch (block.type) {
            case 'video':
              mappedBlock.file = block.videoUrl
              mappedBlock.content = {
                watch_percent: block.watchPercent || 80
              }
              break
            case 'image':
              mappedBlock.type = 'image'
              mappedBlock.file = block.imageUrl
              mappedBlock.title = block.imageName || '图片'
              console.log('映射图片块:', mappedBlock)
              break
            case 'document':
              mappedBlock.type = 'file'
              mappedBlock.file = block.docUrl
              mappedBlock.title = block.displayName || block.docName
              break
            case 'text':
              mappedBlock.type = 'rich_text'
              mappedBlock.content = {
                html: block.textContent || ''
              }
              break
          }
          
          console.log('映射后的块:', mappedBlock)
          return mappedBlock
        })
        
        console.log('准备保存的所有内容块:', contentBlocks)
        
        // 调用批量保存API
        await saveContentBlocks(this.courseId, this.selectedNode.data.id, {
          content_blocks: contentBlocks
        })
        
        // 关联知识点(无论是否为空,都需要同步,以便删除旧关联)
        const lessonId = this.selectedNode.data.id
        if (lessonId) {
          await this.attachKnowledgePointsToLesson(lessonId, this.selectedNode.data.knowledgePoints || [])
        }
        
        this.$message.success('保存成功')
        this.hasChanges = false
      } catch (error) {
        console.error('保存失败:', error)
        this.$message.error('保存失败，请重试')
        throw error
      } finally {
        this.saving = false
      }
    },

    // 映射后端内容块类型到前端
    mapBlockType(backendType) {
      const typeMap = {
        'video': 'video',
        'image': 'image',
        'document': 'document',
        'file': 'document',
        'rich_text': 'text',
        'audio': 'video', // 暂时映射为video
        'code': 'text'
      }
      return typeMap[backendType] || 'text'
    },

    // 映射前端内容块类型到后端
    mapBlockTypeToBackend(frontendType) {
      const typeMap = {
        'video': 'video',
        'image': 'image',
        'document': 'file',
        'text': 'rich_text',
        'quiz': 'rich_text' // 测验暂时当作富文本处理
      }
      return typeMap[frontendType] || 'rich_text'
    },

    // 更新小节标题
    async updateSectionTitle() {
      if (!this.selectedNode || !this.selectedNode.data || !this.selectedNode.data.id) {
        return
      }
      
      try {
        await updateLesson(this.courseId, this.selectedNode.data.id, {
          title: this.selectedNode.data.title
        })
      } catch (error) {
        console.error('更新小节标题失败:', error)
        this.$message.error('更新小节标题失败')
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
    },

    // 获取完整的媒体URL
    getMediaUrl(url) {
      if (!url) return ''
      if (url.startsWith('http://') || url.startsWith('https://')) {
        return url
      }
      // 拼接后端base URL
      const baseUrl = process.env.VUE_APP_API_BASE_URL || 'http://localhost:8000'
      return `${baseUrl}${url}`
    },

    // 处理媒体加载错误
    handleMediaError(event) {
      console.error('媒体加载失败:', event.target.src)
      this.$message.error('媒体文件加载失败')
    }
  },
  watch: {
    knowledgeSearchText(val) {
      this.$refs.knowledgeTree && this.$refs.knowledgeTree.filter(val)
    }
  }
}
</script>

<style lang="scss" scoped>
.chapter-editor {
  height: 100%;
  display: flex;
  flex-direction: column;
  background: #f5f7fa;
  overflow: hidden; /* 防止全局滚动 */
}

.editor-header {
  background: white;
  padding: 15px 30px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #e4e7ed;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
  flex-shrink: 0; /* 防止header被压缩 */

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
        .custom-upload-area {
          border: 2px dashed #d9d9d9;
          border-radius: 6px;
          background: #fafafa;
          padding: 40px 20px;
          text-align: center;
          cursor: pointer;
          transition: all 0.3s;

          &:hover {
            border-color: #409eff;
            background: #f0f9ff;
          }

          .upload-placeholder {
            i {
              font-size: 48px;
              color: #c0c4cc;
              margin-bottom: 16px;
            }

            .el-upload__text {
              color: #606266;
              font-size: 14px;
              margin-bottom: 8px;

              em {
                color: #409eff;
                font-style: normal;
              }
            }

            .el-upload__tip {
              color: #909399;
              font-size: 12px;
              margin-top: 8px;
            }
          }

          .upload-loading {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 12px;
            color: #409eff;

            i {
              font-size: 32px;
            }

            div {
              font-size: 14px;
            }
          }
        }

        .video-preview-container,
        .image-preview-container {
          background: #f9fafc;
          border-radius: 8px;
          border: 1px solid #e4e7ed;
          overflow: hidden;

          .video-preview {
            width: 100%;
            max-height: 400px;
            background: #000;
            display: block;
          }

          .image-preview {
            width: 100%;
            max-height: 400px;
            object-fit: contain;
            display: block;
            background: #f5f5f5;
          }

          .file-info-bar {
            display: flex;
            align-items: center;
            gap: 15px;
            padding: 12px 15px;
            background: white;
            border-top: 1px solid #e4e7ed;

            .file-name {
              flex: 1;
              display: flex;
              align-items: center;
              gap: 8px;
              color: #303133;
              font-weight: 500;

              i {
                color: #409eff;
                font-size: 18px;
              }
            }

            .file-size {
              color: #909399;
              font-size: 12px;
            }
          }
        }

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
            color: #303133;
            
            &:not(.file-size) {
              flex: 1;
              font-weight: bold;
            }

            &.file-size {
              color: #909399;
              font-size: 12px;
            }
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

/* 知识点选择弹窗样式 */
.knowledge-dialog-content {
  .knowledge-actions {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 12px 0;
    margin-bottom: 16px;
    border-bottom: 1px solid #ebeef5;

    .selected-node-hint {
      color: #909399;
      font-size: 13px;
      margin-left: 10px;
    }
  }

  .knowledge-body {
    display: flex;
    gap: 20px;
    height: 500px;
  }

  .knowledge-left {
    flex: 1;
    display: flex;
    flex-direction: column;
    border: 1px solid #dcdfe6;
    border-radius: 4px;
    padding: 15px;
    background: #fff;

    .knowledge-tree-container {
      flex: 1;
      overflow-y: auto;
      margin-top: 10px;

      .knowledge-tree {
        ::v-deep .el-tree-node__content {
          height: auto;
          min-height: 36px;
          
          &:hover {
            background-color: #f5f7fa;
          }
        }

        .tree-node-wrapper {
          width: 100%;
        }

        .custom-tree-node {
          flex: 1;
          display: flex;
          align-items: center;
          justify-content: space-between;
          padding: 5px 8px 5px 0;
          min-height: 36px;

          .node-label {
            flex: 1;
            font-size: 14px;
          }

          .inline-edit-input {
            flex: 1;
            margin-right: 10px;
          }

          .node-actions {
            display: flex;
            align-items: center;
            gap: 5px;
            opacity: 0;
            transition: opacity 0.3s;

            .el-button {
              padding: 0;
              font-size: 12px;
            }
          }

          &:hover .node-actions {
            opacity: 1;
          }
        }

        .inline-add-input {
          padding: 8px 0 8px 24px;
          
          ::v-deep .el-input-group {
            .el-input__inner {
              border-radius: 4px 0 0 4px;
            }
            
            .el-input-group__append {
              padding: 0;
              
              .el-button {
                margin: 0;
                border-radius: 0;
                border-left: none;
                
                &:last-child {
                  border-radius: 0 4px 4px 0;
                }
                
                &:hover {
                  z-index: 1;
                }
              }
            }
          }
        }

        .root-add {
          padding: 8px;
          margin-top: 10px;
          border-top: 1px dashed #dcdfe6;
        }
      }

      .add-knowledge-btn {
        margin-top: 10px;
        padding-top: 10px;
        border-top: 1px solid #ebeef5;
      }
    }
  }

  .knowledge-right {
    width: 280px;
    display: flex;
    flex-direction: column;
    border: 1px solid #dcdfe6;
    border-radius: 4px;
    background: #f9fafb;

    .selected-header {
      padding: 12px 15px;
      background: #fff;
      border-bottom: 1px solid #dcdfe6;
      font-weight: bold;
      color: #606266;
      border-radius: 4px 4px 0 0;
    }

    .selected-list {
      flex: 1;
      padding: 15px;
      overflow-y: auto;

      .empty-tip {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 100%;
        color: #909399;
        font-size: 13px;

        i {
          font-size: 48px;
          margin-bottom: 10px;
          color: #c0c4cc;
        }
      }
    }
  }
}

.custom-tree-node {
  display: flex;
  align-items: center;
  width: 100%;
}

/* 题库选择卡片样式 */
.question-bank-card {
  cursor: pointer;
  transition: all 0.3s;
  border: 2px solid transparent;

  &:hover {
    border-color: #409eff;
    transform: translateY(-2px);
  }

  &.selected {
    border-color: #67c23a;
    background-color: #f0f9ff;
  }
}
</style>
