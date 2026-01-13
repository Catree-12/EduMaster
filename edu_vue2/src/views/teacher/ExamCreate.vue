<template>
  <div class="exam-create">
    <!-- 顶部标题栏 -->
    <div class="top-bar">
      <span class="title">新建考试</span>
      <el-button type="primary" @click="saveExam">完成</el-button>
    </div>

    <!-- 主体内容 -->
    <div class="content-wrapper">
      <!-- 试卷基本信息 -->
      <div class="exam-info-section">
        <h2>{{ exam.name }}</h2>
        
        <div class="info-row">
          <div class="info-item">
            <span class="label">题目序号</span>
            <el-radio-group v-model="exam.numberingType">
              <el-radio label="continuous">连续编号</el-radio>
              <el-radio label="byType">按题型编号</el-radio>
            </el-radio-group>
          </div>

          <div class="info-item">
            <span class="label">题型设置</span>
            <el-radio-group v-model="exam.typeGrouping">
              <el-radio :label="true">按题型归类</el-radio>
              <el-radio :label="false">不按题型归类</el-radio>
            </el-radio-group>
          </div>
        </div>

        <div class="info-row">
          <div class="info-item">
            <span class="label">试卷难度</span>
            <el-select v-model="exam.difficulty" placeholder="请选择">
              <el-option label="易" value="easy"></el-option>
              <el-option label="中" value="medium"></el-option>
              <el-option label="难" value="hard"></el-option>
            </el-select>
          </div>
        </div>

        <div class="new-section-link">
          <i class="el-icon-circle-plus"></i>
          <span @click="addNewSection">新建分卷</span>
        </div>
      </div>

      <!-- 左侧题目列表和右侧编辑区 -->
      <div class="main-content">
        <!-- 左侧题目列表 -->
        <div class="questions-sidebar">
          <div class="sidebar-header">
            <span>题量 {{ totalQuestions }}, 总分 {{ totalScore }}</span>
            <el-button type="text" icon="el-icon-refresh" @click="batchOperate">批量操作</el-button>
          </div>

          <!-- 按题型分组显示 -->
          <div v-if="exam.typeGrouping" class="question-groups">
            <div v-for="group in questionGroups" :key="group.type" class="question-group">
              <div class="group-header">
                <i class="el-icon-edit"></i>
                <span class="group-title">题型说明</span>
              </div>
              <div class="group-name">{{ group.name }}（共{{ group.questions.length }}题，{{ group.totalScore }} 分）</div>
              
              <div class="question-list">
                <div 
                  v-for="(q, index) in group.questions" 
                  :key="q.id" 
                  class="question-item"
                  :class="{ active: selectedQuestion && selectedQuestion.id === q.id }"
                  @click="selectQuestion(q)"
                >
                  <span class="question-number">{{ index + 1 }} ({{ q.score }}分)</span>
                </div>
              </div>
            </div>
          </div>

          <!-- 不分组显示 -->
          <div v-else class="question-list-flat">
            <div 
              v-for="(q, index) in allQuestions" 
              :key="q.id" 
              class="question-item"
              :class="{ active: selectedQuestion && selectedQuestion.id === q.id }"
              @click="selectQuestion(q)"
            >
              <span class="question-number">{{ index + 1 }} ({{ q.score }}分)</span>
              <span class="question-type-tag">{{ getQuestionTypeLabel(q.type) }}</span>
            </div>
          </div>
        </div>

        <!-- 右侧编辑区域 -->
        <div class="edit-area">
          <!-- 题型工具栏 -->
          <div class="toolbar">
            <div class="question-type-tabs">
              <span class="toolbar-label">添加题目</span>
              <el-button 
                v-for="type in questionTypes" 
                :key="type.value"
                size="small"
                @click="showQuestionCountDialog(type.value)"
              >
                {{ type.label }}
              </el-button>
              <el-dropdown trigger="click">
                <el-button size="small">
                  更多 <i class="el-icon-arrow-down"></i>
                </el-button>
                <el-dropdown-menu slot="dropdown">
                  <el-dropdown-item>导入题目</el-dropdown-item>
                  <el-dropdown-item>从题库选择</el-dropdown-item>
                </el-dropdown-menu>
              </el-dropdown>
            </div>
            
            <div class="toolbar-actions">
              <el-button size="small" icon="el-icon-magic-stick">智能导入</el-button>
              <el-button size="small" @click="showBatchSelect = true">选题</el-button>
            </div>
          </div>

          <!-- 题目编辑器 -->
          <div v-if="selectedQuestion" class="question-editor">
            <div class="editor-header">
              <span class="question-label">{{ selectedQuestionIndex }} ({{ getQuestionTypeLabel(selectedQuestion.type) }}，{{ selectedQuestion.score }} 分)</span>
              <div class="editor-actions">
                <el-button type="primary" size="small" @click="saveQuestion">编辑</el-button>
                <el-button 
                  type="danger" 
                  size="small" 
                  icon="el-icon-delete"
                  @click="deleteQuestion(selectedQuestion.id)"
                ></el-button>
              </div>
            </div>

            <div class="editor-content">
              <div class="field-row">
                <label>答案解析：</label>
                <div class="field-value">{{ selectedQuestion.analysis || '-' }}</div>
              </div>

              <div class="field-row">
                <label>难度：</label>
                <div class="field-value">{{ selectedQuestion.difficulty || '-' }}</div>
              </div>

              <div class="field-row">
                <label>知识点：</label>
                <div class="field-value">{{ selectedQuestion.knowledgePoints || '-' }}</div>
              </div>
            </div>
          </div>

          <div v-else class="no-question-selected">
            <p>请在左侧选择或添加题目</p>
          </div>
        </div>
      </div>
    </div>

    <!-- 添加题目数量对话框 -->
    <el-dialog 
      :visible.sync="showCountDialog" 
      title="添加题目" 
      width="400px"
      @close="questionCount = 1"
    >
      <div style="margin-bottom: 20px;">
        <label>题目数量：</label>
        <el-input-number 
          v-model="questionCount" 
          :min="1" 
          :max="50"
          style="width: 200px; margin-left: 10px;"
        ></el-input-number>
      </div>
      <div style="margin-bottom: 20px;">
        <label>每题分值：</label>
        <el-input-number 
          v-model="questionScore" 
          :min="1" 
          :max="100"
          style="width: 200px; margin-left: 10px;"
        ></el-input-number>
      </div>
      <span slot="footer">
        <el-button @click="showCountDialog = false">取消</el-button>
        <el-button type="primary" @click="addQuestions">确定</el-button>
      </span>
    </el-dialog>

    <!-- 编辑题目对话框 -->
    <el-dialog 
      :visible.sync="showEditDialog" 
      title="编辑题目" 
      width="800px"
    >
      <el-form v-if="editingQuestion" :model="editingQuestion" label-width="100px">
        <el-form-item label="题目内容">
          <el-input 
            v-model="editingQuestion.title" 
            type="textarea" 
            :rows="3"
            placeholder="请输入题目内容"
          ></el-input>
        </el-form-item>

        <el-form-item v-if="editingQuestion.type === 'single' || editingQuestion.type === 'multiple'" label="选项">
          <div v-for="(option, index) in editingQuestion.options" :key="index" style="margin-bottom: 10px;">
            <el-input 
              v-model="editingQuestion.options[index]" 
              :placeholder="`选项 ${String.fromCharCode(65 + index)}`"
            >
              <template slot="prepend">{{ String.fromCharCode(65 + index) }}</template>
            </el-input>
          </div>
          <el-button size="small" @click="addOption">添加选项</el-button>
        </el-form-item>

        <el-form-item label="正确答案">
          <el-input 
            v-if="editingQuestion.type === 'fill' || editingQuestion.type === 'essay'" 
            v-model="editingQuestion.answer"
            type="textarea"
            :rows="2"
            placeholder="请输入参考答案"
          ></el-input>
          <el-radio-group 
            v-else-if="editingQuestion.type === 'single'" 
            v-model="editingQuestion.answer"
          >
            <el-radio 
              v-for="(option, index) in editingQuestion.options" 
              :key="index" 
              :label="index"
            >
              {{ String.fromCharCode(65 + index) }}
            </el-radio>
          </el-radio-group>
          <el-checkbox-group 
            v-else-if="editingQuestion.type === 'multiple'" 
            v-model="editingQuestion.answer"
          >
            <el-checkbox 
              v-for="(option, index) in editingQuestion.options" 
              :key="index" 
              :label="index"
            >
              {{ String.fromCharCode(65 + index) }}
            </el-checkbox>
          </el-checkbox-group>
          <el-radio-group 
            v-else-if="editingQuestion.type === 'judge'" 
            v-model="editingQuestion.answer"
          >
            <el-radio :label="true">正确</el-radio>
            <el-radio :label="false">错误</el-radio>
          </el-radio-group>
        </el-form-item>

        <el-form-item label="分值">
          <el-input-number v-model="editingQuestion.score" :min="1" :max="100"></el-input-number>
        </el-form-item>

        <el-form-item label="答案解析">
          <el-input 
            v-model="editingQuestion.analysis" 
            type="textarea" 
            :rows="2"
            placeholder="请输入答案解析"
          ></el-input>
        </el-form-item>

        <el-form-item label="难度">
          <el-select v-model="editingQuestion.difficulty">
            <el-option label="易" value="0.8 (易)"></el-option>
            <el-option label="中" value="0.5 (中)"></el-option>
            <el-option label="难" value="0.2 (难)"></el-option>
          </el-select>
        </el-form-item>

        <el-form-item label="知识点">
          <el-input v-model="editingQuestion.knowledgePoints" placeholder="请输入知识点"></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer">
        <el-button @click="showEditDialog = false">取消</el-button>
        <el-button type="primary" @click="saveEditedQuestion">保存</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
export default {
  name: 'ExamCreate',
  data() {
    return {
      exam: {
        name: '新建试卷' + new Date().getTime(),
        numberingType: 'continuous',
        typeGrouping: true,
        difficulty: 'easy'
      },
      questionTypes: [
        { label: '单选题', value: 'single' },
        { label: '多选题', value: 'multiple' },
        { label: '填空题', value: 'fill' },
        { label: '判断题', value: 'judge' },
        { label: '简答题', value: 'essay' }
      ],
      questions: [],
      selectedQuestion: null,
      showCountDialog: false,
      showEditDialog: false,
      showBatchSelect: false,
      currentAddingType: '',
      questionCount: 1,
      questionScore: 5,
      editingQuestion: null,
      nextQuestionId: 1
    }
  },
  computed: {
    questionGroups() {
      const groups = {
        single: { name: '一 多选题', type: 'single', questions: [], totalScore: 0 },
        fill: { name: '二 填空题', type: 'fill', questions: [], totalScore: 0 },
        multiple: { name: '三 单选题', type: 'multiple', questions: [], totalScore: 0 }
      }
      
      this.questions.forEach(q => {
        if (groups[q.type]) {
          groups[q.type].questions.push(q)
          groups[q.type].totalScore += q.score
        }
      })
      
      return Object.values(groups).filter(g => g.questions.length > 0)
    },
    allQuestions() {
      return this.questions
    },
    totalQuestions() {
      return this.questions.length
    },
    totalScore() {
      return this.questions.reduce((sum, q) => sum + q.score, 0).toFixed(1)
    },
    selectedQuestionIndex() {
      if (!this.selectedQuestion) return ''
      const index = this.questions.findIndex(q => q.id === this.selectedQuestion.id)
      return index + 1
    }
  },
  mounted() {
    // 检查是否为编辑模式
    const mode = this.$route.query.mode
    const id = this.$route.query.id
    
    if (mode === 'edit' && id) {
      // 从 sessionStorage 加载试卷数据
      const editData = sessionStorage.getItem('editExamData')
      if (editData) {
        try {
          const examData = JSON.parse(editData)
          // 加载试卷基本信息
          this.exam.name = examData.name || this.exam.name
          this.exam.numberingType = examData.numberingType || 'continuous'
          this.exam.typeGrouping = examData.typeGrouping !== undefined ? examData.typeGrouping : true
          this.exam.difficulty = examData.difficulty || 'easy'
          
          // 加载题目列表
          if (examData.questions && Array.isArray(examData.questions)) {
            this.questions = examData.questions.map(q => ({
              ...q,
              id: q.id || this.nextQuestionId++,
              score: q.points || q.score || 5
            }))
            
            // 选中第一题
            if (this.questions.length > 0) {
              this.selectedQuestion = this.questions[0]
            }
          }
          
          console.log('加载试卷数据成功，题目数：', this.questions.length)
          this.$message.success('加载试卷成功')
          
          // 清理 sessionStorage
          sessionStorage.removeItem('editExamData')
        } catch (error) {
          console.error('加载试卷数据失败:', error)
          this.$message.error('加载试卷数据失败')
        }
      }
    }
  },
  methods: {
    getQuestionTypeLabel(type) {
      const typeMap = {
        single: '单选题',
        multiple: '多选题',
        fill: '填空题',
        judge: '判断题',
        essay: '简答题'
      }
      return typeMap[type] || type
    },
    showQuestionCountDialog(type) {
      this.currentAddingType = type
      this.showCountDialog = true
    },
    addQuestions() {
      const count = this.questionCount
      for (let i = 0; i < count; i++) {
        const question = {
          id: this.nextQuestionId++,
          type: this.currentAddingType,
          title: '',
          options: this.currentAddingType === 'single' || this.currentAddingType === 'multiple' ? ['', '', '', ''] : null,
          answer: this.currentAddingType === 'multiple' ? [] : (this.currentAddingType === 'judge' ? null : ''),
          score: this.questionScore,
          analysis: '',
          difficulty: '0.8 (易)',
          knowledgePoints: ''
        }
        this.questions.push(question)
      }
      
      this.showCountDialog = false
      this.questionCount = 1
      this.$message.success(`已添加 ${count} 道${this.getQuestionTypeLabel(this.currentAddingType)}`)
    },
    selectQuestion(question) {
      this.selectedQuestion = question
    },
    saveQuestion() {
      if (!this.selectedQuestion) return
      this.editingQuestion = JSON.parse(JSON.stringify(this.selectedQuestion))
      this.showEditDialog = true
    },
    saveEditedQuestion() {
      const index = this.questions.findIndex(q => q.id === this.editingQuestion.id)
      if (index !== -1) {
        this.$set(this.questions, index, this.editingQuestion)
        this.selectedQuestion = this.editingQuestion
      }
      this.showEditDialog = false
      this.$message.success('题目已保存')
    },
    deleteQuestion(id) {
      this.$confirm('确定删除此题目？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.questions = this.questions.filter(q => q.id !== id)
        if (this.selectedQuestion && this.selectedQuestion.id === id) {
          this.selectedQuestion = null
        }
        this.$message.success('题目已删除')
      }).catch(() => {})
    },
    addOption() {
      if (this.editingQuestion.options) {
        this.editingQuestion.options.push('')
      }
    },
    addNewSection() {
      this.$message.info('新建分卷功能开发中')
    },
    batchOperate() {
      this.$message.info('批量操作功能开发中')
    },
    saveExam() {
      if (this.questions.length === 0) {
        this.$message.warning('请至少添加一道题目')
        return
      }
      
      this.$confirm('确定保存试卷？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消'
      }).then(() => {
        this.$message.success('试卷已保存')
        this.$router.back()
      }).catch(() => {})
    }
  }
}
</script>

<style scoped lang="scss">
.exam-create {
  min-height: 100vh;
  background: #f5f7fa;
}

.top-bar {
  background: #4a5568;
  color: white;
  padding: 15px 30px;
  display: flex;
  justify-content: space-between;
  align-items: center;

  .title {
    font-size: 18px;
    font-weight: bold;
  }
}

.content-wrapper {
  padding: 20px;
}

.exam-info-section {
  background: white;
  padding: 30px;
  border-radius: 4px;
  margin-bottom: 20px;

  h2 {
    margin: 0 0 30px 0;
    font-size: 20px;
    color: #333;
  }

  .info-row {
    display: flex;
    gap: 60px;
    margin-bottom: 20px;

    .info-item {
      display: flex;
      align-items: center;
      gap: 15px;

      .label {
        font-size: 14px;
        color: #666;
        min-width: 70px;
      }
    }
  }

  .new-section-link {
    color: #1890ff;
    cursor: pointer;
    font-size: 14px;
    margin-top: 20px;

    i {
      margin-right: 5px;
    }

    &:hover {
      opacity: 0.8;
    }
  }
}

.main-content {
  display: flex;
  gap: 20px;
  height: calc(100vh - 400px);
  min-height: 500px;
}

.questions-sidebar {
  width: 350px;
  background: white;
  border-radius: 4px;
  padding: 20px;
  overflow-y: auto;

  .sidebar-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-bottom: 15px;
    border-bottom: 1px solid #e0e0e0;
    margin-bottom: 20px;

    span {
      font-size: 14px;
      color: #333;
    }
  }

  .question-groups {
    .question-group {
      margin-bottom: 25px;

      .group-header {
        display: flex;
        align-items: center;
        gap: 8px;
        color: #666;
        font-size: 13px;
        margin-bottom: 8px;

        i {
          color: #999;
        }
      }

      .group-name {
        font-size: 14px;
        color: #333;
        font-weight: bold;
        margin-bottom: 10px;
      }
    }
  }

  .question-list {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;

    .question-item {
      padding: 8px 12px;
      background: #f5f5f5;
      border-radius: 4px;
      cursor: pointer;
      font-size: 13px;
      color: #666;
      transition: all 0.3s;

      &:hover {
        background: #e6f7ff;
        color: #1890ff;
      }

      &.active {
        background: #1890ff;
        color: white;
      }
    }
  }

  .question-list-flat {
    display: flex;
    flex-direction: column;
    gap: 8px;

    .question-item {
      padding: 12px;
      background: #f5f5f5;
      border-radius: 4px;
      cursor: pointer;
      display: flex;
      justify-content: space-between;
      align-items: center;
      transition: all 0.3s;

      .question-type-tag {
        font-size: 12px;
        color: #999;
      }

      &:hover {
        background: #e6f7ff;
        color: #1890ff;
      }

      &.active {
        background: #1890ff;
        color: white;

        .question-type-tag {
          color: white;
        }
      }
    }
  }
}

.edit-area {
  flex: 1;
  background: white;
  border-radius: 4px;
  padding: 20px;
  overflow-y: auto;

  .toolbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-bottom: 20px;
    border-bottom: 1px solid #e0e0e0;
    margin-bottom: 20px;

    .question-type-tabs {
      display: flex;
      gap: 10px;
      align-items: center;

      .toolbar-label {
        font-size: 14px;
        color: #666;
        margin-right: 10px;
      }
    }

    .toolbar-actions {
      display: flex;
      gap: 10px;
    }
  }

  .question-editor {
    .editor-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 20px;
      padding-bottom: 15px;
      border-bottom: 1px solid #e0e0e0;

      .question-label {
        font-size: 14px;
        color: #333;
      }

      .editor-actions {
        display: flex;
        gap: 10px;
      }
    }

    .editor-content {
      .field-row {
        margin-bottom: 20px;

        label {
          display: block;
          font-size: 14px;
          color: #333;
          margin-bottom: 8px;
        }

        .field-value {
          font-size: 14px;
          color: #666;
          line-height: 1.6;
        }
      }
    }
  }

  .no-question-selected {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 300px;
    color: #999;
    font-size: 14px;
  }
}
</style>
