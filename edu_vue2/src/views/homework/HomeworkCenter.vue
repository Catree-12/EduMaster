<template>
  <div class="homework-center">
    <div class="page-header">
      <button class="back-btn" @click="goBack">
        <i class="el-icon-arrow-left"></i>
        返回
      </button>
      <div class="header-content">
        <h1>📋 作业中心</h1>
        <p>完成课程作业，巩固学习知识</p>
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
        <input v-model="searchQuery" type="text" placeholder="搜索作业名称或课程...">
      </div>
      <div class="filter-tabs">
        <button 
          v-for="status in ['全部', '未提交', '已提交', '已批改']"
          :key="status"
          :class="{ active: activeStatus === status }"
          @click="activeStatus = status"
          class="filter-btn"
        >
          {{ status }}
        </button>
      </div>
    </div>

    <div v-if="filteredHomeworks.length > 0" class="homeworks-grid">
      <div v-for="homework in filteredHomeworks" :key="homework.id" class="homework-card">
        <div class="homework-header">
          <h3>{{ homework.name }}</h3>
          <span :class="['status-badge', homework.status]">
            <i :class="getStatusIcon(homework.status)"></i>
            {{ homework.status }}
          </span>
        </div>
        
        <p class="homework-course">📚 {{ homework.courseName }}</p>
        <p class="homework-description">{{ homework.description }}</p>
        
        <div class="homework-info">
          <span>📅 {{ homework.dueDate }}</span>
          <span>📊 {{ homework.totalPoints }}分</span>
        </div>

        <div v-if="homework.status === '已批改'" class="homework-score">
          得分: <strong>{{ homework.score }}/{{ homework.totalPoints }}</strong>
        </div>

        <button 
          v-if="homework.status === '未提交'"
          @click="submitHomework(homework.id)"
          class="homework-btn submit-btn"
        >
          提交作业
        </button>
        <button 
          v-else-if="homework.status === '已提交'"
          @click="viewHomework(homework.id)"
          class="homework-btn view-btn"
        >
          查看作业
        </button>
        <button 
          v-else
          @click="viewFeedback(homework.id)"
          class="homework-btn feedback-btn"
        >
          查看反馈
        </button>
      </div>
    </div>

    <div v-else class="no-content">
      <p>暂无作业</p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'HomeworkCenter',
  data() {
    return {
      searchQuery: '',
      activeStatus: '全部',
      homeworks: [
        {
          id: 1,
          name: '第一周练习题',
          courseName: 'Vue.js 从入门到精通',
          description: '完成第一周课程内容相关的练习题',
          dueDate: '2024-01-20',
          totalPoints: 50,
          status: '已批改',
          score: 45
        },
        {
          id: 2,
          name: '第二周练习题',
          courseName: 'Vue.js 从入门到精通',
          description: '完成第二周课程内容相关的练习题',
          dueDate: '2024-01-27',
          totalPoints: 50,
          status: '已提交'
        },
        {
          id: 3,
          name: '第三周练习题',
          courseName: 'Vue.js 从入门到精通',
          description: '完成第三周课程内容相关的练习题',
          dueDate: '2024-02-03',
          totalPoints: 50,
          status: '未提交'
        }
      ]
    }
  },
  computed: {
    filteredHomeworks() {
      return this.homeworks.filter(hw => {
        const matchSearch = hw.name.includes(this.searchQuery) || hw.courseName.includes(this.searchQuery)
        const matchStatus = this.activeStatus === '全部' || hw.status === this.activeStatus
        return matchSearch && matchStatus
      })
    }
  },
  methods: {
    goBack() {
      this.$router.push('/course/my-courses')
    },
    getStatusIcon(status) {
      const iconMap = {
        '未提交': 'el-icon-warning',
        '已提交': 'el-icon-time',
        '已批改': 'el-icon-circle-check'
      }
      return iconMap[status] || 'el-icon-info'
    },
    submitHomework(homeworkId) {
      // 跳转到作业详情页（使用 courseId=1 作为作业中心的标识）
      this.$router.push(`/student/course/1/homework/${homeworkId}`)
    },
    viewHomework(homeworkId) {
      // 跳转到作业详情页
      this.$router.push(`/student/course/1/homework/${homeworkId}`)
    },
    viewFeedback(homeworkId) {
      // 跳转到作业详情页（查看反馈）
      this.$router.push(`/student/course/1/homework/${homeworkId}`)
    }
  }
}
</script>

<style scoped>
.homework-center {
  width: 100%;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
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
  flex-shrink: 0;
}

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

.back-btn i {
  font-size: 1rem;
}

.header-content {
  position: relative;
  z-index: 2;
  text-align: center;
}

.page-header h1 {
  margin: 0 0 0.25rem 0;
  font-size: 1.25rem;
  font-weight: 700;
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
  min-width: 250px;
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
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
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
  border-color: transparent;
}

.filter-btn:hover {
  transform: translateY(-2px);
}

.homeworks-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 1.5rem;
}

.homework-card {
  background: white;
  border: 1px solid #e8ecf1;
  border-radius: 12px;
  padding: 1.5rem;
  transition: all 0.3s;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  position: relative;
  overflow: hidden;
}

.homework-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
  opacity: 0;
  transition: opacity 0.3s;
}

.homework-card:hover {
  box-shadow: 0 8px 24px rgba(102, 126, 234, 0.15);
  transform: translateY(-4px);
  border-color: #667eea;
}

.homework-card:hover::before {
  opacity: 1;
}

.homework-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1rem;
  gap: 1rem;
}

.homework-header h3 {
  margin: 0;
  color: #2c3e50;
  font-size: 1.1rem;
  flex: 1;
}

.status-badge {
  padding: 0.375rem 0.75rem;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 600;
  white-space: nowrap;
  flex-shrink: 0;
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
}

.status-badge i {
  font-size: 0.85rem;
}

.status-badge.未提交 {
  background: linear-gradient(135deg, #fff5f5 0%, #ffe5e5 100%);
  color: #e74c3c;
  border: 1px solid #ffcccc;
}

.status-badge.已提交 {
  background: linear-gradient(135deg, #fffbf0 0%, #fef5e7 100%);
  color: #f39c12;
  border: 1px solid #fdeaa8;
}

.status-badge.已批改 {
  background: linear-gradient(135deg, #f0fdf4 0%, #d5f4e6 100%);
  color: #27ae60;
  border: 1px solid #a8e6cf;
}

.homework-course {
  color: #7f8c8d;
  font-size: 0.9rem;
  margin: 0 0 0.5rem 0;
}

.homework-description {
  color: #7f8c8d;
  font-size: 0.85rem;
  margin: 0 0 1rem 0;
  line-height: 1.5;
}

.homework-info {
  display: flex;
  gap: 1rem;
  font-size: 0.9rem;
  color: #7f8c8d;
  margin-bottom: 1rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #ecf0f1;
}

.homework-score {
  color: #667eea;
  font-weight: 500;
  margin-bottom: 1rem;
  font-size: 0.95rem;
}

.homework-score strong {
  color: #27ae60;
  font-size: 1.1rem;
}

.homework-btn {
  width: 100%;
  padding: 0.65rem;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s;
  font-size: 0.9rem;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.submit-btn {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

.submit-btn:hover {
  box-shadow: 0 6px 16px rgba(102, 126, 234, 0.4);
  transform: translateY(-2px);
}

.view-btn {
  background: linear-gradient(135deg, #3498db 0%, #2980b9 100%);
  color: white;
  box-shadow: 0 4px 12px rgba(52, 152, 219, 0.3);
}

.view-btn:hover {
  box-shadow: 0 6px 16px rgba(52, 152, 219, 0.4);
  transform: translateY(-2px);
}

.feedback-btn {
  background: linear-gradient(135deg, #27ae60 0%, #229954 100%);
  color: white;
  box-shadow: 0 4px 12px rgba(39, 174, 96, 0.3);
}

.feedback-btn:hover {
  box-shadow: 0 6px 16px rgba(39, 174, 96, 0.4);
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

  .homeworks-grid {
    grid-template-columns: 1fr;
  }
}
</style>
