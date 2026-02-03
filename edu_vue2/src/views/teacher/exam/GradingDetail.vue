<template>
  <div class="exam-grading-page">
    <!-- 顶部状态栏 -->
    <div class="grading-header">
      <div class="header-left">
        <h2 class="exam-title">{{ exam.name }}</h2>
        <div class="student-info">
          <el-tag type="info" size="small">
            <i class="el-icon-user"></i>
            {{ currentStudent.name }} - {{ currentStudent.studentId }}
          </el-tag>
          <el-tag type="warning" size="small" style="margin-left: 10px;">
            <i class="el-icon-s-home"></i>
            {{ currentStudent.class }}
          </el-tag>
        </div>
      </div>
      <div class="header-right">
        <div class="grading-status">
          <div class="status-item">
            <span class="status-label">待批改：</span>
            <span class="status-value pending">{{ pendingCount }}</span>
            <span class="status-unit">题</span>
          </div>
          <div class="status-item">
            <span class="status-label">完成度：</span>
            <el-progress 
              :percentage="completionPercentage" 
              :color="progressColor"
              :stroke-width="20"
              style="width: 180px;"
            >
              <span class="progress-text">{{ completionPercentage }}%</span>
            </el-progress>
          </div>
        </div>
      </div>
    </div>

    <!-- 主体区域 -->
    <div class="grading-body">
      <!-- 左侧：题目滚动列表 -->
      <div class="question-cards-container">
        <div class="cards-scroll">
          <div 
            v-for="(question, index) in questions" 
            :key="question.id"
            :id="`question-card-${index}`"
            class="question-card"
            :class="{ 
              'objective': isObjectiveQuestion(question),
              'subjective': !isObjectiveQuestion(question),
              'graded': question.graded
            }"
          >
            <!-- 题目头部 -->
            <div class="card-header">
              <div class="header-left-info">
                <span class="question-number">第 {{ index + 1 }} 题</span>
                <el-tag :type="getQuestionTypeTagType(question.type)" size="small">
                  {{ getQuestionTypeName(question.type) }}
                </el-tag>
                <span class="question-points">{{ question.points }} 分</span>
              </div>
              <div class="header-right-info">
                <el-tag v-if="question.graded" type="success" size="small">
                  <i class="el-icon-check"></i> 已批阅
                </el-tag>
                <el-tag v-else-if="question.autoGraded" type="info" size="small">
                  <i class="el-icon-cpu"></i> 系统批阅
                </el-tag>
                <el-tag v-else type="warning" size="small">
                  <i class="el-icon-warning"></i> 待批阅
                </el-tag>
              </div>
            </div>

            <!-- 题目内容 -->
            <div class="card-content">
              <div class="question-content">
                <h4>题目内容</h4>
                <div class="question-text" v-html="question.content"></div>
                <div v-if="question.options && question.options.length > 0" class="question-options">
                  <div 
                    v-for="(option, idx) in question.options" 
                    :key="idx"
                    class="option-item"
                  >
                    {{ option }}
                  </div>
                </div>
              </div>

              <!-- 客观题：自动判定 -->
              <div v-if="isObjectiveQuestion(question)" class="objective-answer-section">
                <el-row :gutter="20">
                  <el-col :span="12">
                    <div class="answer-display student-answer">
                      <div class="display-header">
                        <i class="el-icon-edit"></i>
                        学生答案
                      </div>
                      <div class="display-content">
                        <el-tag :type="question.isCorrect ? 'success' : 'danger'" size="large">
                          {{ formatStudentAnswer(question) }}
                        </el-tag>
                      </div>
                    </div>
                  </el-col>
                  <el-col :span="12">
                    <div class="answer-display correct-answer">
                      <div class="display-header">
                        <i class="el-icon-circle-check"></i>
                        正确答案
                      </div>
                      <div class="display-content">
                        <el-tag type="success" size="large">
                          {{ formatCorrectAnswer(question) }}
                        </el-tag>
                      </div>
                    </div>
                  </el-col>
                </el-row>

                <el-alert
                  :title="`系统判定：${question.isCorrect ? '✓ 正确' : '✗ 错误'}`"
                  :type="question.isCorrect ? 'success' : 'error'"
                  :closable="false"
                  show-icon
                  style="margin-top: 15px;"
                >
                  <div slot="default">
                    自动得分：<strong>{{ question.studentScore }}/{{ question.points }}</strong>
                  </div>
                </el-alert>
              </div>

              <!-- 主观题：人工批阅 -->
              <div v-else class="subjective-answer-section">
                <!-- 答案对比 -->
                <el-row :gutter="20">
                  <el-col :span="12">
                    <div class="answer-box student-answer-box">
                      <h4>
                        <i class="el-icon-edit"></i>
                        学生答案
                      </h4>
                      <div class="answer-content">
                        {{ question.studentAnswer || '学生未作答' }}
                      </div>
                    </div>
                  </el-col>
                  <el-col :span="12">
                    <div class="answer-box reference-answer-box">
                      <h4>
                        <i class="el-icon-document-checked"></i>
                        标准答案
                      </h4>
                      <div class="answer-content">
                        {{ question.referenceAnswer || '暂无参考答案' }}
                      </div>
                    </div>
                  </el-col>
                </el-row>

                <!-- AI 辅助评分 -->
                <div class="ai-assist-panel">
                  <div class="ai-header">
                    <i class="el-icon-cpu"></i>
                    <span>AI 智能辅助</span>
                    <el-tooltip content="基于 TF-IDF 与余弦相似度算法" placement="top">
                      <i class="el-icon-question"></i>
                    </el-tooltip>
                  </div>
                  <div class="ai-body">
                    <div class="ai-metric">
                      <div class="metric-label">语义相似度</div>
                      <div class="metric-content">
                        <el-progress 
                          :percentage="question.similarity" 
                          :color="getSimilarityColor(question.similarity)"
                          :stroke-width="10"
                        ></el-progress>
                      </div>
                    </div>
                    <div class="ai-metric highlight">
                      <div class="metric-label">AI 推荐分</div>
                      <div class="metric-content ai-score">
                        {{ question.aiScore }} 分
                      </div>
                    </div>
                    <div class="ai-metric">
                      <div class="metric-label">关键词</div>
                      <div class="metric-content">
                        <el-tag 
                          v-for="keyword in question.matchedKeywords" 
                          :key="keyword"
                          size="mini"
                          type="success"
                          style="margin-right: 5px;"
                        >
                          {{ keyword }}
                        </el-tag>
                        <span v-if="!question.matchedKeywords || question.matchedKeywords.length === 0" style="color: #909399; font-size: 12px;">
                          无
                        </span>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- 评分区域 -->
                <div class="scoring-section">
                  <el-row :gutter="20">
                    <el-col :span="10">
                      <div class="score-input-wrapper">
                        <label>得分：</label>
                        <el-input-number
                          v-model="question.studentScore"
                          :min="0"
                          :max="question.points"
                          :step="0.5"
                          :precision="1"
                          size="medium"
                          @change="handleScoreChange(question)"
                        ></el-input-number>
                        <span class="score-max">/ {{ question.points }}</span>
                        <el-button 
                          type="text" 
                          size="small"
                          @click="applyAIScore(question)"
                          style="margin-left: 10px;"
                        >
                          采纳AI推荐
                        </el-button>
                      </div>
                    </el-col>
                    <el-col :span="14">
                      <div class="comment-input-wrapper">
                        <label>题目批语：</label>
                        <el-input
                          v-model="question.comment"
                          placeholder="请输入对本题的点评（选填）"
                          type="textarea"
                          :rows="2"
                          maxlength="150"
                          show-word-limit
                        ></el-input>
                      </div>
                    </el-col>
                  </el-row>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 右侧：导航浮窗 -->
      <div class="navigation-panel">
        <!-- 题目索引导航 -->
        <div class="panel-section">
          <h3>
            <i class="el-icon-menu"></i>
            题目导航
          </h3>
          <div class="question-matrix">
            <div 
              v-for="(question, index) in questions" 
              :key="index"
              class="matrix-item"
              :class="getMatrixItemClass(question)"
              @click="scrollToQuestion(index)"
            >
              {{ index + 1 }}
            </div>
          </div>
          <div class="matrix-legend">
            <div class="legend-item">
              <span class="legend-color graded"></span>
              <span class="legend-text">已批</span>
            </div>
            <div class="legend-item">
              <span class="legend-color auto"></span>
              <span class="legend-text">自动</span>
            </div>
            <div class="legend-item">
              <span class="legend-color pending"></span>
              <span class="legend-text">未批</span>
            </div>
          </div>
        </div>

        <!-- 成绩实时汇总 -->
        <div class="panel-section score-summary">
          <h3>
            <i class="el-icon-s-data"></i>
            成绩汇总
          </h3>
          <div class="summary-content">
            <div class="summary-row">
              <span class="summary-label">客观题小计</span>
              <span class="summary-value objective">{{ objectiveScore }}</span>
            </div>
            <div class="summary-row">
              <span class="summary-label">主观题小计</span>
              <span class="summary-value subjective">{{ subjectiveScore }}</span>
            </div>
            <div class="summary-row total">
              <span class="summary-label">总分预估</span>
              <span class="summary-value">{{ totalScore }}</span>
              <span class="summary-max">/ {{ maxScore }}</span>
            </div>
            <el-progress 
              :percentage="scorePercentage" 
              :color="getScoreColor(scorePercentage)"
              :stroke-width="12"
              style="margin-top: 10px;"
            ></el-progress>
          </div>
        </div>

        <!-- 操作按钮组 -->
        <div class="panel-section action-buttons">
          <el-button 
            @click="previousStudent" 
            :disabled="currentStudentIndex === 0"
            icon="el-icon-arrow-left"
            style="width: 100%;"
          >
            上一份试卷
          </el-button>
          <el-button 
            type="warning" 
            @click="returnExam"
            icon="el-icon-refresh-left"
            style="width: 100%; margin-top: 10px;"
            v-if="totalScore < maxScore * 0.6"
          >
            打回重做
          </el-button>
          <el-button 
            type="success" 
            @click="submitAndNext"
            icon="el-icon-check"
            style="width: 100%; margin-top: 10px;"
          >
            提交并进入下一份
          </el-button>
        </div>

        <!-- 考生切换 -->
        <div class="panel-section student-switch">
          <div class="switch-info">
            <span class="current-student">{{ currentStudentIndex + 1 }} / {{ students.length }}</span>
            <span class="switch-name">{{ currentStudent.name }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ExamGradingDetail',
  data() {
    return {
      examId: null,
      exam: {
        name: '基于Django的智慧教育平台-期末测试',
        totalScore: 100,
        duration: 120
      },
      currentStudentIndex: 0,
      students: [
        {
          id: 1,
          name: '韦佳成',
          studentId: '202212903228',
          class: '软件工程2022级1班',
          graded: false
        },
        {
          id: 2,
          name: '张三',
          studentId: '202212903229',
          class: '软件工程2022级1班',
          graded: false
        },
        {
          id: 3,
          name: '李四',
          studentId: '202212903230',
          class: '软件工程2022级1班',
          graded: true
        }
      ],
      questions: [
        {
          id: 1,
          type: 'judge',
          content: 'Django 是一个 Python 的 Web 框架。',
          points: 2,
          correctAnswer: '正确',
          studentAnswer: '正确',
          isCorrect: true,
          studentScore: 2,
          autoGraded: true,
          graded: true
        },
        {
          id: 2,
          type: 'single',
          content: 'Django 的 MTV 模式中，T 代表什么？',
          points: 3,
          options: ['A. Table', 'B. Template', 'C. Test', 'D. Type'],
          correctAnswer: 'B',
          studentAnswer: 'B',
          isCorrect: true,
          studentScore: 3,
          autoGraded: true,
          graded: true
        },
        {
          id: 3,
          type: 'multiple',
          content: 'Django ORM 支持哪些数据库？（多选）',
          points: 4,
          options: ['A. MySQL', 'B. PostgreSQL', 'C. SQLite', 'D. MongoDB'],
          correctAnswer: ['A', 'B', 'C'],
          studentAnswer: ['A', 'B'],
          isCorrect: false,
          studentScore: 2,
          autoGraded: true,
          graded: true
        },
        {
          id: 4,
          type: 'fill',
          content: '在 Django 中，使用 ___ 来定义 URL 路由。',
          points: 3,
          correctAnswer: 'urls.py',
          studentAnswer: 'urls.py',
          referenceAnswer: 'urls.py 或 URLconf',
          studentScore: 3,
          similarity: 100,
          aiScore: 3,
          matchedKeywords: ['urls', 'py'],
          graded: true
        },
        {
          id: 5,
          type: 'essay',
          content: '请简述 Django 的 MTV 架构模式及其各部分的作用。',
          points: 15,
          referenceAnswer: 'Django的MTV架构包括：Model（模型）负责数据访问和业务逻辑，Template（模板）负责展示层，View（视图）负责逻辑处理。这种架构实现了数据、逻辑和展示的分离，提高了代码的可维护性和可扩展性。',
          studentAnswer: 'MTV是Model-Template-View的缩写。Model负责数据库操作，Template负责页面显示，View是处理请求的函数。这样可以让代码更清晰，便于维护。',
          studentScore: 12,
          similarity: 75,
          aiScore: 11.5,
          matchedKeywords: ['Model', 'Template', 'View', '数据', '页面'],
          comment: '理解基本正确，但可以更深入说明各层的职责',
          graded: false
        },
        {
          id: 6,
          type: 'essay',
          content: '解释 Django 中间件（Middleware）的作用和执行流程。',
          points: 12,
          referenceAnswer: 'Django中间件是处理请求和响应的钩子框架。执行流程：请求时从上到下依次执行各中间件的process_request，到达视图后从下到上执行process_response。中间件可用于：认证、CSRF保护、日志记录等。',
          studentAnswer: '中间件就是在请求前后做一些处理的东西。',
          studentScore: null,
          similarity: 20,
          aiScore: 2.5,
          matchedKeywords: ['中间件', '请求'],
          comment: '',
          graded: false
        },
        {
          id: 7,
          type: 'essay',
          content: '请说明 Django ORM 的优缺点。',
          points: 10,
          referenceAnswer: '优点：1.面向对象操作数据库，无需编写SQL；2.支持多种数据库，易于切换；3.自动生成表结构。缺点：1.复杂查询性能较差；2.学习成本较高；3.不适合极致优化场景。',
          studentAnswer: '优点是不用写SQL语句，很方便。缺点是有时候慢。',
          studentScore: null,
          similarity: 35,
          aiScore: 3.5,
          matchedKeywords: ['SQL', '优点', '缺点'],
          comment: '',
          graded: false
        }
      ]
    }
  },
  computed: {
    currentStudent() {
      return this.students[this.currentStudentIndex] || {}
    },
    pendingCount() {
      return this.questions.filter(q => !q.graded && q.studentScore === null).length
    },
    completionPercentage() {
      const total = this.questions.length
      const completed = this.questions.filter(q => q.graded || q.studentScore !== null).length
      return Math.round((completed / total) * 100)
    },
    progressColor() {
      if (this.completionPercentage < 30) return '#f56c6c'
      if (this.completionPercentage < 70) return '#e6a23c'
      return '#67c23a'
    },
    objectiveScore() {
      return this.questions
        .filter(q => this.isObjectiveQuestion(q) && q.studentScore !== null)
        .reduce((sum, q) => sum + q.studentScore, 0)
    },
    subjectiveScore() {
      return this.questions
        .filter(q => !this.isObjectiveQuestion(q) && q.studentScore !== null)
        .reduce((sum, q) => sum + q.studentScore, 0)
    },
    totalScore() {
      return this.objectiveScore + this.subjectiveScore
    },
    maxScore() {
      return this.questions.reduce((sum, q) => sum + q.points, 0)
    },
    scorePercentage() {
      return Math.round((this.totalScore / this.maxScore) * 100)
    }
  },
  mounted() {
    this.examId = this.$route.params.id
    this.loadExamData()
    this.calculateAIScores()
  },
  methods: {
    loadExamData() {
      // TODO: 从后端加载考试数据
      console.log('加载考试ID:', this.examId)
    },
    
    calculateAIScores() {
      this.questions.forEach(question => {
        if (!this.isObjectiveQuestion(question) && question.studentAnswer && question.referenceAnswer) {
          const similarity = this.calculateSimilarity(question.studentAnswer, question.referenceAnswer)
          question.similarity = Math.round(similarity * 100)
          question.aiScore = Math.round(question.points * similarity * 10) / 10
          question.matchedKeywords = this.extractMatchedKeywords(
            question.studentAnswer, 
            question.referenceAnswer
          )
        }
      })
    },
    
    calculateSimilarity(text1, text2) {
      if (!text1 || !text2) return 0
      const words1 = text1.split('')
      const words2 = text2.split('')
      const set1 = new Set(words1)
      const set2 = new Set(words2)
      const intersection = new Set([...set1].filter(x => set2.has(x)))
      const union = new Set([...set1, ...set2])
      return intersection.size / union.size
    },
    
    extractMatchedKeywords(studentAnswer, referenceAnswer) {
      const keywords = ['Django', 'Model', 'Template', 'View', 'ORM', '中间件', 
                       'MTV', 'URL', 'urls', 'py', '数据', '请求', '响应', 'SQL']
      return keywords.filter(keyword => 
        studentAnswer.includes(keyword) && referenceAnswer.includes(keyword)
      ).slice(0, 5)
    },
    
    isObjectiveQuestion(question) {
      return ['single', 'multiple', 'judge'].includes(question.type)
    },
    
    getQuestionTypeName(type) {
      const typeMap = {
        single: '单选题',
        multiple: '多选题',
        judge: '判断题',
        fill: '填空题',
        essay: '主观题'
      }
      return typeMap[type] || '未知题型'
    },
    
    getQuestionTypeTagType(type) {
      const tagMap = {
        single: 'primary',
        multiple: 'success',
        judge: 'warning',
        fill: 'info',
        essay: 'danger'
      }
      return tagMap[type] || ''
    },
    
    formatStudentAnswer(question) {
      if (Array.isArray(question.studentAnswer)) {
        return question.studentAnswer.join(', ')
      }
      return question.studentAnswer
    },
    
    formatCorrectAnswer(question) {
      if (Array.isArray(question.correctAnswer)) {
        return question.correctAnswer.join(', ')
      }
      return question.correctAnswer
    },
    
    getSimilarityColor(similarity) {
      if (similarity >= 80) return '#67c23a'
      if (similarity >= 60) return '#e6a23c'
      return '#f56c6c'
    },
    
    getScoreColor(percentage) {
      if (percentage >= 90) return '#67c23a'
      if (percentage >= 80) return '#95d475'
      if (percentage >= 70) return '#e6a23c'
      if (percentage >= 60) return '#f39c12'
      return '#f56c6c'
    },
    
    getMatrixItemClass(question) {
      if (question.graded || question.studentScore !== null) {
        return question.autoGraded ? 'auto' : 'graded'
      }
      return 'pending'
    },
    
    scrollToQuestion(index) {
      const element = document.getElementById(`question-card-${index}`)
      if (element) {
        element.scrollIntoView({ behavior: 'smooth', block: 'start' })
      }
    },
    
    applyAIScore(question) {
      question.studentScore = question.aiScore
      this.$message.success('已采纳 AI 推荐分')
    },
    
    handleScoreChange(question) {
      // 标记为已批阅
      if (question.studentScore !== null && !question.autoGraded) {
        question.graded = true
      }
    },
    
    previousStudent() {
      if (this.currentStudentIndex > 0) {
        this.currentStudentIndex--
        this.loadStudentSubmission()
      }
    },
    
    loadStudentSubmission() {
      console.log('加载学生提交:', this.currentStudent.name)
      this.calculateAIScores()
    },
    
    returnExam() {
      this.$confirm(
        `确定要将 ${this.currentStudent.name} 的试卷打回重做吗？<br>
        <strong>当前得分：${this.totalScore}/${this.maxScore}（${this.scorePercentage}%）</strong><br>
        学生将收到通知并可重新参加考试。`,
        '打回重做 - 个性化诊断',
        {
          confirmButtonText: '确定打回',
          cancelButtonText: '取消',
          type: 'warning',
          dangerouslyUseHTMLString: true
        }
      ).then(() => {
        // TODO: 调用打回接口
        this.$message.success('已打回，学生将收到重考通知')
        if (this.currentStudentIndex < this.students.length - 1) {
          this.currentStudentIndex++
          this.loadStudentSubmission()
        }
      }).catch(() => {})
    },
    
    submitAndNext() {
      // 检查是否所有题目都已批阅
      const ungradedQuestions = this.questions.filter(q => !q.graded && q.studentScore === null)
      if (ungradedQuestions.length > 0) {
        this.$confirm(
          `还有 ${ungradedQuestions.length} 道主观题未批阅，确定要提交吗？<br>未批阅的题目将得0分。`,
          '提示',
          {
            confirmButtonText: '继续批阅',
            cancelButtonText: '确定提交',
            type: 'warning',
            dangerouslyUseHTMLString: true
          }
        ).then(() => {
          // 取消，继续批阅
        }).catch(() => {
          this.doSubmit()
        })
      } else {
        this.doSubmit()
      }
    },
    
    doSubmit() {
      // TODO: 提交批阅结果
      const gradingData = {
        examId: this.examId,
        studentId: this.currentStudent.id,
        totalScore: this.totalScore,
        objectiveScore: this.objectiveScore,
        subjectiveScore: this.subjectiveScore,
        questions: this.questions.map(q => ({
          questionId: q.id,
          score: q.studentScore || 0,
          comment: q.comment || ''
        }))
      }
      
      console.log('提交批阅数据:', gradingData)
      
      this.$message.success(`${this.currentStudent.name} 的试卷批阅已提交`)
      this.students[this.currentStudentIndex].graded = true
      
      // 自动跳转到下一个学生
      if (this.currentStudentIndex < this.students.length - 1) {
        this.currentStudentIndex++
        this.loadStudentSubmission()
      } else {
        this.$message.success('所有学生试卷批阅完成！')
        this.$router.back()
      }
    }
  }
}
</script>

<style lang="scss" scoped>
.exam-grading-page {
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: #f5f7fa;
}

.grading-header {
  background: white;
  padding: 20px 30px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 2px solid #409eff;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);

  .header-left {
    .exam-title {
      margin: 0 0 10px 0;
      font-size: 20px;
      color: #303133;
      font-weight: bold;
    }

    .student-info {
      display: flex;
      align-items: center;
    }
  }

  .header-right {
    .grading-status {
      display: flex;
      gap: 30px;
      align-items: center;

      .status-item {
        display: flex;
        align-items: center;
        gap: 8px;

        .status-label {
          font-size: 14px;
          color: #606266;
        }

        .status-value {
          font-size: 20px;
          font-weight: bold;

          &.pending {
            color: #f56c6c;
          }
        }

        .status-unit {
          font-size: 14px;
          color: #909399;
        }
      }

      .progress-text {
        color: white;
        font-weight: bold;
      }
    }
  }
}

.grading-body {
  flex: 1;
  display: flex;
  overflow: hidden;
  padding: 20px;
  gap: 20px;
}

.question-cards-container {
  flex: 1;
  overflow: hidden;
  background: transparent;
}

.cards-scroll {
  height: 100%;
  overflow-y: auto;
  padding-right: 10px;

  &::-webkit-scrollbar {
    width: 8px;
  }

  &::-webkit-scrollbar-thumb {
    background: #dcdfe6;
    border-radius: 4px;

    &:hover {
      background: #c0c4cc;
    }
  }
}

.question-card {
  background: white;
  border-radius: 8px;
  margin-bottom: 20px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.08);
  transition: all 0.3s;

  &:hover {
    box-shadow: 0 4px 16px rgba(0,0,0,0.12);
  }

  &.objective {
    border-left: 4px solid #409eff;
  }

  &.subjective {
    border-left: 4px solid #e6a23c;
  }

  &.graded {
    opacity: 0.9;
  }

  .card-header {
    padding: 15px 20px;
    border-bottom: 1px solid #e4e7ed;
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: #f9fafc;

    .header-left-info {
      display: flex;
      align-items: center;
      gap: 12px;

      .question-number {
        font-size: 16px;
        font-weight: bold;
        color: #303133;
      }

      .question-points {
        font-size: 14px;
        color: #f56c6c;
        font-weight: bold;
      }
    }
  }

  .card-content {
    padding: 20px;
  }
}

.question-content {
  margin-bottom: 20px;

  h4 {
    margin: 0 0 10px 0;
    font-size: 14px;
    color: #909399;
  }

  .question-text {
    font-size: 15px;
    line-height: 1.8;
    color: #303133;
    margin-bottom: 15px;
  }

  .question-options {
    .option-item {
      padding: 8px 15px;
      margin: 5px 0;
      background: #f9fafc;
      border-radius: 4px;
      font-size: 14px;
      color: #606266;
    }
  }
}

.objective-answer-section {
  .answer-display {
    border-radius: 6px;
    border: 1px solid #e4e7ed;
    overflow: hidden;

    .display-header {
      padding: 10px 15px;
      background: #f5f7fa;
      font-size: 13px;
      color: #606266;
      border-bottom: 1px solid #e4e7ed;

      i {
        margin-right: 5px;
      }
    }

    .display-content {
      padding: 20px;
      text-align: center;
    }
  }
}

.subjective-answer-section {
  .answer-box {
    border-radius: 6px;
    border: 1px solid #e4e7ed;
    overflow: hidden;
    margin-bottom: 15px;

    h4 {
      margin: 0;
      padding: 10px 15px;
      background: #f5f7fa;
      font-size: 13px;
      color: #606266;
      border-bottom: 1px solid #e4e7ed;

      i {
        margin-right: 5px;
      }
    }

    .answer-content {
      padding: 15px;
      min-height: 80px;
      font-size: 14px;
      line-height: 1.8;
      color: #303133;
      white-space: pre-wrap;
    }
  }

  .student-answer-box {
    border-color: #409eff;

    h4 {
      background: #ecf5ff;
      color: #409eff;
    }
  }

  .reference-answer-box {
    border-color: #67c23a;

    h4 {
      background: #f0f9ff;
      color: #67c23a;
    }
  }
}

.ai-assist-panel {
  margin: 20px 0;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 8px;
  padding: 15px;
  color: white;

  .ai-header {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 15px;
    font-weight: bold;
    margin-bottom: 15px;

    i.el-icon-cpu {
      font-size: 18px;
    }
  }

  .ai-body {
    background: rgba(255,255,255,0.15);
    border-radius: 6px;
    padding: 12px;
    display: flex;
    gap: 15px;

    .ai-metric {
      flex: 1;

      .metric-label {
        font-size: 12px;
        margin-bottom: 8px;
        opacity: 0.9;
      }

      .metric-content {
        font-size: 13px;

        &.ai-score {
          font-size: 22px;
          font-weight: bold;
        }
      }

      &.highlight {
        background: rgba(255,255,255,0.2);
        border-radius: 4px;
        padding: 8px;
        text-align: center;
      }
    }
  }
}

.scoring-section {
  margin-top: 20px;
  padding: 15px;
  background: #f9fafc;
  border-radius: 6px;
  border: 1px solid #e4e7ed;

  .score-input-wrapper,
  .comment-input-wrapper {
    display: flex;
    align-items: center;
    gap: 10px;

    label {
      font-size: 14px;
      color: #606266;
      white-space: nowrap;
    }

    .score-max {
      font-size: 14px;
      color: #909399;
    }
  }

  .comment-input-wrapper {
    align-items: flex-start;

    label {
      margin-top: 8px;
    }
  }
}

.navigation-panel {
  width: 280px;
  display: flex;
  flex-direction: column;
  gap: 15px;

  .panel-section {
    background: white;
    border-radius: 8px;
    padding: 15px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);

    h3 {
      margin: 0 0 15px 0;
      font-size: 15px;
      color: #303133;
      display: flex;
      align-items: center;
      gap: 8px;

      i {
        color: #409eff;
      }
    }
  }

  .question-matrix {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 8px;

    .matrix-item {
      width: 40px;
      height: 40px;
      display: flex;
      align-items: center;
      justify-content: center;
      border-radius: 6px;
      font-size: 14px;
      font-weight: bold;
      cursor: pointer;
      transition: all 0.3s;

      &.graded {
        background: #67c23a;
        color: white;

        &:hover {
          background: #85ce61;
        }
      }

      &.auto {
        background: #409eff;
        color: white;

        &:hover {
          background: #66b1ff;
        }
      }

      &.pending {
        background: #e4e7ed;
        color: #909399;

        &:hover {
          background: #d3d4d6;
        }
      }
    }
  }

  .matrix-legend {
    margin-top: 15px;
    display: flex;
    gap: 15px;
    justify-content: center;

    .legend-item {
      display: flex;
      align-items: center;
      gap: 5px;

      .legend-color {
        width: 16px;
        height: 16px;
        border-radius: 3px;

        &.graded {
          background: #67c23a;
        }

        &.auto {
          background: #409eff;
        }

        &.pending {
          background: #e4e7ed;
        }
      }

      .legend-text {
        font-size: 12px;
        color: #606266;
      }
    }
  }

  .score-summary {
    .summary-content {
      .summary-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 12px;

        .summary-label {
          font-size: 13px;
          color: #606266;
        }

        .summary-value {
          font-size: 18px;
          font-weight: bold;

          &.objective {
            color: #409eff;
          }

          &.subjective {
            color: #e6a23c;
          }
        }

        .summary-max {
          font-size: 14px;
          color: #909399;
          margin-left: 5px;
        }

        &.total {
          padding-top: 12px;
          border-top: 2px solid #e4e7ed;
          margin-top: 5px;

          .summary-label {
            font-size: 15px;
            font-weight: bold;
          }

          .summary-value {
            font-size: 24px;
            color: #67c23a;
          }
        }
      }
    }
  }

  .student-switch {
    .switch-info {
      display: flex;
      justify-content: space-between;
      align-items: center;

      .current-student {
        font-size: 13px;
        color: #909399;
      }

      .switch-name {
        font-size: 14px;
        color: #303133;
        font-weight: bold;
      }
    }
  }
}
</style>
