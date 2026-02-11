<template>
  <div class="exam-center">
    <div class="page-header">
      <button class="back-btn" @click="goBack">
        <i class="el-icon-arrow-left"></i>
        返回
      </button>
      
      <div class="header-content">
        <h1>📝 考试中心</h1>
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
        <div class="exam-header">
          <h3>{{ exam.name }}</h3>
          <span :class="['status-badge', exam.status]">
            <i :class="getStatusIcon(exam.status)"></i>
            {{ exam.status }}
          </span>
        </div>
        
        <p class="exam-course">📚 {{ exam.courseName }}</p>
        <p class="exam-description">{{ exam.description }}</p>
        
        <div class="exam-info">
          <span><i class="el-icon-time"></i> {{ exam.duration }}分钟</span>
          <span><i class="el-icon-edit"></i> {{ exam.questionCount }}题</span>
          <span><i class="el-icon-star-off"></i> {{ exam.totalPoints }}分</span>
        </div>

        <div v-if="exam.status === '已完成'" class="exam-score">
          考试得分: <strong>{{ exam.score }}/{{ exam.totalPoints }}</strong>
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
      <p>暂无符合条件的考试</p>
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
      this.$router.push('/courses/mycourses')
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
      // 修正：根据你的路由表，确认页路径应包含 courseId
      // 这里假设 courseId 为 1，实际开发中应从 exam 对象中获取
      // 路径：/student/courses/:courseId/exams/:examId
      this.$router.push(`/student/courses/1/exams/${examId}`);
    },

      continueExam(examId) {
        // 修正：进行中的考试直接进入答题页
        // 路径：/student/courses/:courseId/exams/:examId/answer
        this.$router.push(`/student/courses/1/exams/${examId}/answer`);
      },

      viewResult(examId) {
        // 修正：查看成绩
        // 注意：你之前的路由表中似乎没有专门的 /result 路径
        // 如果你想复用 ExamDetail 组件来显示成绩，路径如下：
        this.$router.push(`/student/courses/1/exams/${examId}/answer`);
        
        // 或者如果你想跳到“考试中心”的详情（如果有配置的话）：
        // this.$router.push(`/exams/${examId}/answer`);
    }
  }
}
</script>

<style scoped>
/* --- 页面整体容器 --- */
.exam-center, .homework-center {
  width: 100%;
  min-height: calc(100vh - 64px);
  display: flex;
  flex-direction: column;
  padding: 2rem;
  background: #f5f7fa;
  box-sizing: border-box;
}

/* --- Header 头部区域样式 --- */
.page-header {
  margin-bottom: 1rem;
  position: relative;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 12px;
  padding: 0.3rem 1rem;
  color: white;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.2);
  flex-shrink: 0;
}

/* 统一的返回按钮：绝对定位确保标题完美居中 */
.back-btn {
  position: absolute;
  left: 1.5rem;
  top: 50%;
  transform: translateY(-50%);
  background: rgba(255, 255, 255, 0.2);
  border: none;
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.9rem;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 0.375rem;
  transition: all 0.3s;
  z-index: 10;
}

.back-btn:hover {
  background: rgba(255, 255, 255, 0.3);
  transform: translateY(-50%) translateX(-2px);
}

.header-content {
  position: relative;
  z-index: 2;
  text-align: center;
}

.header-content h1 {
  margin: 0 0 0.5rem 0;
  font-size: 1.5rem;
  font-weight: 700;
}

.header-content p {
  margin: 0;
  font-size: 0.9rem;
  opacity: 0.9;
}

/* 背景修饰圆圈 */
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
.circle-1 { width: 50px; height: 50px; top: -15px; right: 15px; }
.circle-2 { width: 35px; height: 35px; top: 20px; right: 60px; }
.circle-3 { width: 25px; height: 25px; bottom: 10px; right: 25px; }

/* --- 筛选与搜索区域 (修复后的精装版) --- */
.filter-section {
  display: flex;
  gap: 1.5rem;
  margin-bottom: 2rem;
  align-items: center;
  background: white;
  padding: 1rem 1.5rem;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.search-box {
  flex: 1;
  position: relative;
  display: flex;
  align-items: center;
}

.search-box i {
  position: absolute;
  left: 1rem;
  color: #a0aec0;
  font-size: 1rem;
  z-index: 1;
}

.search-box input {
  width: 100%;
  padding: 0.75rem 1rem 0.75rem 2.8rem;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-size: 0.9rem;
  transition: all 0.3s;
  outline: none;
  background-color: #f8fafc;
}

.search-box input:focus {
  background-color: #fff;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.filter-tabs {
  display: flex;
  gap: 0.5rem;
}

.filter-btn {
  padding: 0.6rem 1.2rem;
  background-color: transparent;
  border: none;
  color: #718096;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
  font-weight: 600;
  font-size: 0.85rem;
}

.filter-btn.active {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

.filter-btn:hover:not(.active) {
  background-color: #edf2f7;
  color: #4a5568;
}

/* --- 卡片布局与样式 --- */
.exams-grid, .homeworks-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 1.5rem;
}

.exam-card, .homework-card {
  background: white;
  border: 1px solid #e8ecf1;
  border-radius: 12px;
  padding: 1.5rem;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
  position: relative;
  overflow: hidden;
}

/* 卡片顶部的彩色修饰线条 */
.exam-card::before, .homework-card::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0; height: 4px;
  background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
  opacity: 0;
  transition: opacity 0.3s;
}

.exam-card:hover, .homework-card:hover {
  box-shadow: 0 10px 25px rgba(102, 126, 234, 0.12);
  transform: translateY(-5px);
  border-color: #667eea;
}

.exam-card:hover::before, .homework-card:hover::before {
  opacity: 1;
}

/* 状态标签样式 */
.status-badge {
  padding: 0.4rem 0.8rem;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 700;
  display: inline-flex;
  align-items: center;
  gap: 0.3rem;
}

.status-badge.未开始, .status-badge.未提交 { background: #fff5f5; color: #e74c3c; border: 1px solid #feb2b2; }
.status-badge.进行中, .status-badge.已提交 { background: #fffaf0; color: #dd6b20; border: 1px solid #fbd38d; }
.status-badge.已完成, .status-badge.已批改 { background: #f0fff4; color: #2f855a; border: 1px solid #9ae6b4; }

/* 详情信息条样式 */
.exam-info, .homework-info {
  display: flex;
  gap: 1rem;
  font-size: 0.85rem;
  color: #718096;
  margin: 1rem 0;
  padding: 0.8rem 0;
  border-top: 1px solid #f1f5f9;
  border-bottom: 1px solid #f1f5f9;
}

/* 分数显示 */
.exam-score, .homework-score {
  color: #4a5568;
  font-size: 0.9rem;
  margin-bottom: 1.2rem;
}
.exam-score strong, .homework-score strong {
  color: #2f855a;
  font-size: 1.2rem;
  margin-left: 0.3rem;
}

/* 操作按钮统一 */
.exam-btn, .homework-btn {
  width: 100%;
  padding: 0.75rem;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 700;
  transition: all 0.3s;
  font-size: 0.9rem;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.start-btn, .submit-btn { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; }
.continue-btn, .view-btn { background: linear-gradient(135deg, #f6ad55 0%, #ed8936 100%); color: white; }
.result-btn, .feedback-btn { background: linear-gradient(135deg, #4299e1 0%, #3182ce 100%); color: white; }

.exam-btn:hover, .homework-btn:hover {
  filter: brightness(1.1);
  transform: translateY(-1px);
}

/* 无内容缺省页 */
.no-content {
  text-align: center;
  padding: 5rem 0;
  color: #a0aec0;
}

/* 响应式适配 */
@media (max-width: 768px) {
  .filter-section { flex-direction: column; align-items: stretch; }
  .exams-grid, .homeworks-grid { grid-template-columns: 1fr; }
  .back-btn { padding: 0.4rem 0.6rem; font-size: 0.8rem; }
}
</style>
