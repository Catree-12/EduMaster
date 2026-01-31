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
          <!-- 只显示选中的题目（内联编辑模式） -->
          <div v-if="selectedQuestion" class="question-block editable">
            <div class="question-block-header">
              <div class="question-block-title">
                <span class="question-num">{{ getQuestionDisplayNumber(selectedQuestion) }}</span>
                <el-tag size="small" type="info">{{ getQuestionTypeLabel(selectedQuestion.type) }}</el-tag>
                <el-input-number 
                  v-if="isEditMode && homework.gradingType === 'custom'"
                  v-model="selectedQuestion.points" 
                  :min="0" 
                  :max="100"
                  size="mini"
                  controls-position="right"
                  @change="updateTotalScore"
                  style="width: 100px; margin-left: 10px;"
                ></el-input-number>
                <span v-else-if="homework.gradingType === 'custom'" style="margin-left: 10px; color: #f56c6c; font-weight: 500;">{{ selectedQuestion.points || 0 }}分</span>
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

                <div v-if="isEditMode" class="answer-hint" style="margin-top: 15px;">
                  <i class="el-icon-info"></i>
                  <span v-if="selectedQuestion.type === 'single'">点击选项字母设置正确答案（单选）</span>
                  <span v-else>点击选项字母设置正确答案（多选）</span>
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

    <!-- 标签管理对话框 -->
    <el-dialog
      title="标签管理"
      :visible.sync="showTagDialog"
      width="600px"
    >
      <div class="tag-management">
        <el-form inline>
          <el-form-item label="标签名称">
            <el-input v-model="newTagName" placeholder="输入标签名称"></el-input>
          </el-form-item>
          <el-form-item label="颜色">
            <el-color-picker v-model="newTagColor"></el-color-picker>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="addTag">添加标签</el-button>
          </el-form-item>
        </el-form>
        <el-table :data="tagList" style="width: 100%; margin-top: 20px;">
          <el-table-column prop="name" label="标签名称">
            <template slot-scope="scope">
              <el-tag :color="scope.row.color" :style="{ color: '#fff' }">{{ scope.row.name }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="count" label="使用次数" width="100"></el-table-column>
          <el-table-column label="操作" width="100">
            <template slot-scope="scope">
              <el-button type="text" size="small" @click="deleteTag(scope.row.id)">删除</el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </el-dialog>

    <!-- 知识点管理对话框 -->
    <el-dialog
      title="知识点管理"
      :visible.sync="showKnowledgeDialog"
      width="700px"
    >
      <div class="knowledge-management">
        <el-form inline>
          <el-form-item label="知识点名称">
            <el-input v-model="newKnowledgeName" placeholder="输入知识点名称"></el-input>
          </el-form-item>
          <el-form-item label="分类">
            <el-select v-model="newKnowledgeCategory" placeholder="选择分类">
              <el-option label="基础知识" value="basic"></el-option>
              <el-option label="核心概念" value="core"></el-option>
              <el-option label="高级应用" value="advanced"></el-option>
              <el-option label="实战技巧" value="practical"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="addKnowledgeQuick">添加知识点</el-button>
          </el-form-item>
        </el-form>
        <div class="knowledge-category-list" style="margin-top: 20px;">
          <el-collapse>
            <el-collapse-item 
              v-for="cat in knowledgeCategories" 
              :key="cat.value"
              :title="`${cat.label}（${getKnowledgeCountByCategory(cat.value)}）`"
            >
              <div v-for="kp in knowledgeList.filter(k => k.category === cat.value)" :key="kp.id" class="knowledge-item">
                <span>{{ kp.name }}</span>
                <el-button type="text" size="small" @click="deleteKnowledge(kp.id)">删除</el-button>
              </div>
            </el-collapse-item>
          </el-collapse>
        </div>
      </div>
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
      showTagDialog: false,
      showKnowledgeDialog: false,
      currentQuestion: {},
      editingIndex: null,
      selectedQuestion: null,
      isEditMode: false, // 编辑模式控制
      // 标签和知识点数据
      tagList: [
        { id: 1, name: '期中考试', color: '#409EFF', count: 5 },
        { id: 2, name: '期末考试', color: '#67C23A', count: 3 },
        { id: 3, name: '月考', color: '#E6A23C', count: 2 }
      ],
      knowledgeList: [
        { id: 1, name: '数据结构', category: 'basic', count: 12 },
        { id: 2, name: '算法分析', category: 'basic', count: 8 },
        { id: 3, name: '面向对象编程', category: 'core', count: 15 }
      ],
      knowledgeCategories: [
        { label: '基础知识', value: 'basic' },
        { label: '核心概念', value: 'core' },
        { label: '高级应用', value: 'advanced' },
        { label: '实战技巧', value: 'practical' }
      ],
      newTagName: '',
      newTagColor: '#409EFF',
      newKnowledgeName: '',
      newKnowledgeCategory: 'basic'
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
      this.isEditMode = false // 切换题目时退出编辑模式
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
      const newQuestion = this.createEmptyQuestion(type)
      this.homework.questions.push(newQuestion)
      this.selectedQuestion = newQuestion
      this.isEditMode = true // 自动进入编辑模式
      this.updateTotalScore()
    },
    createEmptyQuestion(type) {
      const baseQuestion = {
        id: Date.now() + Math.random(),
        type: type,
        title: '',
        points: this.homework.gradingType === 'auto' ? 0 : 10,
        analysis: '', // 答案解析
        difficulty: 0.5, // 默认难度0.5
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
    // 添加选项
    addOption() {
      if (!this.selectedQuestion || !this.selectedQuestion.options) return
      this.selectedQuestion.options.push('')
    },
    // 删除选项
    removeOption(optIdx) {
      if (!this.selectedQuestion || !this.selectedQuestion.options) return
      if (this.selectedQuestion.options.length <= 2) {
        this.$message.warning('至少保留2个选项')
        return
      }
      this.selectedQuestion.options.splice(optIdx, 1)
      
      // 更新答案
      if (this.selectedQuestion.type === 'single' && this.selectedQuestion.answer === optIdx) {
        this.selectedQuestion.answer = null
      } else if (this.selectedQuestion.type === 'multiple' && this.selectedQuestion.answer) {
        const answerIdx = this.selectedQuestion.answer.indexOf(optIdx)
        if (answerIdx > -1) {
          this.selectedQuestion.answer.splice(answerIdx, 1)
        }
        // 调整大于删除索引的答案
        this.selectedQuestion.answer = this.selectedQuestion.answer.map(a => a > optIdx ? a - 1 : a)
      }
    },
    // 标签管理
    addTag() {
      if (!this.newTagName.trim()) {
        this.$message.warning('请输入标签名称')
        return
      }
      const newTag = {
        id: Date.now(),
        name: this.newTagName.trim(),
        color: this.newTagColor,
        count: 0
      }
      this.tagList.push(newTag)
      this.$message.success(`标签"${newTag.name}"创建成功`)
      this.newTagName = ''
      this.newTagColor = '#409EFF'
    },
    deleteTag(tagId) {
      this.$confirm('确定删除此标签？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        const index = this.tagList.findIndex(t => t.id === tagId)
        if (index > -1) {
          this.tagList.splice(index, 1)
          this.$message.success('删除成功')
        }
      }).catch(() => {})
    },
    // 知识点管理
    addKnowledgeQuick() {
      if (!this.newKnowledgeName.trim()) {
        this.$message.warning('请输入知识点名称')
        return
      }
      const newKnowledge = {
        id: Date.now(),
        name: this.newKnowledgeName.trim(),
        category: this.newKnowledgeCategory
      }
      this.knowledgeList.push(newKnowledge)
      this.$message.success(`知识点"${newKnowledge.name}"创建成功`)
      this.newKnowledgeName = ''
      this.newKnowledgeCategory = 'basic'
    },
    deleteKnowledge(kpId) {
      this.$confirm('确定删除此知识点？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        const index = this.knowledgeList.findIndex(k => k.id === kpId)
        if (index > -1) {
          this.knowledgeList.splice(index, 1)
          this.$message.success('删除成功')
        }
      }).catch(() => {})
    },
    getKnowledgeCountByCategory(category) {
      return this.knowledgeList.filter(k => k.category === category).length
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
            this.isEditMode = false
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
  
  &.editable {
    border: 2px solid transparent;
    background: linear-gradient(white, white) padding-box,
                linear-gradient(135deg, #667eea 0%, #764ba2 100%) border-box;
    box-shadow: 0 4px 16px rgba(102, 126, 234, 0.15);
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

.placeholder-text {
  color: #c0c4cc;
  font-style: italic;
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

/* 题目编辑相关样式 */
.edit-label {
  display: block;
  font-size: 13px;
  color: #606266;
  font-weight: 500;
  margin-bottom: 8px;
}

.question-stem-edit,
.answer-edit,
.question-options-edit,
.answer-analysis-edit,
.question-metadata-edit {
  margin-bottom: 20px;
}

.tag-management,
.knowledge-management {
  .knowledge-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 8px 12px;
    border-bottom: 1px solid #f0f0f0;
    
    &:last-child {
      border-bottom: none;
    }
  }
}
</style>

