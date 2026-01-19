<template>
  <div class="homework-create-new">
    <!-- 顶部基础信息区 -->
    <div class="top-info-area">
      <div class="homework-title-row">
        <button class="back-btn" @click="goBack" title="返回">
          <span class="back-icon">←</span>
        </button>
        <el-input 
          v-model="homework.name" 
          class="homework-name-input"
          placeholder="输入作业名称"
        />
        <div class="header-actions">
          <el-button @click="previewHomework">预览</el-button>
          <el-button @click="saveHomework">保存</el-button>
          <el-button type="primary" @click="saveAndPublish">保存并发布</el-button>
        </div>
      </div>

      <div class="settings-row">
        <div class="setting-item">
          <label>评分机制：</label>
          <el-radio-group v-model="homework.gradingType" size="small">
            <el-radio label="auto">百分制（平均分配每道题的分值）</el-radio>
            <el-radio label="custom">自定义（自行设置每道题的分值）</el-radio>
          </el-radio-group>
        </div>
        <div class="setting-item">
          <label>题型设置：</label>
          <el-radio-group v-model="homework.questionTypeMode" size="small">
            <el-radio label="by-type">按题型归类</el-radio>
            <el-radio label="no-type">不按题型归类</el-radio>
          </el-radio-group>
        </div>
      </div>
    </div>

    <!-- 主内容区域：左侧目录 + 右侧题目 -->
    <div class="main-content-area">
      <!-- 左侧题目目录 -->
      <div class="left-catalog">
        <div class="catalog-header">
          <span>题量 {{ questionCount }}，总分 {{ totalScore.toFixed(1) }}</span>
        </div>
        <div class="catalog-list">
          <!-- 按题型归类模式 -->
          <template v-if="homework.questionTypeMode === 'by-type'">
            <div v-for="(group, groupIndex) in groupedQuestions" :key="groupIndex" class="catalog-type-group">
              <div class="catalog-type-header">
                {{ groupIndex + 1 }} {{ group.typeLabel }}
              </div>
              <draggable 
                v-model="group.questions" 
                handle=".catalog-drag-handle"
                @end="onDragEnd"
                group="questions"
              >
                <transition-group>
                  <div 
                    v-for="(question, qIndex) in group.questions" 
                    :key="question.id"
                    :class="['catalog-item', { active: selectedQuestion && selectedQuestion.id === question.id }]"
                    @click="selectQuestion(question)"
                  >
                    <i class="el-icon-rank catalog-drag-handle"></i>
                    <span class="catalog-num">{{ qIndex + 1 }}</span>
                    <i 
                      class="el-icon-delete catalog-delete" 
                      @click.stop="deleteQuestionFromCatalog(question)"
                      title="删除"
                    ></i>
                  </div>
                </transition-group>
              </draggable>
            </div>
          </template>
          
          <!-- 不按题型归类模式 -->
          <draggable 
            v-else
            v-model="homework.questions" 
            handle=".catalog-drag-handle"
            @end="onDragEnd"
          >
            <transition-group>
              <div 
                v-for="(question, index) in homework.questions" 
                :key="question.id"
                :class="['catalog-item', { active: selectedQuestion && selectedQuestion.id === question.id }]"
                @click="selectQuestion(question)"
              >
                <i class="el-icon-rank catalog-drag-handle"></i>
                <span class="catalog-num">{{ index + 1 }}</span>
                <span class="catalog-type">{{ getQuestionTypeLabel(question.type) }}</span>
                <i 
                  class="el-icon-delete catalog-delete" 
                  @click.stop="deleteQuestionFromCatalog(question)"
                  title="删除"
                ></i>
              </div>
            </transition-group>
          </draggable>
        </div>
      </div>

      <!-- 右侧题目内容区 -->
      <div class="right-questions">
        <!-- 题型工具栏 -->
        <div class="question-type-toolbar">
          <el-button 
            v-for="qType in questionTypes" 
            :key="qType.value"
            @click="addQuestionDirect(qType.value)"
            size="small"
            icon="el-icon-plus"
          >
            {{ qType.label }}
          </el-button>
          <div class="toolbar-extras">
            <el-button size="small" icon="el-icon-star-on">智能导入</el-button>
            <el-button size="small" icon="el-icon-document">选题</el-button>
            <el-dropdown trigger="click">
              <el-button size="small">
                更多<i class="el-icon-arrow-down el-icon--right"></i>
              </el-button>
              <el-dropdown-menu slot="dropdown">
                <el-dropdown-item>从题库选题</el-dropdown-item>
                <el-dropdown-item>批量导入</el-dropdown-item>
              </el-dropdown-menu>
            </el-dropdown>
          </div>
        </div>

        <!-- 题目块列表 -->
        <div class="questions-container">
          <!-- 只显示选中的题目 -->
          <div v-if="selectedQuestion" class="question-block">
            <div class="question-block-header">
              <div class="question-block-title">
                <span class="question-num">{{ getQuestionDisplayNumber(selectedQuestion) }}</span>
                <el-tag size="small" type="info">{{ getQuestionTypeLabel(selectedQuestion.type) }}</el-tag>
                <span v-if="homework.gradingType === 'custom'" class="question-score">
                  {{ selectedQuestion.points || 0 }}分
                </span>
              </div>
              <div class="question-block-actions">
                <el-button 
                  type="text" 
                  size="small" 
                  icon="el-icon-edit"
                  @click="editQuestion(selectedQuestion)"
                >
                  编辑
                </el-button>
                <el-button 
                  type="text" 
                  size="small" 
                  icon="el-icon-delete"
                  style="color: #f56c6c;"
                  @click="deleteQuestionFromCatalog(selectedQuestion)"
                >
                  删除
                </el-button>
              </div>
            </div>

            <div class="question-block-content">
              <!-- 题干 -->
              <div class="question-stem">
                <span v-if="selectedQuestion.title" v-html="selectedQuestion.title"></span>
                <span v-else class="placeholder-text">点击编辑添加题目内容...</span>
              </div>

              <!-- 选项（单选/多选） -->
              <div v-if="['single', 'multiple'].includes(selectedQuestion.type)" class="question-options">
                <div v-for="(opt, optIdx) in selectedQuestion.options" :key="optIdx" class="option-item">
                  <span class="option-label">{{ String.fromCharCode(65 + optIdx) }}.</span>
                  <span>{{ opt }}</span>
                </div>
                <div v-if="!selectedQuestion.options || selectedQuestion.options.length === 0" class="placeholder-text">
                  暂无选项
                </div>
              </div>

              <!-- 答案提示 -->
              <div v-if="selectedQuestion.answer !== null && selectedQuestion.answer !== undefined && selectedQuestion.answer !== ''" class="question-answer-hint">
                <i class="el-icon-check"></i>
                <span v-if="selectedQuestion.type === 'single'">答案：{{ String.fromCharCode(65 + selectedQuestion.answer) }}</span>
                <span v-else-if="selectedQuestion.type === 'multiple'">答案：{{ selectedQuestion.answer.map(a => String.fromCharCode(65 + a)).join(', ') }}</span>
                <span v-else-if="selectedQuestion.type === 'judge'">答案：{{ selectedQuestion.answer ? '正确' : '错误' }}</span>
                <span v-else>已设置参考答案</span>
              </div>

              <!-- 难度和知识点 -->
              <div v-if="selectedQuestion.difficulty || selectedQuestion.knowledgePoints" class="question-meta">
                <el-tag v-if="selectedQuestion.difficulty" size="mini" type="warning">
                  难度：{{ selectedQuestion.difficulty }}
                </el-tag>
                <el-tag v-if="selectedQuestion.knowledgePoints" size="mini">
                  知识点：{{ selectedQuestion.knowledgePoints }}
                </el-tag>
              </div>
            </div>
          </div>

          <!-- 空状态 -->
          <div v-if="!selectedQuestion" class="empty-state">
            <i class="el-icon-document-add"></i>
            <p v-if="homework.questions.length === 0">还没有题目，点击上方按钮添加题目</p>
            <p v-else>点击左侧目录选择题目进行查看或编辑</p>
          </div>
        </div>
      </div>
    </div>

    <!-- 预览对话框 -->
    <el-dialog
      title="作业预览"
      :visible.sync="showPreviewDialog"
      width="900px"
      top="5vh"
      custom-class="preview-dialog"
    >
      <div class="preview-container">
        <div class="preview-header">
          <h2>{{ homework.name }}</h2>
          <div class="preview-info">
            <el-tag>总题量：{{ questionCount }}</el-tag>
            <el-tag type="success">总分：{{ totalScore.toFixed(1) }}分</el-tag>
            <el-tag type="info">评分机制：{{ homework.gradingType === 'auto' ? '自动百分制' : '自定义分值' }}</el-tag>
          </div>
        </div>
        
        <div class="preview-content">
          <!-- 按题型归类显示 -->
          <template v-if="homework.questionTypeMode === 'by-type'">
            <div v-for="(group, groupIndex) in groupedQuestions" :key="groupIndex" class="preview-type-section">
              <h3 class="preview-type-title">{{ groupIndex + 1 }}、{{ group.typeLabel }}（共{{ group.questions.length }}题）</h3>
              <div 
                v-for="(question, qIndex) in group.questions" 
                :key="question.id"
                class="preview-question"
              >
                <div class="preview-question-title">
                  <span class="preview-q-num">{{ qIndex + 1 }}.</span>
                  <span v-html="question.title || '（题目内容未设置）'"></span>
                  <span v-if="homework.gradingType === 'custom'" class="preview-score">({{ question.points || 0 }}分)</span>
                </div>
                
                <!-- 选项 -->
                <div v-if="['single', 'multiple'].includes(question.type)" class="preview-options">
                  <div v-for="(opt, optIdx) in question.options" :key="optIdx" class="preview-option">
                    {{ String.fromCharCode(65 + optIdx) }}. {{ opt || '（选项未设置）' }}
                  </div>
                </div>
                
                <!-- 填空题/简答题答题区 -->
                <div v-if="['fill', 'essay'].includes(question.type)" class="preview-answer-area">
                  <el-input 
                    :type="question.type === 'essay' ? 'textarea' : 'text'"
                    :rows="question.type === 'essay' ? 4 : 1"
                    placeholder="学生作答区域"
                    disabled
                  ></el-input>
                </div>
              </div>
            </div>
          </template>
          
          <!-- 不按题型归类 -->
          <template v-else>
            <div 
              v-for="(question, index) in homework.questions" 
              :key="question.id"
              class="preview-question"
            >
              <div class="preview-question-title">
                <span class="preview-q-num">{{ index + 1 }}.</span>
                <el-tag size="mini" type="info">{{ getQuestionTypeLabel(question.type) }}</el-tag>
                <span v-html="question.title || '（题目内容未设置）'"></span>
                <span v-if="homework.gradingType === 'custom'" class="preview-score">({{ question.points || 0 }}分)</span>
              </div>
              
              <!-- 选项 -->
              <div v-if="['single', 'multiple'].includes(question.type)" class="preview-options">
                <div v-for="(opt, optIdx) in question.options" :key="optIdx" class="preview-option">
                  {{ String.fromCharCode(65 + optIdx) }}. {{ opt || '（选项未设置）' }}
                </div>
              </div>
              
              <!-- 填空题/简答题答题区 -->
              <div v-if="['fill', 'essay'].includes(question.type)" class="preview-answer-area">
                <el-input 
                  :type="question.type === 'essay' ? 'textarea' : 'text'"
                  :rows="question.type === 'essay' ? 4 : 1"
                  placeholder="学生作答区域"
                  disabled
                ></el-input>
              </div>
            </div>
          </template>
          
          <div v-if="homework.questions.length === 0" class="preview-empty">
            <i class="el-icon-warning"></i>
            <p>暂无题目</p>
          </div>
        </div>
      </div>
      
      <span slot="footer">
        <el-button @click="showPreviewDialog = false">关闭</el-button>
        <el-button type="primary" @click="showPreviewDialog = false">确定</el-button>
      </span>
    </el-dialog>

    <!-- 题目编辑对话框 -->
    <el-dialog
      :title="(editingIndex !== null ? '编辑' : '添加') + getQuestionTypeLabel(currentQuestion.type)"
      :visible.sync="showQuestionDialog"
      width="700px"
      :close-on-click-modal="false"
    >
      <el-form :model="currentQuestion" label-width="80px">
        <el-form-item label="题目">
          <el-input 
            v-model="currentQuestion.title" 
            type="textarea" 
            rows="3"
            placeholder="请输入题目内容"
          ></el-input>
        </el-form-item>

        <!-- 单选题/多选题选项 -->
        <template v-if="currentQuestion.type === 'single' || currentQuestion.type === 'multiple'">
          <el-form-item label="选项">
            <div v-for="(option, optIdx) in currentQuestion.options" :key="optIdx" class="option-input-row">
              <span class="option-label">{{ String.fromCharCode(65 + optIdx) }}.</span>
              <el-input v-model="currentQuestion.options[optIdx]" placeholder="请输入选项内容"></el-input>
              <el-button 
                v-if="currentQuestion.options.length > 2"
                type="text" 
                icon="el-icon-delete" 
                @click="removeOption(optIdx)"
                style="color: #f56c6c;"
              ></el-button>
            </div>
            <el-button size="small" @click="addOption" style="margin-top: 10px;">
              <i class="el-icon-plus"></i> 添加选项
            </el-button>
          </el-form-item>

          <el-form-item label="正确答案">
            <el-checkbox-group v-if="currentQuestion.type === 'multiple'" v-model="currentQuestion.answer">
              <el-checkbox 
                v-for="(opt, optIdx) in currentQuestion.options" 
                :key="optIdx" 
                :label="optIdx"
              >
                {{ String.fromCharCode(65 + optIdx) }}
              </el-checkbox>
            </el-checkbox-group>
            <el-radio-group v-else v-model="currentQuestion.answer">
              <el-radio 
                v-for="(opt, optIdx) in currentQuestion.options" 
                :key="optIdx" 
                :label="optIdx"
              >
                {{ String.fromCharCode(65 + optIdx) }}
              </el-radio>
            </el-radio-group>
          </el-form-item>
        </template>

        <!-- 填空题 -->
        <el-form-item v-if="currentQuestion.type === 'fill'" label="参考答案">
          <el-input v-model="currentQuestion.answer" placeholder="请输入参考答案"></el-input>
        </el-form-item>

        <!-- 判断题 -->
        <el-form-item v-if="currentQuestion.type === 'judge'" label="正确答案">
          <el-radio-group v-model="currentQuestion.answer">
            <el-radio :label="true">正确</el-radio>
            <el-radio :label="false">错误</el-radio>
          </el-radio-group>
        </el-form-item>

        <!-- 简答题 -->
        <el-form-item v-if="currentQuestion.type === 'essay'" label="参考答案">
          <el-input 
            v-model="currentQuestion.answer" 
            type="textarea" 
            rows="4"
            placeholder="请输入参考答案（选填）"
          ></el-input>
        </el-form-item>

        <el-form-item v-if="homework.gradingType === 'custom'" label="分值">
          <el-input-number v-model="currentQuestion.points" :min="0" :max="100"></el-input-number>
        </el-form-item>
      </el-form>

      <span slot="footer">
        <el-button @click="showQuestionDialog = false">取消</el-button>
        <el-button type="primary" @click="saveQuestion">确定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import draggable from 'vuedraggable'

export default {
  name: 'HomeworkCreate',
  components: {
    draggable
  },
  data() {
    return {
      homework: {
        id: null,
        name: '新建作业' + new Date().toISOString().slice(0, 19).replace(/[-:T]/g, ''),
        type: 'question', // question | file
        gradingType: 'auto', // auto | custom
        questionTypeMode: 'by-type', // by-type | no-type
        questions: []
      },
      questionTypes: [
        { label: '单选题', value: 'single' },
        { label: '多选题', value: 'multiple' },
        { label: '填空题', value: 'fill' },
        { label: '判断题', value: 'judge' },
        { label: '简答题', value: 'essay' }
      ],
      showQuestionDialog: false,
      showSmartImport: false,
      showBatchSelect: false,
      showPreviewDialog: false,
      currentQuestion: {},
      editingIndex: null,
      selectedQuestion: null
    }
  },
  computed: {
    questionCount() {
      return this.homework.questions.length
    },
    totalScore() {
      if (this.homework.gradingType === 'auto') {
        return 100
      }
      return this.homework.questions.reduce((sum, q) => sum + (q.points || 0), 0)
    },
    // 按题型分组
    groupedQuestions() {
      const groups = []
      const typeMap = {}
      const typeOrder = ['single', 'multiple', 'fill', 'judge', 'essay']
      
      this.homework.questions.forEach(question => {
        if (!typeMap[question.type]) {
          typeMap[question.type] = {
            type: question.type,
            typeLabel: this.getQuestionTypeLabel(question.type),
            questions: []
          }
        }
        typeMap[question.type].questions.push(question)
      })
      
      // 按预定义顺序排列
      typeOrder.forEach(type => {
        if (typeMap[type]) {
          groups.push(typeMap[type])
        }
      })
      
      return groups
    }
  },
  mounted() {
    // 检查是否为编辑模式
    const mode = this.$route.query.mode
    const id = this.$route.query.id
    const from = this.$route.query.from
    
    // 如果从章节编辑器跳转过来，设置作业名称
    if (from === 'chapter-editor') {
      this.homework.name = '课程内嵌测验_' + new Date().toISOString().slice(0, 19).replace(/[-:T]/g, '')
    }
    
    if (mode === 'edit' && id) {
      // 从 sessionStorage 加载作业数据
      const editData = sessionStorage.getItem('editHomeworkData')
      if (editData) {
        try {
          const homeworkData = JSON.parse(editData)
          // 加载作业基本信息
          this.homework.id = homeworkData.id || null
          this.homework.name = homeworkData.name || this.homework.name
          this.homework.type = homeworkData.type || 'question'
          this.homework.gradingType = homeworkData.gradingType || 'auto'
          this.homework.questionTypeMode = homeworkData.questionTypeMode || 'by-type'
          
          // 加载题目列表
          if (homeworkData.questions && Array.isArray(homeworkData.questions)) {
            this.homework.questions = homeworkData.questions.map(q => ({
              ...q,
              id: q.id || Date.now() + Math.random()
            }))
          }
          
          console.log('加载作业数据成功，题目数：', this.homework.questions.length)
          this.$message.success('加载作业成功')
          
          // 清理 sessionStorage
          sessionStorage.removeItem('editHomeworkData')
        } catch (error) {
          console.error('加载作业数据失败:', error)
          this.$message.error('加载作业数据失败')
        }
      }
    }
  },
  methods: {
    // 返回上一页
    goBack() {
      if (this.homework.questions.length > 0 || this.homework.name.trim()) {
        this.$confirm('有未保存的内容，确定要离开吗？', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          this.$router.back()
        }).catch(() => {})
      } else {
        this.$router.back()
      }
    },
    // 直接添加题目（不立即编辑）
    addQuestionDirect(type) {
      const newQuestion = this.createEmptyQuestion(type)
      this.homework.questions.push(newQuestion)
      // 自动选中新添加的题目
      this.selectedQuestion = newQuestion
    },
    
    // 选择左侧目录中的题目
    selectQuestion(question) {
      this.selectedQuestion = question
    },
    
    handleTypeChange(type) {
      if (this.homework.questions.length > 0) {
        this.$confirm('切换作业类型将清空当前题目，是否继续？', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          this.homework.questions = []
        }).catch(() => {
          this.homework.type = type === 'question' ? 'file' : 'question'
        })
      }
    },
    addQuestion(type) {
      this.currentQuestion = this.createEmptyQuestion(type)
      this.editingIndex = null
      this.showQuestionDialog = true
    },
    createEmptyQuestion(type) {
      const baseQuestion = {
        id: Date.now(),
        type: type,
        title: '',
        points: this.homework.gradingType === 'auto' ? 0 : 10
      }

      if (type === 'single' || type === 'multiple') {
        return {
          ...baseQuestion,
          options: ['', '', '', ''],
          answer: type === 'single' ? null : []
        }
      } else if (type === 'fill' || type === 'essay') {
        return {
          ...baseQuestion,
          answer: ''
        }
      } else if (type === 'judge') {
        return {
          ...baseQuestion,
          answer: true
        }
      }
      return baseQuestion
    },
    editQuestion(question) {
      this.currentQuestion = JSON.parse(JSON.stringify(question))
      this.editingIndex = this.homework.questions.findIndex(q => q.id === question.id)
      this.showQuestionDialog = true
    },
    saveQuestion() {
      if (!this.currentQuestion.title) {
        this.$message.error('请输入题目内容')
        return
      }

      if (this.editingIndex !== null) {
        this.$set(this.homework.questions, this.editingIndex, { ...this.currentQuestion })
        // 更新选中的题目
        if (this.selectedQuestion && this.selectedQuestion.id === this.currentQuestion.id) {
          this.selectedQuestion = this.homework.questions[this.editingIndex]
        }
      } else {
        this.homework.questions.push({ ...this.currentQuestion })
        this.selectedQuestion = this.homework.questions[this.homework.questions.length - 1]
      }

      this.showQuestionDialog = false
      this.updateTotalScore()
    },
    copyQuestion(question) {
      const newQuestion = JSON.parse(JSON.stringify(question))
      newQuestion.id = Date.now()
      this.homework.questions.push(newQuestion)
    },
    deleteQuestion(index) {
      this.$confirm('确定删除此题目？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.homework.questions.splice(index, 1)
        this.updateTotalScore()
      }).catch(() => {})
    },
    // 从目录删除题目
    deleteQuestionFromCatalog(question) {
      this.$confirm('确定删除此题目？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        const index = this.homework.questions.findIndex(q => q.id === question.id)
        if (index !== -1) {
          this.homework.questions.splice(index, 1)
          // 如果删除的是当前选中的题目，清空选中
          if (this.selectedQuestion && this.selectedQuestion.id === question.id) {
            this.selectedQuestion = this.homework.questions.length > 0 ? this.homework.questions[0] : null
          }
          this.updateTotalScore()
        }
      }).catch(() => {})
    },
    // 获取题目显示序号
    getQuestionDisplayNumber(question) {
      if (this.homework.questionTypeMode === 'by-type') {
        // 按题型归类时，显示在该题型中的序号
        const sameTypeQuestions = this.homework.questions.filter(q => q.type === question.type)
        return sameTypeQuestions.findIndex(q => q.id === question.id) + 1
      } else {
        // 不归类时，显示总序号
        return this.homework.questions.findIndex(q => q.id === question.id) + 1
      }
    },
    addOption() {
      this.currentQuestion.options.push('')
    },
    removeOption(index) {
      this.currentQuestion.options.splice(index, 1)
    },
    onDragEnd() {
      this.$message.success('题目顺序已调整')
    },
    updateTotalScore() {
      if (this.homework.gradingType === 'auto' && this.homework.questions.length > 0) {
        const pointsPerQuestion = 100 / this.homework.questions.length
        this.homework.questions.forEach(q => {
          q.points = pointsPerQuestion
        })
      }
    },
    getQuestionTypeLabel(type) {
      const labels = {
        single: '单选题',
        multiple: '多选题',
        fill: '填空题',
        judge: '判断题',
        essay: '简答题'
      }
      return labels[type] || type
    },
    previewHomework() {
      if (this.homework.questions.length === 0) {
        this.$message.warning('还没有题目，无法预览')
        return
      }
      this.showPreviewDialog = true
    },
    saveHomework() {
      if (this.homework.questions.length === 0) {
        this.$message.error('请至少添加一道题目')
        return
      }
      
      // 生成作业ID（如果是新建）
      if (!this.homework.id) {
        this.homework.id = 'hw_' + Date.now()
      }
      
      // TODO: 调用API保存
      this.$message.success('作业已保存')
      
      // 如果是从章节编辑器跳转过来的，返回章节编辑器
      if (this.$route.query.from === 'chapter-editor') {
        const blockId = this.$route.query.blockId
        this.$router.push({
          path: `/teacher/course/${this.$route.query.courseId || 1}/chapters/edit`,
          query: {
            from: 'homework-create',
            homeworkId: this.homework.id,
            blockId: blockId
          }
        })
      }
    },
    saveAndPublish() {
      if (this.homework.questions.length === 0) {
        this.$message.error('请至少添加一道题目')
        return
      }
      
      // 生成作业ID（如果是新建）
      if (!this.homework.id) {
        this.homework.id = 'hw_' + Date.now()
      }
      
      // TODO: 调用API保存并发布
      this.$message.success('作业已保存')
      
      // 如果是从章节编辑器跳转过来的
      if (this.$route.query.from === 'chapter-editor') {
        const blockId = this.$route.query.blockId
        const courseId = this.$route.query.courseId || 1
        
        // 跳转到发布页面，并携带返回信息
        this.$router.push({
          path: `/teacher/homework/${this.homework.id}/publish`,
          query: { 
            from: 'chapter-editor',
            courseId: courseId,
            blockId: blockId
          }
        })
      } else {
        // 正常流程：跳转到发布页面
        this.$router.push({
          path: `/teacher/homework/${this.homework.id}/publish`
        })
      }
    }
  }
}
</script>

<style scoped lang="scss">
.homework-create-new {
  min-height: 100vh;
  background: #f5f7fa;
  display: flex;
  flex-direction: column;
}

/* 顶部基础信息区 */
.top-info-area {
  background: white;
  padding: 20px 24px;
  border-bottom: 1px solid #e5e7eb;
}

.homework-title-row {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 16px;

  .back-btn {
    background: white;
    border: 1px solid #e5e7eb;
    width: 40px;
    height: 40px;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: all 0.2s;
    flex-shrink: 0;

    &:hover {
      border-color: #409eff;
      background: #ecf5ff;
    }

    .back-icon {
      font-size: 1.5rem;
      font-weight: 700;
      color: #606266;
    }
  }

  .homework-name-input {
    flex: 1;
    font-size: 18px;
    font-weight: 600;

    ::v-deep .el-input__inner {
      border: 1px dashed transparent;
      font-size: 18px;
      font-weight: 600;
      padding: 8px 12px;
      
      &:hover {
        border-color: #c0c4cc;
      }
      
      &:focus {
        border-color: #409eff;
        border-style: solid;
      }
    }
  }

  .header-actions {
    display: flex;
    gap: 10px;
  }
}

.settings-row {
  display: flex;
  gap: 40px;
  flex-wrap: wrap;

  .setting-item {
    display: flex;
    align-items: center;
    gap: 12px;

    label {
      font-weight: 500;
      color: #606266;
      white-space: nowrap;
    }
  }
}

/* 主内容区域 */
.main-content-area {
  flex: 1;
  display: flex;
  gap: 0;
  overflow: hidden;
}

/* 左侧题目目录 */
.left-catalog {
  width: 280px;
  background: white;
  border-right: 1px solid #e5e7eb;
  display: flex;
  flex-direction: column;
}

.catalog-header {
  padding: 16px;
  border-bottom: 1px solid #e5e7eb;
  background: #fafbfc;
  font-size: 14px;
  font-weight: 500;
  color: #606266;
}

.catalog-list {
  flex: 1;
  overflow-y: auto;
  padding: 8px;
}

.catalog-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 12px;
  margin-bottom: 4px;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s;
  background: white;

  &:hover {
    background: #f5f7fa;
  }

  &.active {
    background: #e6f7ff;
    border-left: 3px solid #1890ff;
  }

  .catalog-drag-handle {
    cursor: move;
    color: #c0c4cc;
    font-size: 14px;

    &:hover {
      color: #909399;
    }
  }

  .catalog-num {
    font-weight: 600;
    color: #303133;
    min-width: 24px;
  }

  .catalog-type {
    color: #909399;
    font-size: 13px;
  }

  .catalog-delete {
    margin-left: auto;
    color: #f56c6c;
    font-size: 14px;
    opacity: 0;
    transition: opacity 0.2s;

    &:hover {
      color: #f78989;
    }
  }

  &:hover .catalog-delete {
    opacity: 1;
  }
}

/* 按题型归类的目录 */
.catalog-type-group {
  margin-bottom: 12px;

  .catalog-type-header {
    padding: 8px 12px;
    font-weight: 600;
    font-size: 14px;
    color: #303133;
    background: #f5f7fa;
    border-radius: 4px;
    margin-bottom: 4px;
  }

  .catalog-item {
    padding-left: 24px;
  }
}

/* 右侧题目内容区 */
.right-questions {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: #f5f7fa;
  overflow: hidden;
}

.question-type-toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 20px;
  background: white;
  border-bottom: 1px solid #e5e7eb;
  gap: 8px;

  .toolbar-extras {
    display: flex;
    gap: 8px;
    margin-left: auto;
  }
}

.questions-container {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
}

.question-block {
  background: white;
  border-radius: 8px;
  margin-bottom: 16px;
  border: 1px solid #e5e7eb;
  transition: all 0.3s;

  &:hover {
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
    border-color: #c0c4cc;
  }
}

.question-block-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  border-bottom: 1px solid #f0f0f0;
  background: #fafbfc;
}

.question-block-title {
  display: flex;
  align-items: center;
  gap: 10px;

  .question-num {
    font-weight: 600;
    font-size: 16px;
    color: #303133;
  }

  .question-score {
    color: #f56c6c;
    font-weight: 500;
    margin-left: 8px;
  }
}

.question-block-actions {
  display: flex;
  gap: 8px;
}

.question-block-content {
  padding: 16px;
}

.question-stem {
  margin-bottom: 12px;
  line-height: 1.6;
  font-size: 14px;
  color: #303133;
  min-height: 24px;
}

.placeholder-text {
  color: #c0c4cc;
  font-style: italic;
}

.question-options {
  margin: 12px 0;
}

.option-item {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  padding: 8px 0;
  font-size: 14px;
  color: #606266;

  .option-label {
    font-weight: 600;
    min-width: 24px;
    color: #909399;
  }
}

.question-answer-hint {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 12px;
  background: #f0f9ff;
  border-left: 3px solid #1890ff;
  border-radius: 4px;
  font-size: 13px;
  color: #1890ff;
  margin-top: 12px;

  i {
    font-size: 14px;
  }
}

.question-meta {
  display: flex;
  gap: 8px;
  margin-top: 12px;
}

.empty-state {
  text-align: center;
  padding: 100px 20px;
  color: #c0c4cc;

  i {
    font-size: 80px;
    display: block;
    margin-bottom: 16px;
    opacity: 0.5;
  }

  p {
    font-size: 14px;
    margin: 0;
  }
}

/* 编辑对话框中的选项输入 */
.option-input-row {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 10px;

  .option-label {
    font-weight: bold;
    color: #666;
    min-width: 30px;
  }

  .el-input {
    flex: 1;
  }
}

/* 预览对话框样式 */
.preview-container {
  max-height: 70vh;
  overflow-y: auto;
}

.preview-header {
  padding-bottom: 20px;
  border-bottom: 2px solid #e5e7eb;
  margin-bottom: 20px;

  h2 {
    margin: 0 0 12px 0;
    font-size: 20px;
    color: #303133;
  }

  .preview-info {
    display: flex;
    gap: 12px;
  }
}

.preview-content {
  padding: 0 4px;
}

.preview-type-section {
  margin-bottom: 30px;

  .preview-type-title {
    font-size: 16px;
    font-weight: 600;
    color: #303133;
    margin: 0 0 16px 0;
    padding-bottom: 8px;
    border-bottom: 1px solid #e5e7eb;
  }
}

.preview-question {
  margin-bottom: 24px;
  padding: 16px;
  background: #fafbfc;
  border-radius: 4px;
  border: 1px solid #e5e7eb;

  .preview-question-title {
    display: flex;
    align-items: flex-start;
    gap: 8px;
    margin-bottom: 12px;
    font-size: 14px;
    line-height: 1.6;
    color: #303133;

    .preview-q-num {
      font-weight: 600;
      min-width: 24px;
    }

    .preview-score {
      color: #f56c6c;
      font-weight: 500;
      margin-left: auto;
    }
  }

  .preview-options {
    margin-left: 32px;

    .preview-option {
      padding: 6px 0;
      color: #606266;
      font-size: 14px;
      line-height: 1.5;
    }
  }

  .preview-answer-area {
    margin-left: 32px;
    margin-top: 8px;
  }
}

.preview-empty {
  text-align: center;
  padding: 60px 20px;
  color: #c0c4cc;

  i {
    font-size: 60px;
    display: block;
    margin-bottom: 12px;
  }

  p {
    font-size: 14px;
    margin: 0;
  }
}
</style>
