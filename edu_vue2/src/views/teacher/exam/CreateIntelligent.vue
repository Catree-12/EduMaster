<template>
  <div class="exam-create-intelligent">
    <div class="page-header">
      <button class="back-btn" @click="goBack">
        <span class="back-icon">←</span>
      </button>
      <h1>智能组卷</h1>
    </div>
    
    <div class="content-wrapper">
      <el-card class="config-card">
        <div slot="header" class="card-header">
          <span>组卷配置</span>
        </div>
        
        <el-form :model="examConfig" :rules="rules" ref="examForm" label-width="120px">
          <el-form-item label="试卷名称" prop="name">
            <el-input v-model="examConfig.name" placeholder="请输入试卷名称"></el-input>
          </el-form-item>
          
          <el-form-item label="课程" prop="courseId">
            <el-select v-model="examConfig.courseId" placeholder="请选择课程" style="width: 100%;">
              <el-option 
                v-for="course in courseList" 
                :key="course.id" 
                :label="course.name" 
                :value="course.id"
              ></el-option>
            </el-select>
          </el-form-item>
          
          <el-form-item label="总题数" prop="totalQuestions">
            <el-input-number 
              v-model="examConfig.totalQuestions" 
              :min="5" 
              :max="100"
              controls-position="right"
            ></el-input-number>
          </el-form-item>
          
          <el-form-item label="总分" prop="totalScore">
            <el-input-number 
              v-model="examConfig.totalScore" 
              :min="50" 
              :max="200"
              controls-position="right"
            ></el-input-number>
          </el-form-item>
          
          <el-form-item label="试卷难度">
            <el-radio-group v-model="examConfig.difficulty">
              <el-radio label="easy">易</el-radio>
              <el-radio label="medium">中</el-radio>
              <el-radio label="hard">难</el-radio>
            </el-radio-group>
          </el-form-item>
          
          <el-divider>题型配置</el-divider>
          
          <div v-for="(qType, index) in examConfig.questionTypes" :key="index" class="question-type-config">
            <el-row :gutter="20">
              <el-col :span="8">
                <el-form-item :label="qType.label">
                  <el-input-number 
                    v-model="qType.count" 
                    :min="0" 
                    :max="50"
                    controls-position="right"
                    @change="calculateScore"
                  ></el-input-number>
                </el-form-item>
              </el-col>
              <el-col :span="8">
                <el-form-item label="每题分值">
                  <el-input-number 
                    v-model="qType.pointsPerQuestion" 
                    :min="1" 
                    :max="20"
                    :precision="1"
                    controls-position="right"
                    @change="calculateScore"
                  ></el-input-number>
                </el-form-item>
              </el-col>
              <el-col :span="8">
                <el-form-item label="小计">
                  <el-tag type="success">{{ (qType.count * qType.pointsPerQuestion).toFixed(1) }} 分</el-tag>
                </el-form-item>
              </el-col>
            </el-row>
          </div>
          
          <el-divider>知识点筛选</el-divider>
          
          <el-form-item label="知识点范围">
            <el-select 
              v-model="examConfig.knowledgePoints" 
              multiple 
              filterable
              placeholder="请选择知识点（不选则全部）"
              style="width: 100%;"
            >
              <el-option 
                v-for="kp in knowledgePointList" 
                :key="kp.id" 
                :label="kp.name" 
                :value="kp.id"
              ></el-option>
            </el-select>
          </el-form-item>
          
          <el-form-item label="题目标签">
            <el-select 
              v-model="examConfig.tags" 
              multiple 
              filterable
              placeholder="请选择标签（可选）"
              style="width: 100%;"
            >
              <el-option 
                v-for="tag in tagList" 
                :key="tag.id" 
                :label="tag.name" 
                :value="tag.id"
              ></el-option>
            </el-select>
          </el-form-item>
          
          <el-form-item>
            <el-button type="primary" @click="generateExam" :loading="generating">
              <i class="el-icon-magic-stick"></i> 智能生成试卷
            </el-button>
            <el-button @click="resetForm">重置</el-button>
          </el-form-item>
        </el-form>
      </el-card>
      
      <!-- 预览生成的试卷 -->
      <el-card v-if="generatedExam" class="preview-card">
        <div slot="header" class="card-header">
          <span>生成的试卷预览</span>
          <el-button type="text" @click="confirmExam">确认并编辑</el-button>
        </div>
        
        <div class="exam-summary">
          <h3>{{ generatedExam.name }}</h3>
          <div class="summary-info">
            <el-tag>题量: {{ generatedExam.questionCount }}</el-tag>
            <el-tag type="success">总分: {{ generatedExam.totalScore }}分</el-tag>
            <el-tag type="warning">难度: {{ getDifficultyLabel(generatedExam.difficulty) }}</el-tag>
          </div>
        </div>
        
        <el-divider></el-divider>
        
        <div class="question-list">
          <div v-for="(question, index) in generatedExam.questions" :key="index" class="question-item">
            <div class="question-header">
              <span class="question-num">{{ index + 1 }}.</span>
              <el-tag size="small" type="info">{{ getQuestionTypeLabel(question.type) }}</el-tag>
              <span class="question-score">{{ question.points }}分</span>
            </div>
            <div class="question-content">{{ question.title || '（题目内容）' }}</div>
          </div>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ExamCreateIntelligent',
  data() {
    return {
      examConfig: {
        name: '',
        courseId: null,
        totalQuestions: 20,
        totalScore: 100,
        difficulty: 'medium',
        questionTypes: [
          { type: 'single', label: '单选题', count: 10, pointsPerQuestion: 2 },
          { type: 'multiple', label: '多选题', count: 5, pointsPerQuestion: 4 },
          { type: 'fill', label: '填空题', count: 3, pointsPerQuestion: 5 },
          { type: 'judge', label: '判断题', count: 5, pointsPerQuestion: 2 },
          { type: 'essay', label: '简答题', count: 2, pointsPerQuestion: 10 }
        ],
        knowledgePoints: [],
        tags: []
      },
      rules: {
        name: [
          { required: true, message: '请输入试卷名称', trigger: 'blur' }
        ],
        courseId: [
          { required: true, message: '请选择课程', trigger: 'change' }
        ],
        totalQuestions: [
          { required: true, message: '请设置总题数', trigger: 'blur' }
        ],
        totalScore: [
          { required: true, message: '请设置总分', trigger: 'blur' }
        ]
      },
      courseList: [
        { id: 1, name: '数据结构与算法' },
        { id: 2, name: 'Web前端开发' },
        { id: 3, name: 'Python编程基础' }
      ],
      knowledgePointList: [
        { id: 1, name: '数据结构' },
        { id: 2, name: '算法分析' },
        { id: 3, name: '排序算法' },
        { id: 4, name: '树与图' }
      ],
      tagList: [
        { id: 1, name: '期中考试' },
        { id: 2, name: '期末考试' },
        { id: 3, name: '单元测试' }
      ],
      generating: false,
      generatedExam: null
    }
  },
  mounted() {
    // 初始化试卷名称
    this.examConfig.name = '智能试卷_' + new Date().toISOString().slice(0, 10)
  },
  methods: {
    goBack() {
      this.$router.back()
    },
    calculateScore() {
      // 自动计算总分
      let total = 0
      let count = 0
      this.examConfig.questionTypes.forEach(qType => {
        total += qType.count * qType.pointsPerQuestion
        count += qType.count
      })
      this.examConfig.totalScore = total
      this.examConfig.totalQuestions = count
    },
    generateExam() {
      this.$refs.examForm.validate((valid) => {
        if (!valid) {
          return false
        }
        
        this.generating = true
        
        // 模拟生成试卷
        setTimeout(() => {
          const questions = []
          this.examConfig.questionTypes.forEach(qType => {
            for (let i = 0; i < qType.count; i++) {
              questions.push({
                id: Date.now() + Math.random(),
                type: qType.type,
                title: `这是一道${qType.label}示例题目 ${i + 1}`,
                points: qType.pointsPerQuestion,
                options: ['single', 'multiple'].includes(qType.type) ? ['选项A', '选项B', '选项C', '选项D'] : undefined,
                answer: qType.type === 'single' ? 0 : (qType.type === 'multiple' ? [0, 1] : '答案示例'),
                difficulty: this.examConfig.difficulty,
                knowledgePoints: [],
                tags: []
              })
            }
          })
          
          this.generatedExam = {
            name: this.examConfig.name,
            courseId: this.examConfig.courseId,
            difficulty: this.examConfig.difficulty,
            questionCount: questions.length,
            totalScore: this.examConfig.totalScore,
            questions: questions
          }
          
          this.generating = false
          this.$message.success('试卷生成成功！')
        }, 2000)
      })
    },
    confirmExam() {
      // 将生成的试卷数据保存到 sessionStorage，然后跳转到编辑页面
      sessionStorage.setItem('editExamData', JSON.stringify(this.generatedExam))
      
      this.$router.push({
        path: '/teacher/exam-create',
        query: {
          mode: 'manual',
          action: 'edit',
          id: this.generatedExam.id || 'new'
        }
      })
    },
    resetForm() {
      this.$refs.examForm.resetFields()
      this.generatedExam = null
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
    }
  }
}
</script>

<style scoped lang="scss">
.exam-create-intelligent {
  min-height: 100vh;
  background: #f5f7fa;
  padding: 20px;
}

.page-header {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 30px;
  
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
  
  h1 {
    margin: 0;
    font-size: 24px;
    color: #303133;
  }
}

.content-wrapper {
  max-width: 1200px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  
  @media (max-width: 1200px) {
    grid-template-columns: 1fr;
  }
}

.config-card,
.preview-card {
  height: fit-content;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: 600;
  font-size: 16px;
}

.question-type-config {
  margin-bottom: 20px;
  padding: 15px;
  background: #f9f9f9;
  border-radius: 4px;
}

.exam-summary {
  margin-bottom: 20px;
  
  h3 {
    margin: 0 0 12px 0;
    font-size: 20px;
    color: #303133;
  }
  
  .summary-info {
    display: flex;
    gap: 10px;
  }
}

.question-list {
  max-height: 500px;
  overflow-y: auto;
}

.question-item {
  padding: 15px;
  margin-bottom: 12px;
  background: #fafbfc;
  border-radius: 4px;
  border: 1px solid #e5e7eb;
  
  .question-header {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 8px;
    
    .question-num {
      font-weight: 600;
      color: #303133;
    }
    
    .question-score {
      margin-left: auto;
      color: #f56c6c;
      font-weight: 500;
    }
  }
  
  .question-content {
    color: #606266;
    font-size: 14px;
    line-height: 1.6;
  }
}

::v-deep .el-divider__text {
  background: #f5f7fa;
  font-weight: 600;
  color: #606266;
}
</style>
