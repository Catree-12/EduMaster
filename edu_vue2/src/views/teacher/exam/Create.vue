<template>
  <div class="exam-create-new">
    <!-- 顶部基础信息区 -->
    <div class="top-info-area">
      <div class="exam-title-row">
        <button class="back-btn" @click="goBack" title="返回">
          <span class="back-icon">←</span>
        </button>
        <el-input 
          v-model="exam.name" 
          class="exam-name-input"
          placeholder="输入试卷名称"
        />
        <div class="header-actions">
          <el-button @click="previewExam">预览</el-button>
          <el-button @click="saveExam">保存</el-button>
          <el-button type="primary" @click="saveAndPublish">保存并发布</el-button>
        </div>
      </div>

      <div class="settings-row">
        <div class="setting-item">
          <label>题目序号：</label>
          <el-radio-group v-model="exam.numberingType" size="small">
            <el-radio label="continuous">连续编号</el-radio>
            <el-radio label="by-type">按题型编号</el-radio>
          </el-radio-group>
        </div>
      </div>

      <div class="settings-row">
        <div class="setting-item">
          <label>题型设置：</label>
          <el-radio-group v-model="exam.questionTypeMode" size="small" :disabled="exam.numberingType === 'by-type'">
            <el-radio label="by-type">按题型归类</el-radio>
            <el-radio label="no-type">不按题型归类</el-radio>
          </el-radio-group>
        </div>
      </div>

      <div class="settings-row">
        <div class="setting-item">
          <label>试卷难度：</label>
          <el-select v-model="exam.difficulty" size="small" placeholder="请选择">
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

    <!-- 主内容区域：左侧目录 + 右侧题目 -->
    <div class="main-content-area">
      <!-- 左侧题目目录 -->
      <div class="left-catalog">
        <div class="catalog-header">
          <span>题量 {{ questionCount }}，总分 {{ totalScore.toFixed(1) }}</span>
          <el-button type="text" size="small" @click="showBatchActions = !showBatchActions">
            批量操作
          </el-button>
        </div>
        <div v-if="showBatchActions" class="catalog-actions">
          <el-button size="small" @click="openSetScoreDialog">设置分值</el-button>
          <el-button size="small" @click="batchDeleteQuestions">批量删除</el-button>
        </div>
        <div class="catalog-list">
          <!-- 按题型归类模式 -->
          <template v-if="exam.questionTypeMode === 'by-type'">
            <div v-for="(group, groupIndex) in groupedQuestions" :key="groupIndex" class="catalog-type-group">
              <div class="catalog-type-header">
                <span class="type-title">{{ groupIndex + 1 }} {{ group.typeLabel }}</span>
                <el-input-number 
                  v-if="showBatchActions"
                  v-model="group.totalScore" 
                  :min="0" 
                  :max="1000"
                  size="mini"
                  controls-position="right"
                  @change="updateTypeScore(group)"
                  class="type-score-input"
                ></el-input-number>
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
            v-model="exam.questions" 
            handle=".catalog-drag-handle"
            @end="onDragEnd"
          >
            <transition-group>
              <div 
                v-for="(question, index) in exam.questions" 
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
          <div v-if="selectedQuestion" class="question-block editable">
            <div class="question-block-header">
              <div class="question-block-title">
                <span class="question-num">{{ getQuestionDisplayNumber(selectedQuestion) }}</span>
                <el-tag size="small" type="info">{{ getQuestionTypeLabel(selectedQuestion.type) }}</el-tag>
                <el-input-number 
                  v-if="isEditMode"
                  v-model="selectedQuestion.points" 
                  :min="0" 
                  :max="100"
                  size="mini"
                  controls-position="right"
                  @change="updateTotalScore"
                  style="width: 100px; margin-left: 10px;"
                ></el-input-number>
                <span v-else style="margin-left: 10px; color: #f56c6c; font-weight: 500;">{{ selectedQuestion.points || 0 }}分</span>
              </div>
              <div class="question-block-actions">
                <el-button 
                  v-if="!isEditMode"
                  type="primary"
                  size="small" 
                  icon="el-icon-edit"
                  @click="isEditMode = true"
                >
                  编辑
                </el-button>
                <el-button 
                  v-else
                  type="success"
                  size="small" 
                  icon="el-icon-check"
                  @click="isEditMode = false"
                >
                  完成
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
              <!-- 题干编辑 -->
              <div class="question-stem-edit">
                <label class="edit-label">题目内容</label>
                <el-input 
                  v-if="isEditMode"
                  v-model="selectedQuestion.title" 
                  type="textarea" 
                  rows="3"
                  placeholder="请输入题目内容"
                  @change="updateTotalScore"
                ></el-input>
                <div v-else class="question-stem-view">
                  <span v-if="selectedQuestion.title">{{ selectedQuestion.title }}</span>
                  <span v-else class="placeholder-text">暂无题目内容</span>
                </div>
              </div>

              <!-- 选项编辑（单选/多选） -->
              <div v-if="['single', 'multiple'].includes(selectedQuestion.type)" class="question-options-edit">
                <label class="edit-label">选项设置</label>
                <div v-if="isEditMode">
                  <div v-for="(opt, optIdx) in selectedQuestion.options" :key="optIdx" class="option-input-row">
                    <span 
                      class="option-label clickable"
                      :class="{ selected: isAnswerSelected(optIdx) }"
                      @click="toggleAnswer(optIdx)"
                    >
                      {{ String.fromCharCode(65 + optIdx) }}
                    </span>
                    <el-input v-model="selectedQuestion.options[optIdx]" placeholder="请输入选项内容"></el-input>
                    <el-button 
                      v-if="selectedQuestion.options.length > 2"
                      type="text" 
                      icon="el-icon-delete" 
                      @click="removeOption(optIdx)"
                      style="color: #f56c6c;"
                    ></el-button>
                  </div>
                  <el-button size="small" @click="addOption" style="margin-top: 10px;">
                    <i class="el-icon-plus"></i> 添加选项
                  </el-button>
                </div>
                <div v-else class="options-view">
                  <div v-for="(opt, optIdx) in selectedQuestion.options" :key="optIdx" class="option-view-item">
                    <span 
                      class="option-label"
                      :class="{ selected: isAnswerSelected(optIdx) }"
                    >
                      {{ String.fromCharCode(65 + optIdx) }}
                    </span>
                    <span>{{ opt || '（选项未设置）' }}</span>
                  </div>
                </div>


              </div>

              <!-- 填空题答案 -->
              <div v-if="selectedQuestion.type === 'fill'" class="answer-edit">
                <label class="edit-label">参考答案</label>
                <el-input v-if="isEditMode" v-model="selectedQuestion.answer" placeholder="请输入参考答案"></el-input>
                <div v-else class="answer-view">{{ selectedQuestion.answer || '（未设置）' }}</div>
              </div>

              <!-- 判断题答案 -->
              <div v-if="selectedQuestion.type === 'judge'" class="answer-edit">
                <label class="edit-label">正确答案</label>
                <el-radio-group v-if="isEditMode" v-model="selectedQuestion.answer">
                  <el-radio :label="true">正确</el-radio>
                  <el-radio :label="false">错误</el-radio>
                </el-radio-group>
                <div v-else class="answer-view">
                  <el-tag :type="selectedQuestion.answer ? 'success' : 'danger'">
                    {{ selectedQuestion.answer ? '正确' : '错误' }}
                  </el-tag>
                </div>
              </div>

              <!-- 简答题答案 -->
              <div v-if="selectedQuestion.type === 'essay'" class="answer-edit">
                <label class="edit-label">参考答案</label>
                <el-input 
                  v-if="isEditMode"
                  v-model="selectedQuestion.answer" 
                  type="textarea" 
                  rows="4"
                  placeholder="请输入参考答案（选填）"
                ></el-input>
                <div v-else class="answer-view" style="white-space: pre-wrap;">{{ selectedQuestion.answer || '（未设置）' }}</div>
              </div>

              <!-- 答案解析 -->
              <div class="answer-analysis-edit">
                <label class="edit-label">答案解析</label>
                <el-input 
                  v-if="isEditMode"
                  v-model="selectedQuestion.analysis" 
                  type="textarea" 
                  rows="3"
                  placeholder="请输入答案解析（选填）"
                ></el-input>
                <div v-else class="answer-view" style="white-space: pre-wrap;">{{ selectedQuestion.analysis || '（未设置）' }}</div>
              </div>

              <!-- 难度、知识点、标签 -->
              <div class="question-metadata-edit">
                <el-row :gutter="20">
                  <el-col :span="8">
                    <label class="edit-label">难度（0.1-1.0）</label>
                    <el-input-number
                      v-if="isEditMode"
                      v-model="selectedQuestion.difficulty"
                      :min="0.1"
                      :max="1.0"
                      :step="0.1"
                      :precision="1"
                      placeholder="选择难度"
                      style="width: 100%;"
                    ></el-input-number>
                    <div v-else class="metadata-view">
                      <el-tag v-if="selectedQuestion.difficulty" type="warning" size="small">
                        {{ selectedQuestion.difficulty }}
                      </el-tag>
                      <span v-else class="placeholder-text">未设置</span>
                    </div>
                  </el-col>
                  <el-col :span="8">
                    <label class="edit-label">知识点 <el-button v-if="isEditMode" type="text" size="mini" @click="showKnowledgeDialog = true">创建</el-button></label>
                    <el-select 
                      v-if="isEditMode"
                      v-model="selectedQuestion.knowledgePoints" 
                      multiple 
                      filterable
                      allow-create
                      default-first-option
                      placeholder="选择或创建知识点" 
                      style="width: 100%;"
                    >
                      <el-option 
                        v-for="kp in knowledgeList" 
                        :key="kp.id" 
                        :label="kp.name" 
                        :value="kp.name"
                      ></el-option>
                    </el-select>
                    <div v-else class="metadata-view">
                      <el-tag 
                        v-for="(kp, idx) in selectedQuestion.knowledgePoints" 
                        :key="idx" 
                        size="small" 
                        style="margin-right: 5px;"
                      >
                        {{ kp }}
                      </el-tag>
                      <span v-if="!selectedQuestion.knowledgePoints || selectedQuestion.knowledgePoints.length === 0" class="placeholder-text">未设置</span>
                    </div>
                  </el-col>
                  <el-col :span="8">
                    <label class="edit-label">标签 <el-button v-if="isEditMode" type="text" size="mini" @click="showTagDialog = true">创建</el-button></label>
                    <el-select 
                      v-if="isEditMode"
                      v-model="selectedQuestion.tags" 
                      multiple 
                      filterable
                      allow-create
                      default-first-option
                      placeholder="选择或创建标签" 
                      style="width: 100%;"
                    >
                      <el-option 
                        v-for="tag in tagList" 
                        :key="tag.id" 
                        :label="tag.name" 
                        :value="tag.name"
                      ></el-option>
                    </el-select>
                    <div v-else class="metadata-view">
                      <el-tag 
                        v-for="(tag, idx) in selectedQuestion.tags" 
                        :key="idx" 
                        type="info"
                        size="small" 
                        style="margin-right: 5px;"
                      >
                        {{ tag }}
                      </el-tag>
                      <span v-if="!selectedQuestion.tags || selectedQuestion.tags.length === 0" class="placeholder-text">未设置</span>
                    </div>
                  </el-col>
                </el-row>
              </div>
            </div>
          </div>

          <!-- 空状态 -->
          <div v-if="!selectedQuestion" class="empty-state">
            <i class="el-icon-document-add"></i>
            <p v-if="exam.questions.length === 0">还没有题目，点击上方按钮添加题目</p>
            <p v-else>点击左侧目录选择题目进行查看或编辑</p>
          </div>
        </div>
      </div>
    </div>

    <!-- 预览对话框 -->
    <el-dialog
      title="试卷预览"
      :visible.sync="showPreviewDialog"
      width="900px"
      top="5vh"
      custom-class="preview-dialog"
    >
      <div class="preview-container">
        <div class="preview-header">
          <h2>{{ exam.name }}</h2>
          <div class="preview-info">
            <el-tag>总题量：{{ questionCount }}</el-tag>
            <el-tag type="success">总分：{{ totalScore.toFixed(1) }}分</el-tag>
            <el-tag type="warning">难度：{{ getDifficultyLabel(exam.difficulty) }}</el-tag>
          </div>
        </div>
        
        <div class="preview-content">
          <!-- 按题型归类显示 -->
          <template v-if="exam.questionTypeMode === 'by-type'">
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
                  <span class="preview-score">({{ question.points || 0 }}分)</span>
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
              v-for="(question, index) in exam.questions" 
              :key="question.id"
              class="preview-question"
            >
              <div class="preview-question-title">
                <span class="preview-q-num">{{ index + 1 }}.</span>
                <el-tag size="mini" type="info">{{ getQuestionTypeLabel(question.type) }}</el-tag>
                <span v-html="question.title || '（题目内容未设置）'"></span>
                <span class="preview-score">({{ question.points || 0 }}分)</span>
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
          
          <div v-if="exam.questions.length === 0" class="preview-empty">
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

    <!-- 标签管理对话框 - 简化版 -->
    <el-dialog
      title="快速创建标签"
      :visible.sync="showTagDialog"
      width="500px"
    >
      <el-form label-width="80px">
        <el-form-item label="标签名称">
          <el-input v-model="newTagName" placeholder="输入标签名称" @keyup.enter.native="addTagQuick"></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer">
        <el-button @click="showTagDialog = false">取消</el-button>
        <el-button type="primary" @click="addTagQuick">创建</el-button>
      </span>
    </el-dialog>

    <!-- 知识点管理对话框 - 简化版 -->
    <el-dialog
      title="快速创建知识点"
      :visible.sync="showKnowledgeDialog"
      width="500px"
    >
      <el-form label-width="80px">
        <el-form-item label="知识点">
          <el-input v-model="newKnowledgeName" placeholder="输入知识点名称" @keyup.enter.native="addKnowledgeQuick"></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer">
        <el-button @click="showKnowledgeDialog = false">取消</el-button>
        <el-button type="primary" @click="addKnowledgeQuick">创建</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import draggable from 'vuedraggable'

export default {
  name: 'ExamCreate',
  components: {
    draggable
  },
  data() {
    return {
      exam: {
        id: null,
        name: '新建试卷' + new Date().toISOString().slice(0, 19).replace(/[-:T]/g, ''),
        numberingType: 'continuous', // continuous | by-type
        questionTypeMode: 'by-type', // by-type | no-type
        difficulty: 'easy', // easy | medium | hard
        questions: []
      },
      questionTypes: [
        { label: '单选题', value: 'single' },
        { label: '多选题', value: 'multiple' },
        { label: '填空题', value: 'fill' },
        { label: '判断题', value: 'judge' },
        { label: '简答题', value: 'essay' }
      ],
      showPreviewDialog: false,
      showBatchActions: false,
      selectedQuestion: null,
      isEditMode: false, // 编辑模式控制
      
      // 标签和知识点管理
      showTagDialog: false,
      showKnowledgeDialog: false,
      newTagName: '',
      newKnowledgeName: '',
      tagList: [
        { id: 1, name: '期中考试', color: '#409EFF' },
        { id: 2, name: '期末考试', color: '#67C23A' },
        { id: 3, name: '单元测试', color: '#E6A23C' }
      ],
      knowledgeList: [
        { id: 1, name: '数据结构', category: 'basic' },
        { id: 2, name: '算法分析', category: 'basic' },
        { id: 3, name: '面向对象', category: 'core' }
      ]
    }
  },
  computed: {
    questionCount() {
      return this.exam.questions.length
    },
    totalScore() {
      return this.exam.questions.reduce((sum, q) => sum + (q.points || 0), 0)
    },
    // 按题型分组
    groupedQuestions() {
      const groups = []
      const typeMap = {}
      const typeOrder = ['single', 'multiple', 'fill', 'judge', 'essay']
      
      this.exam.questions.forEach(question => {
        if (!typeMap[question.type]) {
          typeMap[question.type] = {
            type: question.type,
            typeLabel: this.getQuestionTypeLabel(question.type),
            questions: [],
            totalScore: 0
          }
        }
        typeMap[question.type].questions.push(question)
      })
      
      // 按预定义顺序排列
      typeOrder.forEach(type => {
        if (typeMap[type]) {
          // 计算该题型的总分
          typeMap[type].totalScore = typeMap[type].questions.reduce((sum, q) => sum + (q.points || 0), 0)
          groups.push(typeMap[type])
        }
      })
      
      return groups
    }
  },
  watch: {
    'exam.numberingType'(newVal) {
      if (newVal === 'by-type') {
        // 按题型编号时，强制按题型归类
        this.exam.questionTypeMode = 'by-type'
      }
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
          this.exam.id = examData.id || null
          this.exam.name = examData.name || this.exam.name
          this.exam.gradingType = examData.gradingType || 'auto'
          this.exam.questionTypeMode = examData.questionTypeMode || 'by-type'
          
          // 加载题目列表
          if (examData.questions && Array.isArray(examData.questions)) {
            this.exam.questions = examData.questions.map(q => ({
              ...q,
              id: q.id || Date.now() + Math.random()
            }))
          }
          
          console.log('加载试卷数据成功，题目数：', this.exam.questions.length)
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
    // 返回上一页
    goBack() {
      if (this.exam.questions.length > 0 || this.exam.name.trim()) {
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
      this.exam.questions.push(newQuestion)
      // 自动选中新添加的题目
      this.selectedQuestion = newQuestion
    },
    
    // 选择左侧目录中的题目
    selectQuestion(question) {
      this.selectedQuestion = question
    },
    
    createEmptyQuestion(type) {
      const baseQuestion = {
        id: Date.now() + Math.random(),
        type: type,
        title: '',
        points: 5,
        analysis: '', // 答案解析
        difficulty: '', // 难度
        knowledgePoints: [], // 知识点数组
        tags: [] // 标签数组
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
    // 快速添加标签
    addTagQuick() {
      if (!this.newTagName.trim()) {
        this.$message.warning('请输入标签名称')
        return
      }
      const newTag = {
        id: Date.now(),
        name: this.newTagName.trim(),
        color: '#409EFF'
      }
      this.tagList.push(newTag)
      this.$message.success(`标签"${newTag.name}"创建成功`)
      this.newTagName = ''
      this.showTagDialog = false
    },
    // 快速添加知识点
    addKnowledgeQuick() {
      if (!this.newKnowledgeName.trim()) {
        this.$message.warning('请输入知识点名称')
        return
      }
      const newKnowledge = {
        id: Date.now(),
        name: this.newKnowledgeName.trim(),
        category: 'basic'
      }
      this.knowledgeList.push(newKnowledge)
      this.$message.success(`知识点"${newKnowledge.name}"创建成功`)
      this.newKnowledgeName = ''
      this.showKnowledgeDialog = false
    },
    // 判断答案是否被选中
    isAnswerSelected(optIdx) {
      if (!this.selectedQuestion) return false
      if (this.selectedQuestion.type === 'single') {
        return this.selectedQuestion.answer === optIdx
      } else if (this.selectedQuestion.type === 'multiple') {
        return this.selectedQuestion.answer && this.selectedQuestion.answer.includes(optIdx)
      }
      return false
    },
    // 切换答案选择
    toggleAnswer(optIdx) {
      if (!this.isEditMode || !this.selectedQuestion) return
      
      if (this.selectedQuestion.type === 'single') {
        // 单选题：直接设置
        this.selectedQuestion.answer = optIdx
      } else if (this.selectedQuestion.type === 'multiple') {
        // 多选题：切换
        if (!this.selectedQuestion.answer) {
          this.selectedQuestion.answer = []
        }
        const index = this.selectedQuestion.answer.indexOf(optIdx)
        if (index > -1) {
          this.selectedQuestion.answer.splice(index, 1)
        } else {
          this.selectedQuestion.answer.push(optIdx)
        }
      }
    },
    addOption() {
      if (!this.selectedQuestion || !this.selectedQuestion.options) {
        return
      }
      this.selectedQuestion.options.push('')
    },
    removeOption(index) {
      if (!this.selectedQuestion || !this.selectedQuestion.options) {
        return
      }
      this.selectedQuestion.options.splice(index, 1)
    },
    // 从目录删除题目
    deleteQuestionFromCatalog(question) {
      this.$confirm('确定删除此题目？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        const index = this.exam.questions.findIndex(q => q.id === question.id)
        if (index !== -1) {
          this.exam.questions.splice(index, 1)
          // 如果删除的是当前选中的题目，清空选中
          if (this.selectedQuestion && this.selectedQuestion.id === question.id) {
            this.selectedQuestion = this.exam.questions.length > 0 ? this.exam.questions[0] : null
          }
          this.updateTotalScore()
        }
      }).catch(() => {})
    },
    // 获取题目显示序号
    getQuestionDisplayNumber(question) {
      if (this.exam.questionTypeMode === 'by-type') {
        // 按题型归类时，显示在该题型中的序号
        const sameTypeQuestions = this.exam.questions.filter(q => q.type === question.type)
        return sameTypeQuestions.findIndex(q => q.id === question.id) + 1
      } else {
        // 不归类时，显示总序号
        return this.exam.questions.findIndex(q => q.id === question.id) + 1
      }
    },
    onDragEnd() {
      this.$message.success('题目顺序已调整')
    },
    updateTotalScore() {
      // 试卷不需要自动分配分值，由用户手动设置
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
    getDifficultyLabel(difficulty) {
      const labels = {
        easy: '易',
        medium: '中',
        hard: '难'
      }
      return labels[difficulty] || difficulty
    },
    updateTypeScore(group) {
      // 计算该题型应分配的平均分值
      const questionCount = group.questions.length
      if (questionCount === 0) return
      
      const avgScore = group.totalScore / questionCount
      
      // 更新该题型下所有题目的分值
      group.questions.forEach(q => {
        q.points = avgScore
      })
      
      this.$message.success(`已将${group.typeLabel}的总分${group.totalScore}分平均分配给${questionCount}道题`)
    },
    addNewSection() {
      this.$message.info('新建分卷功能开发中')
    },
    openSetScoreDialog() {
      this.$message.info('设置分值功能开发中')
    },
    batchDeleteQuestions() {
      if (this.exam.questions.length === 0) {
        this.$message.warning('暂无题目可删除')
        return
      }
      this.$confirm('确定删除所有选中的题目？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.$message.info('批量删除功能开发中')
      }).catch(() => {})
    },
    previewExam() {
      if (this.exam.questions.length === 0) {
        this.$message.warning('还没有题目，无法预览')
        return
      }
      this.showPreviewDialog = true
    },
    saveExam() {
      if (this.exam.questions.length === 0) {
        this.$message.error('请至少添加一道题目')
        return
      }
      
      // 生成试卷ID（如果是新建）
      if (!this.exam.id) {
        this.exam.id = 'exam_' + Date.now()
      }
      
      // TODO: 调用API保存
      this.$message.success('试卷已保存')
    },
    saveAndPublish() {
      if (this.exam.questions.length === 0) {
        this.$message.error('请至少添加一道题目')
        return
      }
      
      // 生成试卷ID（如果是新建）
      if (!this.exam.id) {
        this.exam.id = 'exam_' + Date.now()
      }
      
      // TODO: 调用API保存并发布
      this.$message.success('试卷已保存')
      
      // 跳转到发布页面
      this.$router.push({
        path: `/teacher/exam/${this.exam.id}/publish`
      })
    }
  }
}
</script>

<style scoped lang="scss">
.exam-create-new {
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

.exam-title-row {
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

  .exam-name-input {
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
  margin-bottom: 12px;

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

.new-section-link {
  color: #1890ff;
  cursor: pointer;
  font-size: 14px;
  margin-top: 8px;
  display: inline-flex;
  align-items: center;

  i {
    margin-right: 5px;
  }

  &:hover {
    opacity: 0.8;
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
  display: flex;
  justify-content: space-between;
  align-items: center;

  .el-button--text {
    color: #409eff;
    padding: 0;
    
    &:hover {
      color: #66b1ff;
    }
  }
}

.catalog-actions {
  padding: 12px 16px;
  border-bottom: 1px solid #e5e7eb;
  display: flex;
  gap: 8px;

  .el-button {
    flex: 1;
  }
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
    display: flex;
    justify-content: space-between;
    align-items: center;

    .type-title {
      flex: 1;
    }

    .type-score-input {
      width: 120px;
      margin-left: 10px;

      ::v-deep .el-input__inner {
        text-align: right;
      }
    }
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

  &.editable {
    border-color: #667eea;
    box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.1);
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
  padding: 20px;

  .edit-label {
    display: block;
    font-size: 14px;
    font-weight: 600;
    color: #606266;
    margin-bottom: 10px;
  }

  .question-stem-edit,
  .question-options-edit,
  .answer-edit,
  .answer-analysis-edit,
  .question-metadata-edit {
    margin-bottom: 20px;
  }

  .option-input-row {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 10px;

    .option-label {
      font-weight: 600;
      min-width: 32px;
      height: 32px;
      display: flex;
      align-items: center;
      justify-content: center;
      color: #909399;
      border: 2px solid #dcdfe6;
      border-radius: 50%;
      transition: all 0.3s;

      &.clickable {
        cursor: pointer;
        
        &:hover {
          border-color: #409eff;
          color: #409eff;
          transform: scale(1.1);
        }
      }

      &.selected {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-color: #667eea;
        box-shadow: 0 2px 8px rgba(102, 126, 234, 0.4);
      }
    }

    .el-input {
      flex: 1;
    }
  }

  .options-view {
    .option-view-item {
      display: flex;
      align-items: center;
      gap: 10px;
      padding: 10px 0;
      border-bottom: 1px solid #f0f0f0;

      &:last-child {
        border-bottom: none;
      }

      .option-label {
        font-weight: 600;
        min-width: 32px;
        height: 32px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #909399;
        border: 2px solid #dcdfe6;
        border-radius: 50%;

        &.selected {
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          color: white;
          border-color: #667eea;
        }
      }
    }
  }

  .answer-hint {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 10px 15px;
    background: #e6f7ff;
    border-left: 3px solid #1890ff;
    border-radius: 4px;
    color: #1890ff;
    font-size: 13px;
  }

  .question-stem-view,
  .answer-view {
    padding: 10px 15px;
    background: #f9f9f9;
    border-radius: 6px;
    min-height: 40px;
    line-height: 1.6;
  }

  .metadata-view {
    padding: 8px 0;
    min-height: 32px;
    display: flex;
    align-items: center;
    flex-wrap: wrap;
    gap: 5px;
  }

  .answer-selection {
    padding: 15px;
    background: #f9f9f9;
    border-radius: 6px;
  }
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
