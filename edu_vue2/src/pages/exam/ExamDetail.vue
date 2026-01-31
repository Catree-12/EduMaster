<template>
  <div class="exam-detail">
    <div class="detail-container">
      <!-- 考试信息卡片 -->
      <div class="exam-info-card">
        <div class="card-header">
          <h1>{{ exam.name }}</h1>
          <span class="course-tag">
            <i class="el-icon-notebook-2"></i>
            {{ exam.courseName }}
          </span>
        </div>

        <div class="exam-description">
          <p>{{ exam.description }}</p>
        </div>

        <div class="exam-meta">
          <div class="meta-item">
            <i class="el-icon-time"></i>
            <span class="label">考试时长</span>
            <span class="value">{{ exam.duration }} 分钟</span>
          </div>
          <div class="meta-item">
            <i class="el-icon-edit"></i>
            <span class="label">题目数量</span>
            <span class="value">{{ exam.questionCount }} 题</span>
          </div>
          <div class="meta-item">
            <i class="el-icon-star-off"></i>
            <span class="label">总分</span>
            <span class="value">{{ exam.totalPoints }} 分</span>
          </div>
          <div class="meta-item">
            <i class="el-icon-date"></i>
            <span class="label">开始时间</span>
            <span class="value">{{ exam.startTime || '不限' }}</span>
          </div>
          <div class="meta-item">
            <i class="el-icon-date"></i>
            <span class="label">结束时间</span>
            <span class="value">{{ exam.endTime || '不限' }}</span>
          </div>
          <div class="meta-item">
            <i class="el-icon-refresh"></i>
            <span class="label">考试次数</span>
            <span class="value">{{ exam.attemptCount || '不限' }}</span>
          </div>
        </div>
      </div>

      <!-- 考试须知 -->
      <div class="exam-rules">
        <h3>
          <i class="el-icon-warning"></i>
          考试须知
        </h3>
        <ul>
          <li>请确保网络连接稳定，避免考试过程中断网</li>
          <li>考试过程中不允许切换浏览器标签页或窗口</li>
          <li>考试时间结束后将自动提交答卷</li>
          <li>请在规定时间内完成考试，超时将无法继续作答</li>
          <li>考试过程中可以标记题目，方便后续检查</li>
          <li>提交后无法修改答案，请仔细检查后再提交</li>
        </ul>
      </div>

      <!-- 题型说明 -->
      <div class="question-types">
        <h3>
          <i class="el-icon-document"></i>
          题型说明
        </h3>
        <div class="type-list">
          <div v-if="exam.questionTypes.choice" class="type-item">
            <div class="type-header">
              <span class="type-badge choice">选择题</span>
              <span class="count">{{ exam.questionTypes.choice.count }} 题</span>
              <span class="points">共 {{ exam.questionTypes.choice.points }} 分</span>
            </div>
            <p>单项或多项选择题，请选择正确答案</p>
          </div>
          <div v-if="exam.questionTypes.fill" class="type-item">
            <div class="type-header">
              <span class="type-badge fill">填空题</span>
              <span class="count">{{ exam.questionTypes.fill.count }} 题</span>
              <span class="points">共 {{ exam.questionTypes.fill.points }} 分</span>
            </div>
            <p>根据题目要求填写答案</p>
          </div>
          <div v-if="exam.questionTypes.essay" class="type-item">
            <div class="type-header">
              <span class="type-badge essay">简答题</span>
              <span class="count">{{ exam.questionTypes.essay.count }} 题</span>
              <span class="points">共 {{ exam.questionTypes.essay.points }} 分</span>
            </div>
            <p>用简洁的语言回答问题</p>
          </div>
        </div>
      </div>

      <!-- 操作按钮 -->
      <div class="action-buttons">
        <button @click="goBack" class="btn-cancel">
          <i class="el-icon-back"></i>
          返回
        </button>
        <button @click="startExam" class="btn-start">
          <i class="el-icon-video-play"></i>
          开始考试
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ExamDetail',
  data() {
    return {
      exam: {
        id: 1,
        name: '第一章测验',
        courseName: 'Vue.js 从入门到精通',
        description: '本次考试将全面考查第一章的基础知识点，包括Vue基础概念、模板语法、数据绑定等内容。',
        duration: 30,
        questionCount: 10,
        totalPoints: 100,
        startTime: '2024-01-15 09:00',
        endTime: '2024-01-20 23:59',
        attemptCount: 1,
        questionTypes: {
          choice: {
            count: 5,
            points: 50
          },
          fill: {
            count: 3,
            points: 30
          },
          essay: {
            count: 2,
            points: 20
          }
        }
      }
    }
  },
  mounted() {
    const examId = this.$route.params.id
    // 实际应用中应该根据 examId 从 API 获取考试详情
    console.log('获取考试详情:', examId)
  },
  methods: {
    goBack() {
      this.$router.back()
    },
    startExam() {
      // 直接进入答题页面，不需要确认弹窗
      this.$router.push(`/exam/${this.exam.id}/answer`)
    }
  }
}
</script>

<style scoped>
.exam-detail {
  min-height: calc(100vh - 64px);
  background: linear-gradient(135deg, #f5f7fa 0%, #e8ecf1 100%);
  padding: 2rem;
}

.detail-container {
  max-width: 1000px;
  margin: 0 auto;
}

.exam-info-card {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  margin-bottom: 1.5rem;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1.5rem;
  gap: 1rem;
}

.card-header h1 {
  margin: 0;
  font-size: 1.75rem;
  color: #2c3e50;
  font-weight: 700;
}

.course-tag {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-size: 0.9rem;
  white-space: nowrap;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
}

.exam-description {
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 8px;
  margin-bottom: 1.5rem;
}

.exam-description p {
  margin: 0;
  color: #5a6c7d;
  line-height: 1.6;
}

.exam-meta {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem;
  background: #f8f9fa;
  border-radius: 8px;
}

.meta-item i {
  font-size: 1.2rem;
  color: #667eea;
}

.meta-item .label {
  color: #7f8c8d;
  font-size: 0.9rem;
}

.meta-item .value {
  color: #2c3e50;
  font-weight: 600;
  margin-left: auto;
}

.exam-rules,
.question-types {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  margin-bottom: 1.5rem;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
}

.exam-rules h3,
.question-types h3 {
  margin: 0 0 1rem 0;
  color: #2c3e50;
  font-size: 1.25rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.exam-rules h3 i {
  color: #f39c12;
}

.question-types h3 i {
  color: #667eea;
}

.exam-rules ul {
  margin: 0;
  padding-left: 1.5rem;
}

.exam-rules li {
  margin-bottom: 0.75rem;
  color: #5a6c7d;
  line-height: 1.6;
}

.type-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.type-item {
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 8px;
  border-left: 4px solid #667eea;
}

.type-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 0.5rem;
}

.type-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 600;
}

.type-badge.choice {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.type-badge.fill {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  color: white;
}

.type-badge.essay {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
  color: white;
}

.type-header .count {
  color: #5a6c7d;
  font-size: 0.9rem;
}

.type-header .points {
  color: #667eea;
  font-weight: 600;
  margin-left: auto;
}

.type-item p {
  margin: 0;
  color: #7f8c8d;
  font-size: 0.9rem;
}

.action-buttons {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
}

.btn-cancel,
.btn-start {
  padding: 0.875rem 2rem;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
}

.btn-cancel {
  background: white;
  color: #6c757d;
  border: 2px solid #e8ecf1;
}

.btn-cancel:hover {
  background: #f8f9fa;
  border-color: #667eea;
  color: #667eea;
}

.btn-start {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

.btn-start:hover {
  box-shadow: 0 6px 16px rgba(102, 126, 234, 0.4);
  transform: translateY(-2px);
}

@media (max-width: 768px) {
  .exam-detail {
    padding: 1rem;
  }

  .exam-meta {
    grid-template-columns: 1fr;
  }

  .action-buttons {
    flex-direction: column;
  }

  .btn-cancel,
  .btn-start {
    width: 100%;
    justify-content: center;
  }
}
</style>
