<template>
  <div class="homework-center">
    <div class="page-header">
      <h1>作业中心</h1>
      <p>完成课程作业，巩固学习知识</p>
    </div>

    <div class="filter-section">
      <div class="search-box">
        <input v-model="searchQuery" type="text" placeholder="搜索作业...">
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
          <span :class="['status-badge', homework.status]">{{ homework.status }}</span>
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
    submitHomework(homeworkId) {
      this.$router.push(`/homework/${homeworkId}/submit`)
    },
    viewHomework(homeworkId) {
      this.$router.push(`/homework/${homeworkId}`)
    },
    viewFeedback(homeworkId) {
      this.$router.push(`/homework/${homeworkId}/feedback`)
    }
  }
}
</script>

<style scoped>
.homework-center {
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

.homeworks-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 1.5rem;
}

.homework-card {
  background: white;
  border: 1px solid #ecf0f1;
  border-radius: 8px;
  padding: 1.5rem;
  transition: all 0.3s;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.homework-card:hover {
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
  transform: translateY(-4px);
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
  padding: 0.25rem 0.75rem;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 600;
  white-space: nowrap;
  flex-shrink: 0;
}

.status-badge.未提交 {
  background-color: #ffe5e5;
  color: #e74c3c;
}

.status-badge.已提交 {
  background-color: #fef5e7;
  color: #f39c12;
}

.status-badge.已批改 {
  background-color: #d5f4e6;
  color: #27ae60;
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
  border-radius: 4px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s;
  font-size: 0.9rem;
}

.submit-btn {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.submit-btn:hover {
  opacity: 0.9;
  transform: translateY(-2px);
}

.view-btn {
  background-color: #3498db;
  color: white;
}

.view-btn:hover {
  background-color: #2980b9;
  transform: translateY(-2px);
}

.feedback-btn {
  background-color: #27ae60;
  color: white;
}

.feedback-btn:hover {
  background-color: #229954;
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
