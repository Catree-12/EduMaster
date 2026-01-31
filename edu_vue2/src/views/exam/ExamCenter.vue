<template>
  <div class="exam-center">
    <div class="page-header">
      <div class="header-content">
        <h1>
          <i class="el-icon-arrow-left back-icon" @click="goBack"></i>
          📝 考试中心
        </h1>
        <p>参加课程考试，检验学习成果</p>
      </div>
      <div class="header-decoration">
        <div class="decoration-circle circle-1"></div>
        <div class="decoration-circle circle-2"></div>
        <div class="decoration-circle circle-3"></div>
      </div>
    </div>

    <div class="filter-section">
      <div class="search-box">
        <i class="el-icon-search"></i>
        <input v-model="searchQuery" type="text" placeholder="搜索考试名称或课程...">
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
        <div class="card-decoration"></div>
        <div class="exam-header">
          <h3>{{ exam.name }}</h3>
          <span :class="['status-badge', exam.status]">
            <i :class="getStatusIcon(exam.status)"></i>
            {{ exam.status }}
          </span>
        </div>
        
        <p class="exam-course">
          <i class="el-icon-notebook-2"></i>
          {{ exam.courseName }}
        </p>
        <p class="exam-description">{{ exam.description }}</p>
        
        <div class="exam-info">
          <div class="info-item">
            <i class="el-icon-time"></i>
            <span>{{ exam.duration }}分钟</span>
          </div>
          <div class="info-item">
            <i class="el-icon-edit"></i>
            <span>{{ exam.questionCount }}题</span>
          </div>
          <div class="info-item">
            <i class="el-icon-star-off"></i>
            <span>{{ exam.totalPoints }}分</span>
          </div>
        </div>

        <div v-if="exam.status === '已完成'" class="exam-score">
          <div class="score-label">考试得分</div>
          <div class="score-value">
            <strong>{{ exam.score }}</strong>
            <span>/{{ exam.totalPoints }}</span>
          </div>
          <div class="score-percentage">{{ Math.round((exam.score / exam.totalPoints) * 100) }}%</div>
        </div>

        <button 
          v-if="exam.status === '未开始'"
          @click="startExam(exam.id)"
          class="exam-btn start-btn"
        >
          <i class="el-icon-video-play"></i>
          开始考试
        </button>
        <button 
          v-else-if="exam.status === '进行中'"
          @click="continueExam(exam.id)"
          class="exam-btn continue-btn"
        >
          <i class="el-icon-refresh-right"></i>
          继续考试
        </button>
        <button 
          v-else
          @click="viewResult(exam.id)"
          class="exam-btn result-btn"
        >
          <i class="el-icon-document-checked"></i>
          查看成绩
        </button>
      </div>
    </div>

    <div v-else class="no-content">
      <i class="el-icon-folder-opened"></i>
      <p>暂无符合条件的考试</p>
      <span class="hint">试试调整筛选条件</span>
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
    goBack() {
      this.$router.push('/course/my-courses')
    },
    getStatusIcon(status) {
      const icons = {
        '未开始': 'el-icon-clock',
        '进行中': 'el-icon-loading',
        '已完成': 'el-icon-circle-check'
      }
      return icons[status] || 'el-icon-info'
    },
    startExam(examId) {
      // 未开始的考试，跳转到确认页（与课程详情页流程一致）
      this.$router.push(`/student/course/1/exam/${examId}`)
    },
    continueExam(examId) {
      // 进行中的考试，直接进入答题页（与课程详情页流程一致）
      this.$router.push(`/student/course/1/exam/${examId}/answer`)
    },
    viewResult(examId) {
      // 已完成的考试，查看成绩和题目
      this.$router.push(`/exam/${examId}/result`)
    }
  }
}
</script>

<style scoped>
.exam-center {
  width: 100%;
  padding: 2rem;
  background: linear-gradient(135deg, #f5f7fa 0%, #e8ecf1 100%);
  min-height: calc(100vh - 64px);
}

.page-header {
  margin-bottom: 1rem;
  position: relative;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 12px;
  padding: 0.5rem 1.5rem;
  color: white;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.2);
}

.header-content {
  position: relative;
  z-index: 2;
  display: flex;
  flex-direction: column; /* 让标题和文字上下堆叠 */
  align-items: center;    /* 水平居中 */
  text-align: center;     /* 确保多行文本本身也居中 */
  justify-content: center; /* 如果父容器有高度，垂直也居中 */
}

.page-header h1 {
  margin: 0 0 0.25rem 0;
  font-size: 1.25rem;
  font-weight: 700;
  display: flex;
  align-items: center;
  gap: 0.375rem;
}

.back-icon {
  cursor: pointer;
  font-size: 1.1rem;
  padding: 0.25rem;
  border-radius: 4px;
  transition: all 0.3s;
}

.back-icon:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: translateX(-2px);
}

.page-header p {
  margin: 0;
  font-size: 0.85rem;
  opacity: 0.9;
}

.header-decoration {
  position: absolute;
  top: 0;
  right: 0;
  width: 120px;
  height: 100%;
  z-index: 1;
}

.decoration-circle {
  position: absolute;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.1);
}

.circle-1 {
  width: 50px;
  height: 50px;
  top: -15px;
  right: 15px;
}

.circle-2 {
  width: 35px;
  height: 35px;
  top: 20px;
  right: 60px;
}

.circle-3 {
  width: 25px;
  height: 25px;
  bottom: 10px;
  right: 25px;
}

.filter-section {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
  align-items: center;
  background: white;
  padding: 0.875rem 1rem;
  border-radius: 10px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
}

.search-box {
  flex: 1;
  min-width: 280px;
  position: relative;
}

.search-box i {
  position: absolute;
  left: 0.75rem;
  top: 50%;
  transform: translateY(-50%);
  color: #7f8c8d;
  font-size: 0.95rem;
}

.search-box input {
  width: 100%;
  padding: 0.625rem 0.875rem 0.625rem 2.5rem;
  border: 2px solid #e8ecf1;
  border-radius: 6px;
  font-size: 0.85rem;
  transition: all 0.3s;
}

.search-box input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.1);
}

.filter-tabs {
  display: flex;
  gap: 0.75rem;
  flex-wrap: wrap;
}

.filter-btn {
  padding: 0.5rem 1rem;
  background-color: #f8f9fa;
  border: 2px solid transparent;
  color: #6c757d;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s;
  font-weight: 600;
  font-size: 0.85rem;
}

.filter-btn.active {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

.filter-btn:hover:not(.active) {
  background-color: #e9ecef;
  border-color: #dee2e6;
}

.exams-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
  gap: 1.75rem;
}

.exam-card {
  background: white;
  border-radius: 12px;
  padding: 1.75rem;
  transition: all 0.3s;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  position: relative;
  overflow: hidden;
}

.card-decoration {
  position: absolute;
  top: 0;
  right: 0;
  width: 80px;
  height: 80px;
  background: linear-gradient(135deg, #667eea20 0%, #764ba220 100%);
  border-radius: 0 0 0 100%;
}

.exam-card:hover {
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.12);
  transform: translateY(-6px);
}

.exam-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1rem;
  gap: 1rem;
  position: relative;
  z-index: 2;
}

.exam-header h3 {
  margin: 0;
  color: #2c3e50;
  font-size: 1.2rem;
  font-weight: 700;
  flex: 1;
  line-height: 1.4;
}

.status-badge {
  padding: 0.375rem 0.875rem;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 700;
  white-space: nowrap;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  gap: 0.375rem;
}

.status-badge i {
  font-size: 0.9rem;
}

.status-badge.未开始 {
  background: linear-gradient(135deg, #e8ecf1 0%, #dfe3e8 100%);
  color: #6c757d;
}

.status-badge.进行中 {
  background: linear-gradient(135deg, #fff3cd 0%, #ffe69c 100%);
  color: #856404;
}

.status-badge.已完成 {
  background: linear-gradient(135deg, #d1f2eb 0%, #a3e4d7 100%);
  color: #0f5132;
}

.exam-course {
  color: #667eea;
  font-size: 0.95rem;
  margin: 0 0 0.75rem 0;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.exam-course i {
  font-size: 1.1rem;
}

.exam-description {
  color: #6c757d;
  font-size: 0.9rem;
  margin: 0 0 1.25rem 0;
  line-height: 1.6;
}

.exam-info {
  display: flex;
  gap: 1.25rem;
  margin-bottom: 1.25rem;
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 8px;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.9rem;
  color: #495057;
  font-weight: 500;
}

.info-item i {
  color: #667eea;
  font-size: 1.1rem;
}

.exam-score {
  margin-bottom: 1.25rem;
  padding: 1rem;
  background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
  border-radius: 8px;
  text-align: center;
}

.score-label {
  color: #2e7d32;
  font-size: 0.85rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
}

.score-value {
  display: flex;
  align-items: baseline;
  justify-content: center;
  gap: 0.25rem;
  margin-bottom: 0.25rem;
}

.score-value strong {
  color: #1b5e20;
  font-size: 2rem;
  font-weight: 700;
}

.score-value span {
  color: #2e7d32;
  font-size: 1.1rem;
}

.score-percentage {
  color: #388e3c;
  font-weight: 600;
  font-size: 0.9rem;
}

.exam-btn {
  width: 100%;
  padding: 0.875rem;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 700;
  transition: all 0.3s;
  font-size: 0.95rem;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.exam-btn i {
  font-size: 1.1rem;
}

.start-btn {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

.start-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(102, 126, 234, 0.4);
}

.continue-btn {
  background: linear-gradient(135deg, #f39c12 0%, #e67e22 100%);
  color: white;
  box-shadow: 0 4px 12px rgba(243, 156, 18, 0.3);
}

.continue-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(243, 156, 18, 0.4);
}

.result-btn {
  background: linear-gradient(135deg, #3498db 0%, #2980b9 100%);
  color: white;
  box-shadow: 0 4px 12px rgba(52, 152, 219, 0.3);
}

.result-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(52, 152, 219, 0.4);
}

.no-content {
  text-align: center;
  padding: 4rem 2rem;
  color: #6c757d;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.no-content i {
  font-size: 4rem;
  color: #dee2e6;
  margin-bottom: 1rem;
}

.no-content p {
  margin: 0 0 0.5rem 0;
  font-size: 1.1rem;
  font-weight: 600;
}

.no-content .hint {
  font-size: 0.9rem;
  color: #adb5bd;
}

@media (max-width: 768px) {
  .exam-center {
    padding: 1rem;
  }

  .page-header {
    padding: 1.75rem;
  }

  .page-header h1 {
    font-size: 1.75rem;
  }

  .filter-section {
    flex-direction: column;
    padding: 1rem;
  }

  .search-box {
    min-width: auto;
  }

  .exams-grid {
    grid-template-columns: 1fr;
  }

  .exam-info {
    flex-direction: column;
    gap: 0.75rem;
  }
}
</style>
