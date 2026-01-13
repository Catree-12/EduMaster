<template>
  <div class="homework-create">
    <div class="page-header">
      <h1>{{ homework.name }}</h1>
      <div class="header-actions">
        <el-button @click="previewHomework">预览</el-button>
        <el-button @click="saveHomework">保存</el-button>
        <el-button type="primary" @click="saveAndPublish">保存并发布</el-button>
      </div>
    </div>

    <div class="content-wrapper">
      <!-- 左侧设置面板 -->
      <div class="settings-panel">
        <el-card class="settings-card">
          <div class="settings-section">
            <h3>作业类型</h3>
            <el-radio-group v-model="homework.type" @change="handleTypeChange">
              <el-radio label="question">题目型作业</el-radio>
              <el-radio label="file">答题卡作业</el-radio>
            </el-radio-group>
          </div>

          <div class="settings-section">
            <h3>评分机制</h3>
            <el-radio-group v-model="homework.gradingType">
              <el-radio label="auto">百分制（平均分配每道题的分值）</el-radio>
              <el-radio label="custom">自定义（自行设置每道题的分值）</el-radio>
            </el-radio-group>
          </div>

          <div class="settings-section">
            <h3>题型设置</h3>
            <el-radio-group v-model="homework.questionTypeMode">
              <el-radio label="by-type">按题型归类</el-radio>
              <el-radio label="no-type">不按题型归类</el-radio>
            </el-radio-group>
          </div>
        </el-card>

        <div class="score-summary">
          <span>题量 {{ questionCount }}</span>
          <span>，总分 {{ totalScore.toFixed(1) }}</span>
        </div>
      </div>

      <!-- 右侧题目编辑区 -->
      <div class="questions-panel">
        <div class="question-toolbar">
          <el-button 
            v-for="qType in questionTypes" 
            :key="qType.value"
            @click="addQuestion(qType.value)"
            size="small"
          >
            {{ qType.label }}
          </el-button>
          <div class="toolbar-right">
            <el-button size="small" @click="showSmartImport = true">
              <i class="el-icon-star-on"></i> 智能导入
            </el-button>
            <el-button size="small" @click="showBatchSelect = true">选题</el-button>
            <el-button size="small" class="more-btn">
              更多
              <i class="el-icon-arrow-down"></i>
            </el-button>
          </div>
        </div>

        <!-- 题目列表 -->
        <div class="questions-list">
          <draggable 
            v-model="homework.questions" 
            handle=".drag-handle"
            @end="onDragEnd"
          >
            <transition-group>
              <div 
                v-for="(question, index) in homework.questions" 
                :key="question.id"
                class="question-item"
              >
                <div class="question-drag-handle drag-handle">
                  <i class="el-icon-rank"></i>
                </div>

                <div class="question-content">
                  <div class="question-header">
                    <span class="question-index">{{ index + 1 }}</span>
                    <el-tag size="small" type="info">{{ getQuestionTypeLabel(question.type) }}</el-tag>
                    <div class="question-actions">
                      <el-button type="text" size="small" @click="editQuestion(question, index)">
                        <i class="el-icon-edit"></i>
                      </el-button>
                      <el-button type="text" size="small" @click="copyQuestion(question)">
                        <i class="el-icon-document-copy"></i>
                      </el-button>
                      <el-button type="text" size="small" @click="deleteQuestion(index)" style="color: #f56c6c;">
                        <i class="el-icon-delete"></i>
                      </el-button>
                    </div>
                  </div>

                  <div class="question-preview" @click="editQuestion(question, index)">
                    <div class="question-title">{{ question.title || '点击编辑题目...' }}</div>
                    <div v-if="question.type === 'single' || question.type === 'multiple'" class="question-options">
                      <div v-for="(opt, optIdx) in question.options" :key="optIdx" class="option-preview">
                        {{ String.fromCharCode(65 + optIdx) }}. {{ opt || '选项' + (optIdx + 1) }}
                      </div>
                    </div>
                  </div>

                  <div class="question-footer">
                    <span v-if="homework.gradingType === 'custom'" class="question-points">
                      <el-input-number 
                        v-model="question.points" 
                        :min="0" 
                        :max="100" 
                        size="mini"
                        @change="updateTotalScore"
                      ></el-input-number> 分
                    </span>
                  </div>
                </div>
              </div>
            </transition-group>
          </draggable>

          <div v-if="homework.questions.length === 0" class="empty-questions">
            <i class="el-icon-document-add"></i>
            <p>点击上方按钮添加题目</p>
          </div>
        </div>
      </div>
    </div>

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
      currentQuestion: {},
      editingIndex: null
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
    editQuestion(question, index) {
      this.currentQuestion = JSON.parse(JSON.stringify(question))
      this.editingIndex = index
      this.showQuestionDialog = true
    },
    saveQuestion() {
      if (!this.currentQuestion.title) {
        this.$message.error('请输入题目内容')
        return
      }

      if (this.editingIndex !== null) {
        this.$set(this.homework.questions, this.editingIndex, { ...this.currentQuestion })
      } else {
        this.homework.questions.push({ ...this.currentQuestion })
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
      this.$message.info('预览功能开发中')
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
          path: '/teacher/homework/publish',
          query: { 
            id: this.homework.id,
            from: 'chapter-editor',
            courseId: courseId,
            blockId: blockId
          }
        })
      } else {
        // 正常流程：跳转到发布页面
        this.$router.push({
          path: '/teacher/homework/publish',
          query: { id: this.homework.id }
        })
      }
    }
  }
}
</script>

<style scoped lang="scss">
.homework-create {
  min-height: 100vh;
  background: #e5e7eb;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 20px;
  background: #1e3a8a;
  color: white;

  h1 {
    margin: 0;
    font-size: 18px;
  }

  .header-actions {
    display: flex;
    gap: 10px;
  }
}

.content-wrapper {
  display: flex;
  gap: 20px;
  padding: 20px;
}

.settings-panel {
  width: 300px;
  flex-shrink: 0;
}

.settings-card {
  margin-bottom: 15px;

  .settings-section {
    margin-bottom: 20px;

    &:last-child {
      margin-bottom: 0;
    }

    h3 {
      margin: 0 0 10px 0;
      font-size: 14px;
      color: #333;
    }

    ::v-deep .el-radio {
      display: block;
      margin: 8px 0;
    }
  }
}

.score-summary {
  padding: 10px 15px;
  background: white;
  border-radius: 4px;
  font-size: 13px;
  color: #666;
  text-align: center;
}

.questions-panel {
  flex: 1;
  background: white;
  border-radius: 4px;
  overflow: hidden;
}

.question-toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px;
  border-bottom: 1px solid #e0e0e0;
  background: #fafafa;

  .toolbar-right {
    display: flex;
    gap: 10px;
  }

  .more-btn {
    i {
      margin-left: 5px;
    }
  }
}

.questions-list {
  padding: 20px;
  min-height: 400px;
}

.question-item {
  display: flex;
  gap: 10px;
  margin-bottom: 15px;
  padding: 15px;
  background: #f9f9f9;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  transition: all 0.3s;

  &:hover {
    border-color: #1890ff;
    box-shadow: 0 2px 8px rgba(24, 144, 255, 0.2);
  }
}

.question-drag-handle {
  display: flex;
  align-items: center;
  cursor: move;
  color: #999;

  &:hover {
    color: #1890ff;
  }
}

.question-content {
  flex: 1;
}

.question-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 10px;

  .question-index {
    font-weight: bold;
    color: #333;
  }

  .question-actions {
    margin-left: auto;
    display: flex;
    gap: 5px;
  }
}

.question-preview {
  cursor: pointer;
  margin-bottom: 10px;

  &:hover {
    .question-title {
      color: #1890ff;
    }
  }
}

.question-title {
  font-size: 14px;
  color: #333;
  margin-bottom: 8px;
  transition: color 0.3s;
}

.question-options {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.option-preview {
  font-size: 13px;
  color: #666;
}

.question-footer {
  display: flex;
  justify-content: flex-end;

  .question-points {
    display: flex;
    align-items: center;
    gap: 5px;
    font-size: 13px;
    color: #f56c6c;
  }
}

.empty-questions {
  text-align: center;
  padding: 80px 20px;
  color: #999;

  i {
    font-size: 64px;
    margin-bottom: 20px;
    display: block;
  }
}

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
</style>
