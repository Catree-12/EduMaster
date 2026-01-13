<template>
  <div class="exam-center">
    <div class="page-header">
      <h1>考试中心</h1>
      <p>参加课程考试，检验学习成果</p>
    </div>

    <div class="filter-section">
      <div class="search-box">
        <input v-model="searchQuery" type="text" placeholder="搜索考试...">
      </div>
      <div class="filter-tabs">
        <button 
          v-for="status in ['全部', '未开始', '进行中', '已完成']"
          :key="status"
          :class="{ active: activeStatus === status }"
          @click="activeStatus = status"
          class="filter-btn"
        >
          {{ status }}
        </button>
      </div>
    </div>

    <div v-if="filteredExams.length > 0" class="exams-grid">
      <div v-for="exam in filteredExams" :key="exam.id" class="exam-card">
        <div class="exam-header">
          <h3>{{ exam.name }}</h3>
          <span :class="['status-badge', exam.status]">{{ exam.status }}</span>
        </div>
        
        <p class="exam-course">📚 {{ exam.courseName }}</p>
        <p class="exam-description">{{ exam.description }}</p>
        
        <div class="exam-info">
          <span>⏱️ {{ exam.duration }}分钟</span>
          <span>📝 {{ exam.questionCount }}题</span>
          <span>⭐ {{ exam.totalPoints }}分</span>
        </div>

        <div v-if="exam.status === '已完成'" class="exam-score">
          得分: <strong>{{ exam.score }}/{{ exam.totalPoints }}</strong>
        </div>

        <button 
          v-if="exam.status === '未开始'"
          @click="startExam(exam.id)"
          class="exam-btn start-btn"
        >
          开始考试
        </button>
        <button 
          v-else-if="exam.status === '进行中'"
          @click="continueExam(exam.id)"
          class="exam-btn continue-btn"
        >
          继续考试
        </button>
        <button 
          v-else
          @click="viewResult(exam.id)"
          class="exam-btn result-btn"
        >
          查看成绩
        </button>
      </div>
    </div>

    <div v-else class="no-content">
      <p>暂无考试</p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ExamCenter',
  data() {
    return {
      searchQuery: '',
      activeStatus: '全部',
      exams: [
        {
          id: 1,
          name: '第一章测验',
          courseName: 'Vue.js 从入门到精通',
          description: '考查第一章基础知识点',
          duration: 30,
          questionCount: 10,
          totalPoints: 100,
          status: '已完成',
          score: 85
        },
        {
          id: 2,
          name: '第二章测验',
          courseName: 'Vue.js 从入门到精通',
          description: '考查第二章核心概念',
          duration: 45,
          questionCount: 15,
          totalPoints: 100,
          status: '未开始'
        },
        {
          id: 3,
          name: '期末考试',
          courseName: 'Vue.js 从入门到精通',
          description: '综合考查全部知识点',
          duration: 120,
          questionCount: 50,
          totalPoints: 100,
          status: '进行中'
        }
      ]
    }
  },
  computed: {
    filteredExams() {
      return this.exams.filter(exam => {
        const matchSearch = exam.name.includes(this.searchQuery) || exam.courseName.includes(this.searchQuery)
        const matchStatus = this.activeStatus === '全部' || exam.status === this.activeStatus
        return matchSearch && matchStatus
      })
    }
  },
  methods: {
    startExam(examId) {
      this.$router.push(`/exam/${examId}/answer`)
    },
    continueExam(examId) {
      this.$router.push(`/exam/${examId}/answer`)
    },
    viewResult(examId) {
      this.$router.push(`/exam/${examId}/result`)
    }
  }
}
</script>

<style scoped>
.exam-center {
  width: 100%;
}

.page-header {
  margin-bottom: 2rem;
}

.page-header h1 {
  color: #2c3e50;
  margin: 0 0 0.5rem 0;
  font-size: 1.75rem;
  font-weight: 700;
}

.page-header p {
  color: #95a5a6;
  margin: 0;
}

.filter-section {
  display: flex;
  gap: 1.5rem;
  margin-bottom: 2rem;
  flex-wrap: wrap;
  align-items: center;
}

.search-box {
  flex: 1;
  min-width: 250px;
}

.search-box input {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 1px solid #bdc3c7;
  border-radius: 4px;
  font-size: 0.9rem;
}

.search-box input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.filter-tabs {
  display: flex;
  gap: 0.75rem;
  flex-wrap: wrap;
}

.filter-btn {
  padding: 0.5rem 1.5rem;
  background-color: #ecf0f1;
  border: 1px solid #bdc3c7;
  color: #7f8c8d;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s;
  font-weight: 500;
}

.filter-btn.active {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-color: transparent;
}

.filter-btn:hover {
  transform: translateY(-2px);
}

.exams-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 1.5rem;
}

.exam-card {
  background: white;
  border: 1px solid #ecf0f1;
  border-radius: 8px;
  padding: 1.5rem;
  transition: all 0.3s;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.exam-card:hover {
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
  transform: translateY(-4px);
}

.exam-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1rem;
  gap: 1rem;
}

.exam-header h3 {
  margin: 0;
  color: #2c3e50;
  font-size: 1.1rem;
  flex: 1;
}

.status-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 600;
  white-space: nowrap;
  flex-shrink: 0;
}

.status-badge.未开始 {
  background-color: #ecf0f1;
  color: #7f8c8d;
}

.status-badge.进行中 {
  background-color: #fef5e7;
  color: #f39c12;
}

.status-badge.已完成 {
  background-color: #d5f4e6;
  color: #27ae60;
}

.exam-course {
  color: #7f8c8d;
  font-size: 0.9rem;
  margin: 0 0 0.5rem 0;
}

.exam-description {
  color: #7f8c8d;
  font-size: 0.85rem;
  margin: 0 0 1rem 0;
  line-height: 1.5;
}

.exam-info {
  display: flex;
  gap: 1rem;
  font-size: 0.9rem;
  color: #7f8c8d;
  margin-bottom: 1rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #ecf0f1;
}

.exam-score {
  color: #667eea;
  font-weight: 500;
  margin-bottom: 1rem;
  font-size: 0.95rem;
}

.exam-score strong {
  color: #27ae60;
  font-size: 1.1rem;
}

.exam-btn {
  width: 100%;
  padding: 0.65rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s;
  font-size: 0.9rem;
}

.start-btn {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.start-btn:hover {
  opacity: 0.9;
  transform: translateY(-2px);
}

.continue-btn {
  background-color: #f39c12;
  color: white;
}

.continue-btn:hover {
  background-color: #e67e22;
  transform: translateY(-2px);
}

.result-btn {
  background-color: #3498db;
  color: white;
}

.result-btn:hover {
  background-color: #2980b9;
  transform: translateY(-2px);
}

.no-content {
  text-align: center;
  padding: 3rem 2rem;
  color: #7f8c8d;
  background: white;
  border-radius: 8px;
  border: 1px solid #ecf0f1;
}

@media (max-width: 768px) {
  .filter-section {
    flex-direction: column;
  }

  .search-box {
    min-width: auto;
  }

  .exams-grid {
    grid-template-columns: 1fr;
  }
}
</style>
