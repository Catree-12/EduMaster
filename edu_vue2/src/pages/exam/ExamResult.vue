<template>
  <div class="exam-result">
    <!-- 顶部固定：成绩信息栏 -->
    <div class="result-header">
      <div class="header-left">
        <button @click="goBack" class="btn-back">
          <i class="el-icon-back"></i>
          返回考试列表
        </button>
        <div class="exam-info">
          <h1>考试成绩</h1>
          <div class="score-display">
            <span class="score">{{ result.score }}</span>
            <span class="total">/{{ result.totalPoints }}</span>
            <span :class="['status-tag', scoreLevel]">{{ scoreText }}</span>
          </div>
        </div>
      </div>
      <div class="header-stats">
        <div class="stat-item">
          <span class="label">答对</span>
          <span class="value correct">{{ result.correctCount }}</span>
        </div>
        <div class="stat-item">
          <span class="label">答错</span>
          <span class="value wrong">{{ result.wrongCount }}</span>
        </div>
        <div class="stat-item">
          <span class="label">用时</span>
          <span class="value">{{ result.timeUsed }}分钟</span>
        </div>
      </div>
    </div>

    <!-- 主体内容区 -->
    <div class="result-container">
      <!-- 左侧：题目详情（可滚动） -->
      <main class="questions-area">
        <div class="questions-list">
          <div 
            v-for="(question, index) in filteredQuestions"
            :key="question.id"
            :id="'question-' + index"
            :class="['question-item', { correct: question.isCorrect, wrong: !question.isCorrect }]"
          >
            <div class="question-header">
              <div class="q-number">
                <span class="number">第 {{ index + 1 }} 题</span>
                <span :class="['type-badge', question.type]">
                  {{ getTypeText(question.type) }}
                </span>
                <span class="points">{{ question.points }} 分</span>
              </div>
              <div :class="['result-badge', { correct: question.isCorrect }]">
                <i :class="question.isCorrect ? 'el-icon-circle-check' : 'el-icon-circle-close'"></i>
                {{ question.isCorrect ? '正确' : '错误' }}
              </div>
            </div>

            <div class="question-content">
              <div class="q-title">{{ question.title }}</div>

              <!-- 选择题 -->
              <div v-if="question.type === 'choice'" class="options">
                <div 
                  v-for="option in question.options"
                  :key="option.key"
                  :class="[
                    'option-item',
                    { 
                      correct: question.correctAnswer.includes(option.key),
                      wrong: question.userAnswer.includes(option.key) && !question.correctAnswer.includes(option.key),
                      selected: question.userAnswer.includes(option.key)
                    }
                  ]"
                >
                  <span class="option-key">{{ option.key }}</span>
                  <span class="option-text">{{ option.text }}</span>
                  <span v-if="question.correctAnswer.includes(option.key)" class="correct-tag">
                    <i class="el-icon-circle-check"></i> 正确答案
                  </span>
                </div>
              </div>

              <!-- 填空题 -->
              <div v-if="question.type === 'fill'" class="answer-display">
                <div class="answer-item">
                  <span class="label">你的答案：</span>
                  <span :class="['answer', { wrong: !question.isCorrect }]">
                    {{ question.userAnswer || '未作答' }}
                  </span>
                </div>
                <div v-if="!question.isCorrect" class="answer-item">
                  <span class="label">正确答案：</span>
                  <span class="answer correct">{{ question.correctAnswer }}</span>
                </div>
              </div>

              <!-- 简答题 -->
              <div v-if="question.type === 'essay'" class="answer-display">
                <div class="answer-item">
                  <span class="label">你的答案：</span>
                  <div class="essay-answer">{{ question.userAnswer || '未作答' }}</div>
                </div>
                <div class="answer-item">
                  <span class="label">参考答案：</span>
                  <div class="essay-answer reference">{{ question.referenceAnswer }}</div>
                </div>
                <div v-if="question.teacherComment" class="teacher-comment">
                  <i class="el-icon-chat-line-square"></i>
                  <span class="label">教师点评：</span>
                  <p>{{ question.teacherComment }}</p>
                </div>
              </div>

              <!-- 解析 -->
              <div v-if="question.analysis" class="analysis">
                <div class="analysis-header">
                  <i class="el-icon-reading"></i>
                  <span>答案解析</span>
                </div>
                <div class="analysis-content">{{ question.analysis }}</div>
              </div>
            </div>
          </div>
        </div>
      </main>

      <!-- 右侧：答题卡导航（固定） -->
      <aside class="answer-card">
        <div class="card-header">
          <h3>答题卡</h3>
          <div class="filter-buttons">
            <button 
              :class="{ active: filterType === 'all' }"
              @click="filterType = 'all'"
              class="filter-btn"
            >
              全部
            </button>
            <button 
              :class="{ active: filterType === 'correct' }"
              @click="filterType = 'correct'"
              class="filter-btn correct"
            >
              答对
            </button>
            <button 
              :class="{ active: filterType === 'wrong' }"
              @click="filterType = 'wrong'"
              class="filter-btn wrong"
            >
              答错
            </button>
          </div>
        </div>

        <div class="questions-grid">
          <div
            v-for="(question, index) in questions"
            :key="question.id"
            :class="[
              'question-number',
              { 
                correct: question.isCorrect,
                wrong: !question.isCorrect,
                hidden: !shouldShowQuestion(question)
              }
            ]"
            @click="goToQuestion(index)"
          >
            {{ index + 1 }}
          </div>
        </div>

        <div class="legend">
          <div class="legend-item">
            <span class="dot correct"></span>
            <span>答对</span>
          </div>
          <div class="legend-item">
            <span class="dot wrong"></span>
            <span>答错</span>
          </div>
        </div>
      </aside>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ExamResult',
  data() {
    return {
      filterType: 'all',
      result: {
        score: 85,
        totalPoints: 100,
        totalQuestions: 10,
        correctCount: 8,
        wrongCount: 2,
        timeUsed: 25
      },
      questions: [
        {
          id: 1,
          type: 'choice',
          title: 'Vue.js 是什么？',
          points: 10,
          options: [
            { key: 'A', text: '一个渐进式JavaScript框架' },
            { key: 'B', text: '一个后端框架' },
            { key: 'C', text: '一个数据库' },
            { key: 'D', text: '一个编程语言' }
          ],
          userAnswer: ['A'],
          correctAnswer: ['A'],
          isCorrect: true,
          analysis: 'Vue.js 是一个用于构建用户界面的渐进式JavaScript框架，它专注于视图层，易于上手。'
        },
        {
          id: 2,
          type: 'choice',
          title: 'Vue中的数据绑定指令是？（多选）',
          points: 10,
          options: [
            { key: 'A', text: 'v-model' },
            { key: 'B', text: 'v-bind' },
            { key: 'C', text: 'v-show' },
            { key: 'D', text: 'v-for' }
          ],
          userAnswer: ['A', 'B'],
          correctAnswer: ['A', 'B'],
          isCorrect: true,
          analysis: 'v-model用于双向数据绑定，v-bind用于单向数据绑定。'
        },
        {
          id: 3,
          type: 'fill',
          title: 'Vue的生命周期钩子函数中，在组件挂载后调用的是______',
          points: 10,
          userAnswer: 'mounted',
          correctAnswer: 'mounted',
          isCorrect: true,
          analysis: 'mounted是在组件挂载到DOM后调用的生命周期钩子。'
        },
        {
          id: 4,
          type: 'fill',
          title: 'Vue中用于监听数据变化的选项是______',
          points: 10,
          userAnswer: 'watcher',
          correctAnswer: 'watch',
          isCorrect: false,
          analysis: '正确答案是watch，用于观察和响应Vue实例上的数据变化。'
        },
        {
          id: 5,
          type: 'essay',
          title: '请简述Vue组件间通信的几种方式。',
          points: 20,
          userAnswer: '1. props和$emit\n2. $parent和$children\n3. provide和inject\n4. Vuex状态管理',
          referenceAnswer: '主要有以下几种方式：\n1. props/$emit：父子组件通信\n2. $parent/$children：父子组件直接访问\n3. provide/inject：跨层级组件通信\n4. EventBus：兄弟组件通信\n5. Vuex：全局状态管理\n6. $attrs/$listeners：多层级组件通信',
          isCorrect: true,
          teacherComment: '回答较为全面，涵盖了主要的通信方式。如果能补充EventBus和$attrs/$listeners会更完整。',
          analysis: 'Vue组件间通信是Vue开发中的重要概念，不同场景应选择合适的通信方式。'
        }
      ]
    }
  },
  computed: {
    percentage() {
      return Math.round((this.result.score / this.result.totalPoints) * 100)
    },
    scoreLevel() {
      const p = this.percentage
      if (p >= 90) return 'excellent'
      if (p >= 80) return 'good'
      if (p >= 60) return 'pass'
      return 'fail'
    },
    scoreText() {
      const p = this.percentage
      if (p >= 90) return '优秀'
      if (p >= 80) return '良好'
      if (p >= 60) return '及格'
      return '不及格'
    },
    filteredQuestions() {
      if (this.filterType === 'all') {
        return this.questions
      } else if (this.filterType === 'correct') {
        return this.questions.filter(q => q.isCorrect)
      } else {
        return this.questions.filter(q => !q.isCorrect)
      }
    }
  },
  mounted() {
    const examId = this.$route.params.id
    // 实际应用中应该根据 examId 从 API 获取考试结果
    console.log('获取考试结果:', examId)
    
    // 禁用body滚动
    document.body.style.overflow = 'hidden'
  },
  beforeDestroy() {
    // 恢复body滚动
    document.body.style.overflow = ''
  },
  methods: {
    goBack() {
      this.$router.push('/exam-center')
    },
    getTypeText(type) {
      const typeMap = {
        choice: '选择题',
        fill: '填空题',
        essay: '简答题'
      }
      return typeMap[type] || type
    },
    shouldShowQuestion(question) {
      if (this.filterType === 'all') return true
      if (this.filterType === 'correct') return question.isCorrect
      if (this.filterType === 'wrong') return !question.isCorrect
      return true
    },
    goToQuestion(index) {
      const element = document.getElementById('question-' + index)
      if (element) {
        const questionsArea = document.querySelector('.questions-area')
        if (questionsArea) {
          const headerHeight = 80 // 顶部header高度
          const elementTop = element.offsetTop - headerHeight - 20
          questionsArea.scrollTo({
            top: elementTop,
            behavior: 'smooth'
          })
        }
      }
    }
  }
}
</script>

<style scoped>
/* ========== 布局结构 ========== */
.exam-result {
  height: 100vh;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  background: #f5f7fa;
}

/* 顶部固定区域 */
.result-header {
  flex-shrink: 0;
  background: white;
  border-bottom: 1px solid #e8ecf1;
  padding: 1.5rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  z-index: 10;
  min-height: 110px;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.btn-back {
  padding: 0.5rem 1rem;
  background: white;
  border: 2px solid #e8ecf1;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.9rem;
  color: #6c757d;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.3s;
}

.btn-back:hover {
  border-color: #667eea;
  color: #667eea;
}

.exam-info h1 {
  margin: 0 0 0.5rem 0;
  font-size: 1.25rem;
  color: #2c3e50;
  font-weight: 600;
}

.score-display {
  display: flex;
  align-items: baseline;
  gap: 0.5rem;
}

.score-display .score {
  font-size: 2rem;
  font-weight: 700;
  color: #667eea;
}

.score-display .total {
  font-size: 1.25rem;
  color: #7f8c8d;
}

.status-tag {
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.85rem;
  font-weight: 600;
  margin-left: 0.5rem;
}

.status-tag.excellent {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  color: white;
}

.status-tag.good {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
  color: white;
}

.status-tag.pass {
  background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
  color: white;
}

.status-tag.fail {
  background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
  color: white;
}

.header-stats {
  display: flex;
  gap: 2rem;
}

.header-stats .stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.header-stats .label {
  font-size: 0.85rem;
  color: #7f8c8d;
  margin-bottom: 0.25rem;
}

.header-stats .value {
  font-size: 1.25rem;
  font-weight: 700;
  color: #2c3e50;
}

.header-stats .value.correct {
  color: #27ae60;
}

.header-stats .value.wrong {
  color: #e74c3c;
}

/* 主体内容区 */
.result-container {
  flex: 1;
  min-height: 0;
  display: flex;
  overflow: hidden;
}

/* 左侧题目区域（可滚动） */
.questions-area {
  flex: 1;
  height: 100%;
  overflow-y: auto;
  overflow-x: hidden;
  padding: 2rem;
  background: #f5f7fa;
}

.questions-list {
  max-width: 900px;
  margin: 0 auto;
}

.question-item {
  background: white;
  border-radius: 12px;
  padding: 1.25rem;
  margin-bottom: 1.25rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  border-left: 4px solid #e8ecf1;
  transition: all 0.3s;
}

.question-item.correct {
  border-left-color: #27ae60;
}

.question-item.wrong {
  border-left-color: #e74c3c;
}

.question-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  padding-bottom: 0.75rem;
  border-bottom: 1px solid #e8ecf1;
}

.q-number {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.q-number .number {
  font-weight: 700;
  color: #2c3e50;
  font-size: 1rem;
}

.type-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 600;
}

.type-badge.choice {
  background: #e3f2fd;
  color: #1976d2;
}

.type-badge.fill {
  background: #f3e5f5;
  color: #7b1fa2;
}

.type-badge.essay {
  background: #e8f5e9;
  color: #388e3c;
}

.q-number .points {
  color: #667eea;
  font-weight: 600;
  font-size: 0.9rem;
}

.result-badge {
  padding: 0.375rem 1rem;
  border-radius: 20px;
  font-weight: 600;
  display: inline-flex;
  align-items: center;
  gap: 0.375rem;
  background: #ffe5e5;
  color: #e74c3c;
  font-size: 0.85rem;
}

.result-badge.correct {
  background: #d5f4e6;
  color: #27ae60;
}

.question-content {
  margin-top: 1rem;
}

.q-title {
  font-size: 1rem;
  color: #2c3e50;
  margin-bottom: 1rem;
  line-height: 1.6;
  font-weight: 500;
}

.options {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  margin-bottom: 1rem;
}

.option-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.875rem 1rem;
  background: #f8f9fa;
  border-radius: 8px;
  border: 2px solid transparent;
  transition: all 0.3s;
}

.option-item.correct {
  background: #d5f4e6;
  border-color: #27ae60;
}

.option-item.wrong {
  background: #ffe5e5;
  border-color: #e74c3c;
}

.option-item.selected:not(.correct):not(.wrong) {
  border-color: #667eea;
}

.option-key {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  background: white;
  border-radius: 50%;
  font-weight: 700;
  color: #2c3e50;
  flex-shrink: 0;
}

.option-text {
  flex: 1;
  color: #2c3e50;
  line-height: 1.5;
}

.correct-tag {
  color: #27ae60;
  font-size: 0.85rem;
  font-weight: 600;
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
}

.answer-display {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-bottom: 1rem;
}

.answer-item {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
}

.answer-item .label {
  font-weight: 600;
  color: #5a6c7d;
  white-space: nowrap;
  padding-top: 0.75rem;
}

.answer-item .answer {
  flex: 1;
  padding: 0.75rem 1rem;
  background: #f8f9fa;
  border-radius: 8px;
  color: #2c3e50;
}

.answer-item .answer.correct {
  background: #d5f4e6;
  color: #27ae60;
  font-weight: 600;
}

.answer-item .answer.wrong {
  background: #ffe5e5;
  color: #e74c3c;
}

.essay-answer {
  flex: 1;
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 8px;
  color: #2c3e50;
  line-height: 1.8;
  white-space: pre-wrap;
}

.essay-answer.reference {
  background: #e8f4f8;
  color: #1976d2;
}

.teacher-comment {
  padding: 1rem;
  background: #fff3e0;
  border-radius: 8px;
  border-left: 4px solid #ff9800;
  display: flex;
  align-items: flex-start;
  gap: 0.5rem;
}

.teacher-comment i {
  color: #ff9800;
  font-size: 1.2rem;
  margin-top: 0.25rem;
}

.teacher-comment .label {
  font-weight: 600;
  color: #e65100;
  white-space: nowrap;
}

.teacher-comment p {
  margin: 0;
  color: #5d4037;
  line-height: 1.6;
}

.analysis {
  margin-top: 1rem;
  padding: 1rem;
  background: #f3e5f5;
  border-radius: 8px;
  border-left: 4px solid #9c27b0;
}

.analysis-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.75rem;
  color: #7b1fa2;
  font-weight: 600;
}

.analysis-header i {
  font-size: 1.1rem;
}

.analysis-content {
  color: #4a148c;
  line-height: 1.6;
}

/* 右侧答题卡（固定） */
.answer-card {
  width: 300px;
  flex-shrink: 0;
  background: white;
  border-left: 1px solid #e8ecf1;
  display: flex;
  flex-direction: column;
  height: 100%;
  overflow: hidden;
}

.card-header {
  padding: 1.25rem 1.25rem 1rem;
  border-bottom: 1px solid #e8ecf1;
  flex-shrink: 0;
}

.card-header h3 {
  margin: 0 0 1rem 0;
  font-size: 1.1rem;
  color: #2c3e50;
}

.filter-buttons {
  display: flex;
  gap: 0.5rem;
}

.filter-btn {
  flex: 1;
  padding: 0.5rem;
  border: 2px solid #e8ecf1;
  background: white;
  color: #6c757d;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
  font-size: 0.8rem;
  transition: all 0.3s;
}

.filter-btn:hover {
  border-color: #667eea;
}

.filter-btn.active {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-color: transparent;
}

.filter-btn.correct.active {
  background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
}

.filter-btn.wrong.active {
  background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
}

.questions-grid {
  flex: 1;
  overflow-y: auto;
  padding: 0.875rem;
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 0.625rem;
  align-content: start;
}

.question-number {
  aspect-ratio: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  font-size: 0.9rem;
}

.question-number.correct {
  background: #d5f4e6;
  color: #27ae60;
  border: 2px solid #27ae60;
}

.question-number.wrong {
  background: #ffe5e5;
  color: #e74c3c;
  border: 2px solid #e74c3c;
}

.question-number.hidden {
  display: none;
}

.question-number:hover {
  transform: scale(1.1);
}

.legend {
  padding: 0.875rem 1.25rem;
  border-top: 1px solid #e8ecf1;
  display: flex;
  flex-direction: column;
  gap: 0.625rem;
  flex-shrink: 0;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.legend .dot {
  width: 20px;
  height: 20px;
  border-radius: 4px;
  flex-shrink: 0;
}

.legend .dot.correct {
  background: #d5f4e6;
  border: 2px solid #27ae60;
}

.legend .dot.wrong {
  background: #ffe5e5;
  border: 2px solid #e74c3c;
}

.legend-item span:last-child {
  color: #5a6c7d;
  font-size: 0.9rem;
}

/* 响应式 */
@media (max-width: 768px) {
  .result-container {
    flex-direction: column;
  }

  .answer-card {
    width: 100%;
    max-height: 40vh;
  }

  .questions-area {
    height: auto;
  }
}
</style>
