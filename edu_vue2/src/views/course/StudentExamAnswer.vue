<template>
  <div class="student-exam-answer">
    <!-- 页面头部 (固定) -->
    <div class="page-header">
      <div class="header-left">
        <el-button icon="el-icon-arrow-left" @click="goBack">返回课程</el-button>
        <div class="exam-info">
          <h1>{{ exam.name }}</h1>
          <div class="meta-info">
            <span class="info-item"><i class="el-icon-document"></i> 共{{ exam.questions.length }}题</span>
            <span class="divider">|</span>
            <span class="info-item"><i class="el-icon-edit"></i> 总分{{ exam.totalScore }}分</span>
            <span class="divider">|</span>
            <span class="info-item"><i class="el-icon-time"></i> 时长{{ exam.duration }}分钟</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 主体内容 (固定容器) -->
    <div class="exam-container">
      <!-- 左侧：答题区 -->
      <main class="questions-area">
        <!-- 单题作答模式 -->
        <div v-if="viewMode === 'single' && currentQuestion" class="question-content">
          <div class="question-header">
            <span class="question-number">第 {{ currentQuestionIndex + 1 }} 题</span>
            <span class="question-type">{{ getQuestionTypeName(currentQuestion.type) }}</span>
            <span class="question-score">({{ currentQuestion.score }}分)</span>
          </div>

          <div class="question-text">{{ currentQuestion.text }}</div>

          <!-- 选择题选项 -->
          <div v-if="currentQuestion.type === 'single-choice'" class="options-area">
            <el-radio-group v-model="answers[currentQuestionIndex]">
              <el-radio
                v-for="(option, idx) in currentQuestion.options"
                :key="idx"
                :label="option.value"
                class="option-item"
              >
                {{ option.label }}. {{ option.text }}
              </el-radio>
            </el-radio-group>
          </div>

          <div v-else-if="currentQuestion.type === 'multiple-choice'" class="options-area">
            <el-checkbox-group v-model="answers[currentQuestionIndex]">
              <el-checkbox
                v-for="(option, idx) in currentQuestion.options"
                :key="idx"
                :label="option.value"
                class="option-item"
              >
                {{ option.label }}. {{ option.text }}
              </el-checkbox>
            </el-checkbox-group>
          </div>

          <!-- 简答题 -->
          <div v-else-if="currentQuestion.type === 'essay'" class="answer-area">
            <el-input
              v-model="answers[currentQuestionIndex]"
              type="textarea"
              :rows="8"
              placeholder="请输入你的答案..."
            />
          </div>

          <!-- 导航按钮 -->
          <div class="question-navigation">
            <el-button
              :disabled="currentQuestionIndex === 0"
              @click="currentQuestionIndex--"
            >
              <i class="el-icon-arrow-left"></i> 上一题
            </el-button>
            <el-button
              :disabled="currentQuestionIndex === exam.questions.length - 1"
              @click="currentQuestionIndex++"
              type="primary"
            >
              下一题 <i class="el-icon-arrow-right"></i>
            </el-button>
          </div>
        </div>

        <!-- 整卷阅览模式 -->
        <div v-if="viewMode === 'all'" class="all-questions-view">
          <div 
            v-for="(question, index) in exam.questions" 
            :key="index"
            :id="'question-' + index"
            class="question-block"
          >
            <div class="question-header">
              <span class="question-number">第 {{ index + 1 }} 题</span>
              <span class="question-type">{{ getQuestionTypeName(question.type) }}</span>
              <span class="question-score">({{ question.score }}分)</span>
            </div>

            <div class="question-text">{{ question.text }}</div>

            <!-- 选择题选项 -->
            <div v-if="question.type === 'single-choice'" class="options-area">
              <el-radio-group v-model="answers[index]">
                <el-radio
                  v-for="(option, idx) in question.options"
                  :key="idx"
                  :label="option.value"
                  class="option-item"
                >
                  {{ option.label }}. {{ option.text }}
                </el-radio>
              </el-radio-group>
            </div>

            <div v-else-if="question.type === 'multiple-choice'" class="options-area">
              <el-checkbox-group v-model="answers[index]">
                <el-checkbox
                  v-for="(option, idx) in question.options"
                  :key="idx"
                  :label="option.value"
                  class="option-item"
                >
                  {{ option.label }}. {{ option.text }}
                </el-checkbox>
              </el-checkbox-group>
            </div>

            <!-- 简答题 -->
            <div v-else-if="question.type === 'essay'" class="answer-area">
              <el-input
                v-model="answers[index]"
                type="textarea"
                :rows="8"
                placeholder="请输入你的答案..."
              />
            </div>
          </div>
        </div>
      </main>

      <!-- 右侧：题目导航 -->
      <aside class="questions-nav">
        <div class="nav-header">
          <h3>答题卡</h3>
          <span class="progress">{{ answeredCount }}/{{ exam.questions.length }}</span>
        </div>

        <!-- 倒计时显示 -->
        <div class="timer-display" :class="{ warning: remainingMinutes < 10 }">
          <i class="el-icon-timer"></i>
          <span>剩余时间：{{ formatTime }}</span>
        </div>

        <!-- 视图切换 -->
        <div class="view-switcher">
          <button 
            :class="['view-btn', { active: viewMode === 'single' }]"
            @click="viewMode = 'single'"
          >
            单题作答
          </button>
          <button 
            :class="['view-btn', { active: viewMode === 'all' }]"
            @click="viewMode = 'all'"
          >
            整卷阅览
          </button>
        </div>

        <div class="questions-grid">
          <div
            v-for="(question, index) in exam.questions"
            :key="index"
            :class="['question-btn', { 
              active: currentQuestionIndex === index && viewMode === 'single',
              answered: answers[index] !== undefined && answers[index] !== '' && answers[index] !== null
            }]"
            @click="goToQuestion(index)"
          >
            {{ index + 1 }}
          </div>
        </div>

        <div class="legend">
          <div class="legend-item">
            <span class="dot answered"></span>
            <span>已答</span>
          </div>
          <div class="legend-item" v-if="viewMode === 'single'">
            <span class="dot active"></span>
            <span>当前</span>
          </div>
          <div class="legend-item">
            <span class="dot"></span>
            <span>未答</span>
          </div>
        </div>

        <div class="submit-section">
          <el-button type="primary" size="large" @click="submitExam" style="width: 100%">
            交卷
          </el-button>
        </div>
      </aside>
    </div>
  </div>
</template>

<script>
export default {
  name: 'StudentExamAnswer',
  data() {
    return {
      courseId: this.$route.params.courseId,
      examId: this.$route.params.examId,
      exam: {
        questions: []
      },
      answers: [],
      currentQuestionIndex: 0,
      remainingSeconds: 7200, // 120分钟
      timer: null,
      viewMode: 'single' // 'single' 或 'all'
    }
  },
  computed: {
    currentQuestion() {
      return this.exam.questions[this.currentQuestionIndex]
    },
    answeredCount() {
      return this.answers.filter(a => a !== undefined && a !== '' && a !== null).length
    },
    formatTime() {
      const hours = Math.floor(this.remainingSeconds / 3600)
      const minutes = Math.floor((this.remainingSeconds % 3600) / 60)
      const seconds = this.remainingSeconds % 60
      if (hours > 0) {
        return `${hours}:${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`
      }
      return `${minutes}:${String(seconds).padStart(2, '0')}`
    },
    remainingMinutes() {
      return Math.floor(this.remainingSeconds / 60)
    }
  },
  created() {
    this.loadExamData()
    this.startTimer()
  },
  mounted() {
    // 禁用全局滚动
    document.body.style.overflow = 'hidden'
  },
  beforeDestroy() {
    // 恢复全局滚动
    document.body.style.overflow = ''
    if (this.timer) {
      clearInterval(this.timer)
    }
  },
  methods: {
    goBack() {
      this.$confirm('确定要退出考试吗？退出后答题将不会保存', '提示', {
        confirmButtonText: '确定退出',
        cancelButtonText: '继续答题',
        type: 'warning'
      }).then(() => {
        // 判断是否有courseId，决定返回到哪里
        if (this.courseId && this.courseId !== '1') {
          // 从课程详情页进入，返回课程详情页
          this.$router.push({
            path: `/student/course/${this.courseId}`,
            query: { tab: 'exams' }
          })
        } else {
          // 从考试中心进入，返回考试中心
          this.$router.push('/exam-center')
        }
      }).catch(() => {})
    },

    loadExamData() {
      // TODO: 从API加载真实数据
      this.exam = {
        id: this.examId,
        name: 'HTML/CSS基础测试',
        duration: 120,
        totalScore: 100,
        questions: [
          {
            type: 'single-choice',
            text: 'HTML是什么的缩写？',
            score: 5,
            options: [
              { label: 'A', value: 'A', text: 'Hyper Text Markup Language' },
              { label: 'B', value: 'B', text: 'High Tech Modern Language' },
              { label: 'C', value: 'C', text: 'Home Tool Markup Language' },
              { label: 'D', value: 'D', text: 'Hyperlinks and Text Markup Language' }
            ]
          },
          {
            type: 'multiple-choice',
            text: '以下哪些是HTML5的新特性？（多选）',
            score: 10,
            options: [
              { label: 'A', value: 'A', text: 'Canvas元素' },
              { label: 'B', value: 'B', text: 'Video和Audio元素' },
              { label: 'C', value: 'C', text: 'Local Storage' },
              { label: 'D', value: 'D', text: 'Table元素' }
            ]
          },
          {
            type: 'essay',
            text: '请简述CSS盒模型的概念。',
            score: 15
          }
        ]
      }

      // 初始化答案数组
      this.answers = this.exam.questions.map(q => {
        if (q.type === 'multiple-choice') {
          return []
        }
        return ''
      })
    },

    startTimer() {
      this.timer = setInterval(() => {
        if (this.remainingSeconds > 0) {
          this.remainingSeconds--
        } else {
          this.autoSubmit()
        }
      }, 1000)
    },

    getQuestionTypeName(type) {
      const types = {
        'single-choice': '单选题',
        'multiple-choice': '多选题',
        'essay': '简答题'
      }
      return types[type] || '未知'
    },

    submitExam() {
      const unanswered = this.exam.questions.length - this.answeredCount
      let message = '确定要交卷吗？'
      if (unanswered > 0) {
        message = `还有${unanswered}题未作答，确定要交卷吗？`
      }

      this.$confirm(message, '提示', {
        confirmButtonText: '确定交卷',
        cancelButtonText: '继续答题',
        type: 'warning'
      }).then(() => {
        this.doSubmit()
      }).catch(() => {})
    },

    autoSubmit() {
      this.$alert('考试时间已到，系统将自动交卷', '提示', {
        confirmButtonText: '确定',
        type: 'warning'
      }).then(() => {
        this.doSubmit()
      })
    },

    doSubmit() {
      if (this.timer) {
        clearInterval(this.timer)
      }
      // TODO: 调用API提交答案
      this.$message.success('考试已提交')
      
      // 交卷后统一返回考试中心主页
      this.$router.push('/exam-center')
    },

    goToQuestion(index) {
      if (this.viewMode === 'single') {
        this.currentQuestionIndex = index
      } else {
        // 整卷模式下点击导航滚动到对应题目
        const element = document.getElementById('question-' + index)
        if (element) {
          const headerHeight = document.querySelector('.page-header').offsetHeight
          const containerTop = document.querySelector('.exam-container').offsetTop
          const offsetTop = element.offsetTop + containerTop - headerHeight - 20
          window.scrollTo({ top: offsetTop, behavior: 'smooth' })
        }
      }
    }
  }
}
</script>

<style scoped>
.student-exam-answer {
  width: 100%;
  height: 100vh;
  background: #f9fafb;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.page-header {
  background: white;
  padding: 1.25rem 2rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-shrink: 0;
  z-index: 100;
  min-height: 80px;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  flex: 1;
}

.exam-info {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.exam-info h1 {
  margin: 0;
  font-size: 1.3rem;
  color: #1f2937;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.meta-info {
  display: flex;
  align-items: center;
  gap: 1rem;
  font-size: 0.875rem;
  color: #6b7280;
}

.meta-info .info-item {
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.meta-info .divider {
  color: #d1d5db;
}

.exam-container {
  flex: 1;
  display: flex;
  gap: 1rem;
  padding: 1rem;
  min-height: 0;
  overflow: hidden;
}

/* 左侧答题区 */
.questions-area {
  flex: 1;
  background: white;
  border-radius: 8px;
  padding: 2rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  overflow-y: auto;
  height: 100%;
}

/* 整卷阅览模式 */
.all-questions-view {
  width: 100%;
}

.all-questions-view::-webkit-scrollbar {
  width: 8px;
}

.all-questions-view::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 4px;
}

.all-questions-view::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 4px;
}

.all-questions-view::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}

.question-block {
  margin-bottom: 2rem;
  padding: 1.5rem;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  transition: all 0.2s;
  scroll-margin-top: 1rem;
}

.question-block:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.question-block:last-child {
  margin-bottom: 0;
}

/* 右侧导航 */
.questions-nav {
  width: 300px;
  flex-shrink: 0;
  background: white;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  display: flex;
  flex-direction: column;
  height: 100%;
  overflow: hidden;
}

.nav-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.75rem;
  padding-bottom: 0.75rem;
  border-bottom: 2px solid #667eea;
}

.nav-header h3 {
  margin: 0;
  font-size: 1rem;
  color: #1f2937;
}

.progress {
  color: #667eea;
  font-weight: 600;
}

/* 倒计时显示（在答题卡中） */
.questions-nav .timer-display {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.375rem;
  padding: 0.5rem 0.75rem;
  background: #f0fdf4;
  border: 2px solid #86efac;
  border-radius: 6px;
  font-weight: 600;
  color: #166534;
  font-size: 0.875rem;
  margin-bottom: 0.75rem;
}

.questions-nav .timer-display.warning {
  background: #fef3c7;
  border-color: #fbbf24;
  color: #92400e;
}

/* 视图切换（在答题卡中） */
.questions-nav .view-switcher {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 0.75rem;
}

.questions-nav .view-btn {
  flex: 1;
  padding: 0.4rem 0.5rem;
  border: 1px solid #d1d5db;
  background: white;
  color: #6b7280;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s;
  font-size: 0.8125rem;
  font-weight: 500;
  text-align: center;
}

.questions-nav .view-btn:hover {
  border-color: #667eea;
  color: #667eea;
}

.questions-nav .view-btn.active {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-color: #667eea;
}

.questions-grid {
  flex: 1;
  overflow-y: auto;
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 0.4rem;
  margin-bottom: 0.75rem;
  padding-right: 0.5rem;
  align-content: start;
  max-height: 280px;
}

.question-btn {
  aspect-ratio: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f3f4f6;
  border: 2px solid transparent;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s;
  font-weight: 600;
  color: #6b7280;
  font-size: 0.875rem;
}

.question-btn:hover {
  background: #e5e7eb;
}

.question-btn.answered {
  background: #d1fae5;
  color: #065f46;
  border-color: #10b981;
}

.question-btn.active {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-color: #667eea;
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
}

.legend {
  display: flex;
  flex-direction: column;
  gap: 0.375rem;
  padding: 0.625rem 0.75rem;
  background: #f9fafb;
  border-radius: 6px;
  margin-bottom: 0.75rem;
  flex-shrink: 0;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 0.375rem;
  font-size: 0.8125rem;
  color: #6b7280;
}

.dot {
  width: 14px;
  height: 14px;
  border-radius: 3px;
  background: #f3f4f6;
  border: 2px solid #d1d5db;
}

.dot.answered {
  background: #d1fae5;
  border-color: #10b981;
}

.dot.active {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-color: #667eea;
}

.question-content {
  width: 100%;
}

.question-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #e5e7eb;
}

.question-number {
  font-size: 1.25rem;
  font-weight: 700;
  color: #1f2937;
}

.question-type {
  padding: 0.25rem 0.75rem;
  background: #f3f4f6;
  border-radius: 4px;
  font-size: 0.875rem;
  color: #6b7280;
}

.question-score {
  color: #667eea;
  font-weight: 600;
}

.question-text {
  font-size: 1.125rem;
  color: #1f2937;
  line-height: 1.8;
  margin-bottom: 2rem;
}

.options-area {
  margin-bottom: 2rem;
}

.option-item {
  display: block;
  padding: 1rem;
  margin-bottom: 0.75rem;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  transition: all 0.2s;
}

.option-item:hover {
  border-color: #667eea;
  background: #f9fafb;
}

.answer-area {
  margin-bottom: 2rem;
}

.question-navigation {
  display: flex;
  justify-content: space-between;
  padding-top: 2rem;
  border-top: 1px solid #e5e7eb;
}

.submit-section {
  flex-shrink: 0;
}
</style>
