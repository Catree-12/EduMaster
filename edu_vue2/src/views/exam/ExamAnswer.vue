<template>
  <div class="exam-answer">
    <!-- 顶部信息栏 -->
    <div class="exam-header">
      <div class="exam-info">
        <h2>{{ exam.name }}</h2>
        <p>{{ exam.description }}</p>
      </div>
      <div class="exam-timer">
        <div class="timer">
          <span class="label">剩余时间</span>
          <span class="time" :class="{ warning: remainingTime < 300 }">
            {{ formatTime(remainingTime) }}
          </span>
        </div>
        <button @click="showSubmitConfirm = true" class="submit-btn">
          提交答卷
        </button>
      </div>
    </div>

    <div class="exam-container">
      <!-- 左侧：题目导航 -->
      <aside class="questions-nav">
        <div class="nav-header">
          <h3>题目导航</h3>
          <span class="progress">{{ answeredCount }}/{{ questions.length }}</span>
        </div>

        <div class="questions-list">
          <div 
            v-for="(q, idx) in questions"
            :key="q.id"
            :class="[
              'question-item',
              { active: currentQuestionIdx === idx },
              { answered: answers[q.id] !== undefined },
              { marked: markedQuestions.includes(q.id) }
            ]"
            @click="currentQuestionIdx = idx"
          >
            <span class="q-number">{{ idx + 1 }}</span>
            <span class="q-type">{{ q.type === 'choice' ? '选' : q.type === 'fill' ? '填' : '简' }}</span>
            <button 
              v-if="markedQuestions.includes(q.id)"
              @click.stop="toggleMark(q.id)" 
              class="mark-btn marked"
              title="取消标记"
            >
              🚩
            </button>
            <button 
              v-else
              @click.stop="toggleMark(q.id)" 
              class="mark-btn"
              title="标记题目"
            >
              📌
            </button>
          </div>
        </div>

        <div class="legend">
          <div class="legend-item">
            <span class="dot answered"></span>
            <span>已答题</span>
          </div>
          <div class="legend-item">
            <span class="dot marked"></span>
            <span>已标记</span>
          </div>
          <div class="legend-item">
            <span class="dot unanswered"></span>
            <span>未答题</span>
          </div>
        </div>
      </aside>

      <!-- 中间：答题区 -->
      <main class="questions-area">
        <div v-if="currentQuestion" class="question-content">
          <!-- 题目信息 -->
          <div class="question-header">
            <h3>第 {{ currentQuestionIdx + 1 }} 题 ({{ questionPoints }}分)</h3>
            <button 
              v-if="!markedQuestions.includes(currentQuestion.id)"
              @click="toggleMark(currentQuestion.id)"
              class="mark-question-btn"
            >
              📌 标记
            </button>
            <button 
              v-else
              @click="toggleMark(currentQuestion.id)"
              class="mark-question-btn marked"
            >
              🚩 已标记
            </button>
          </div>

          <!-- 题目内容 -->
          <div class="question-body">
            <p class="question-text">{{ currentQuestion.content }}</p>

            <!-- 单选题 -->
            <div v-if="currentQuestion.type === 'choice'" class="options">
              <label 
                v-for="option in currentQuestion.options"
                :key="option.id"
                class="option"
              >
                <input 
                  type="radio"
                  :name="`q${currentQuestion.id}`"
                  :value="option.id"
                  v-model="answers[currentQuestion.id]"
                >
                <span class="option-text">{{ option.text }}</span>
              </label>
            </div>

            <!-- 填空题 -->
            <div v-else-if="currentQuestion.type === 'fill'" class="fill-input">
              <textarea 
                v-model="answers[currentQuestion.id]"
                placeholder="请输入你的答案"
                rows="4"
              ></textarea>
            </div>

            <!-- 简答题 -->
            <div v-else-if="currentQuestion.type === 'essay'" class="essay-input">
              <textarea 
                v-model="answers[currentQuestion.id]"
                placeholder="请输入你的答案（不少于50字）"
                rows="6"
              ></textarea>
              <p class="char-count">
                {{ (answers[currentQuestion.id] || '').length }} 字
              </p>
            </div>
          </div>

          <!-- 导航按钮 -->
          <div class="question-nav">
            <button 
              v-if="currentQuestionIdx > 0"
              @click="currentQuestionIdx--"
              class="nav-btn prev-btn"
            >
              ← 上一题
            </button>
            <button 
              v-if="currentQuestionIdx < questions.length - 1"
              @click="currentQuestionIdx++"
              class="nav-btn next-btn"
            >
              下一题 →
            </button>
          </div>
        </div>
      </main>

      <!-- 右侧：统计信息 -->
      <aside class="exam-stats">
        <div class="stats-card">
          <h4>答题统计</h4>
          <div class="stat-item">
            <span class="label">总题数</span>
            <span class="value">{{ questions.length }}</span>
          </div>
          <div class="stat-item">
            <span class="label">已答题</span>
            <span class="value answered">{{ answeredCount }}</span>
          </div>
          <div class="stat-item">
            <span class="label">未答题</span>
            <span class="value unanswered">{{ questions.length - answeredCount }}</span>
          </div>
          <div class="stat-item">
            <span class="label">已标记</span>
            <span class="value marked">{{ markedQuestions.length }}</span>
          </div>
        </div>

        <div class="stats-card">
          <h4>题型分布</h4>
          <div class="stat-item">
            <span class="label">选择题</span>
            <span class="value">{{ questions.filter(q => q.type === 'choice').length }}</span>
          </div>
          <div class="stat-item">
            <span class="label">填空题</span>
            <span class="value">{{ questions.filter(q => q.type === 'fill').length }}</span>
          </div>
          <div class="stat-item">
            <span class="label">简答题</span>
            <span class="value">{{ questions.filter(q => q.type === 'essay').length }}</span>
          </div>
        </div>

        <button @click="autoSaveAnswers" class="save-btn">
          💾 保存草稿
        </button>
      </aside>
    </div>

    <!-- 提交确认模态框 -->
    <div v-if="showSubmitConfirm" class="modal-overlay" @click="showSubmitConfirm = false">
      <div class="modal-content" @click.stop>
        <h2>确认提交答卷？</h2>
        <div class="submit-info">
          <p>已答题：<strong>{{ answeredCount }}</strong> / {{ questions.length }}</p>
          <p v-if="questions.length - answeredCount > 0" class="warning-text">
            ⚠️ 还有 <strong>{{ questions.length - answeredCount }}</strong> 道题目未答，提交后将无法修改
          </p>
        </div>
        <div class="modal-actions">
          <button @click="submitExam" class="confirm-btn" :disabled="submitting">
            {{ submitting ? '提交中...' : '确认提交' }}
          </button>
          <button @click="showSubmitConfirm = false" class="cancel-btn">
            取消
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ExamAnswer',
  data() {
    return {
      examId: this.$route.params.id,
      exam: {
        id: 1,
        name: '期末考试',
        description: '本次考试共50题，总分100分，时间限制120分钟',
        duration: 120,
        totalPoints: 100
      },
      questions: [
        {
          id: 1,
          type: 'choice',
          content: 'Vue.js中，以下哪个不是生命周期钩子？',
          points: 2,
          options: [
            { id: 'a', text: 'mounted' },
            { id: 'b', text: 'updated' },
            { id: 'c', text: 'destroyed' },
            { id: 'd', text: 'initialized' }
          ]
        },
        {
          id: 2,
          type: 'fill',
          content: '在Vue中，用___________指令可以绑定HTML属性',
          points: 2
        },
        {
          id: 3,
          type: 'essay',
          content: '简述Vue的数据绑定原理',
          points: 10
        },
        // ... 更多题目
      ],
      answers: {},
      currentQuestionIdx: 0,
      markedQuestions: [],
      remainingTime: 7200, // 120分钟 = 7200秒
      showSubmitConfirm: false,
      submitting: false,
      timerInterval: null
    }
  },
  computed: {
    currentQuestion() {
      return this.questions[this.currentQuestionIdx]
    },
    questionPoints() {
      return this.currentQuestion ? this.currentQuestion.points : 0
    },
    answeredCount() {
      return Object.keys(this.answers).filter(key => {
        const ans = this.answers[key]
        return ans !== undefined && ans !== null && ans !== ''
      }).length
    }
  },
  mounted() {
    this.startTimer()
    this.loadSavedAnswers()
  },
  beforeDestroy() {
    this.stopTimer()
    this.autoSaveAnswers()
  },
  methods: {
    formatTime(seconds) {
      const hours = Math.floor(seconds / 3600)
      const minutes = Math.floor((seconds % 3600) / 60)
      const secs = seconds % 60
      return `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}:${String(secs).padStart(2, '0')}`
    },
    startTimer() {
      this.timerInterval = setInterval(() => {
        this.remainingTime--
        if (this.remainingTime <= 0) {
          this.stopTimer()
          this.submitExam()
        }
      }, 1000)
    },
    stopTimer() {
      if (this.timerInterval) {
        clearInterval(this.timerInterval)
        this.timerInterval = null
      }
    },
    toggleMark(questionId) {
      const idx = this.markedQuestions.indexOf(questionId)
      if (idx > -1) {
        this.markedQuestions.splice(idx, 1)
      } else {
        this.markedQuestions.push(questionId)
      }
    },
    autoSaveAnswers() {
      const data = {
        answers: this.answers,
        markedQuestions: this.markedQuestions,
        timestamp: Date.now()
      }
      localStorage.setItem(`exam_${this.examId}_draft`, JSON.stringify(data))
      this.$message.success('已保存草稿')
    },
    loadSavedAnswers() {
      const saved = localStorage.getItem(`exam_${this.examId}_draft`)
      if (saved) {
        const data = JSON.parse(saved)
        this.answers = data.answers
        this.markedQuestions = data.markedQuestions
      }
    },
    async submitExam() {
      this.submitting = true
      try {
        // TODO: 调用提交答卷API
        // const response = await this.$api.post(`/exam/${this.examId}/submit`, {
        //   answers: this.answers
        // })
        
        this.$message.success('答卷已提交！')
        localStorage.removeItem(`exam_${this.examId}_draft`)
        this.showSubmitConfirm = false
        this.stopTimer()
        
        // 跳转到成绩查询页面
        this.$router.push(`/exam/${this.examId}/result`)
      } catch (error) {
        this.$message.error('提交失败：' + error.message)
      } finally {
        this.submitting = false
      }
    }
  }
}
</script>

<style scoped>
.exam-answer {
  width: 100%;
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: #f5f5f5;
}

.exam-header {
  background: white;
  padding: 1.5rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.exam-info h2 {
  margin: 0 0 0.5rem 0;
  color: #2c3e50;
  font-size: 1.3rem;
}

.exam-info p {
  margin: 0;
  color: #7f8c8d;
  font-size: 0.9rem;
}

.exam-timer {
  display: flex;
  align-items: center;
  gap: 2rem;
}

.timer {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.timer .label {
  color: #7f8c8d;
  font-size: 0.9rem;
  display: block;
  margin-bottom: 0.25rem;
}

.timer .time {
  font-size: 1.5rem;
  font-weight: 700;
  color: #667eea;
  font-family: 'Courier New', monospace;
}

.timer .time.warning {
  color: #e74c3c;
  animation: blink 1s infinite;
}

@keyframes blink {
  0%, 50% { opacity: 1; }
  51%, 100% { opacity: 0.7; }
}

.submit-btn {
  padding: 0.75rem 1.5rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 600;
  transition: opacity 0.3s;
}

.submit-btn:hover {
  opacity: 0.9;
}

.exam-container {
  display: grid;
  grid-template-columns: 200px 1fr 250px;
  gap: 1rem;
  padding: 1rem;
  flex: 1;
  overflow: hidden;
}

.questions-nav {
  background: white;
  border-radius: 8px;
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  overflow-y: auto;
}

.nav-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid #ecf0f1;
}

.nav-header h3 {
  margin: 0;
  color: #2c3e50;
  font-size: 0.95rem;
}

.progress {
  background: #667eea;
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: 600;
}

.questions-list {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 0.5rem;
  margin-bottom: 1rem;
  flex: 1;
  align-content: start;
}

.question-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.25rem;
  padding: 0.5rem;
  background: #f8f9fa;
  border: 2px solid #ecf0f1;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s;
  position: relative;
  font-size: 0.75rem;
}

.question-item:hover {
  border-color: #667eea;
  background: #f0f0ff;
}

.question-item.active {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-color: transparent;
}

.question-item.answered {
  background: #d5f4e6;
  border-color: #27ae60;
}

.question-item.marked::after {
  content: '🚩';
  position: absolute;
  top: -8px;
  right: -8px;
  font-size: 0.9rem;
}

.q-number {
  font-weight: 700;
}

.q-type {
  color: #95a5a6;
  font-size: 0.7rem;
}

.mark-btn {
  display: none;
  background: none;
  border: none;
  cursor: pointer;
  font-size: 0.8rem;
  padding: 0;
}

.question-item:hover .mark-btn {
  display: block;
}

.mark-btn.marked {
  display: block;
}

.legend {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
  font-size: 0.75rem;
  color: #7f8c8d;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 0.4rem;
}

.dot {
  width: 12px;
  height: 12px;
  border-radius: 2px;
}

.dot.answered {
  background: #d5f4e6;
  border: 1px solid #27ae60;
}

.dot.marked {
  background: #fef5e7;
  border: 1px solid #f39c12;
}

.dot.unanswered {
  background: #f8f9fa;
  border: 1px solid #bdc3c7;
}

.questions-area {
  background: white;
  border-radius: 8px;
  padding: 2rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  overflow-y: auto;
}

.question-content {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.question-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid #ecf0f1;
}

.question-header h3 {
  margin: 0;
  color: #2c3e50;
  font-size: 1rem;
  font-weight: 600;
}

.mark-question-btn {
  padding: 0.5rem 1rem;
  background: #ecf0f1;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s;
  font-weight: 500;
  font-size: 0.85rem;
}

.mark-question-btn.marked {
  background: #fef5e7;
  color: #f39c12;
}

.question-body {
  flex: 1;
  margin-bottom: 1.5rem;
}

.question-text {
  font-size: 1rem;
  line-height: 1.6;
  margin-bottom: 1.5rem;
  color: #2c3e50;
}

.options {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.option {
  display: flex;
  align-items: center;
  padding: 0.75rem;
  background: #f8f9fa;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s;
}

.option:hover {
  background: #e8f0ff;
}

.option input {
  margin-right: 0.75rem;
  cursor: pointer;
}

.option-text {
  flex: 1;
}

.fill-input,
.essay-input {
  position: relative;
}

.fill-input textarea,
.essay-input textarea {
  width: 100%;
  padding: 1rem;
  border: 1px solid #bdc3c7;
  border-radius: 4px;
  font-family: inherit;
  font-size: 0.95rem;
  resize: vertical;
}

.fill-input textarea:focus,
.essay-input textarea:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.char-count {
  text-align: right;
  color: #95a5a6;
  font-size: 0.85rem;
  margin-top: 0.5rem;
}

.question-nav {
  display: flex;
  gap: 1rem;
  justify-content: space-between;
}

.nav-btn {
  padding: 0.75rem 1.5rem;
  background: #ecf0f1;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s;
  flex: 1;
}

.nav-btn:hover {
  background: #d5dbdb;
  transform: translateY(-2px);
}

.exam-stats {
  background: white;
  border-radius: 8px;
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  overflow-y: auto;
}

.stats-card {
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 6px;
}

.stats-card h4 {
  margin: 0 0 1rem 0;
  color: #2c3e50;
  font-size: 0.9rem;
}

.stat-item {
  display: flex;
  justify-content: space-between;
  padding: 0.5rem 0;
  font-size: 0.85rem;
  color: #7f8c8d;
}

.stat-item .value {
  font-weight: 700;
  color: #667eea;
}

.stat-item .value.answered {
  color: #27ae60;
}

.stat-item .value.unanswered {
  color: #e74c3c;
}

.stat-item .value.marked {
  color: #f39c12;
}

.save-btn {
  padding: 0.75rem;
  background: #27ae60;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 600;
  transition: opacity 0.3s;
}

.save-btn:hover {
  opacity: 0.9;
}

/* 模态框 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  max-width: 450px;
  width: 90%;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
}

.modal-content h2 {
  margin: 0 0 1.5rem 0;
  color: #2c3e50;
  font-size: 1.2rem;
}

.submit-info {
  margin-bottom: 1.5rem;
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 4px;
}

.submit-info p {
  margin: 0.5rem 0;
  color: #7f8c8d;
  font-size: 0.9rem;
}

.submit-info strong {
  color: #2c3e50;
  font-weight: 600;
}

.warning-text {
  color: #e74c3c !important;
}

.modal-actions {
  display: flex;
  gap: 1rem;
}

.confirm-btn {
  flex: 1;
  padding: 0.75rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 600;
  transition: opacity 0.3s;
}

.confirm-btn:hover:not(:disabled) {
  opacity: 0.9;
}

.confirm-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.cancel-btn {
  flex: 1;
  padding: 0.75rem;
  background: #ecf0f1;
  color: #2c3e50;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 600;
}

.cancel-btn:hover {
  background: #d5dbdb;
}

@media (max-width: 1200px) {
  .exam-container {
    grid-template-columns: 150px 1fr;
  }

  .exam-stats {
    display: none;
  }
}

@media (max-width: 768px) {
  .exam-header {
    flex-direction: column;
    gap: 1rem;
  }

  .exam-container {
    grid-template-columns: 1fr;
  }

  .questions-nav {
    max-height: 200px;
  }

  .questions-list {
    grid-template-columns: repeat(5, 1fr);
  }
}
</style>
