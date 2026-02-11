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
      this.$router.push('/courses/mycourses')
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
      this.$router.push(`/student/courses/1/homework/${homeworkId}`)
    },
    viewHomework(homeworkId) {
      // 跳转到作业详情页
      this.$router.push(`/student/courses/1/homework/${homeworkId}`)
    },
    viewFeedback(homeworkId) {
      // 跳转到作业详情页（查看反馈）
      this.$router.push(`/student/courses/1/homework/${homeworkId}`)
    }
  }
}
</script>

<style scoped>
/* --- 页面整体容器 --- */
.homework-center {
  width: 100%;
  min-height: calc(100vh - 64px);
  display: flex;
  flex-direction: column;
  padding: 2rem;
  background: #f5f7fa;
  box-sizing: border-box;
}

/* --- Header 头部区域 --- */
.page-header {
  margin-bottom: 1.5rem;
  position: relative;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 12px;
  padding: 0.3rem 1rem; /* 增加内边距，解决“太贴”的问题 */
  color: white;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.2);
  flex-shrink: 0;
}

/* 统一返回按钮：绝对定位 */
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

/* 背景圆圈装饰 */
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

/* --- 筛选与搜索区域 (同步考试中心美化版) --- */
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

/* --- 作业卡片网格 --- */
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
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
  position: relative;
  overflow: hidden;
}

/* 卡片顶部渐变条装饰 */
.homework-card::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0; height: 4px;
  background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
  opacity: 0;
  transition: opacity 0.3s;
}

.homework-card:hover {
  box-shadow: 0 10px 25px rgba(102, 126, 234, 0.12);
  transform: translateY(-5px);
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
}

.homework-header h3 {
  margin: 0;
  color: #2d3748;
  font-size: 1.1rem;
  font-weight: 700;
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

.status-badge.未提交 { background: #fff5f5; color: #e74c3c; border: 1px solid #feb2b2; }
.status-badge.已提交 { background: #fffaf0; color: #dd6b20; border: 1px solid #fbd38d; }
.status-badge.已批改 { background: #f0fff4; color: #2f855a; border: 1px solid #9ae6b4; }

.homework-course {
  color: #4a5568;
  font-size: 0.9rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
}

.homework-description {
  color: #718096;
  font-size: 0.85rem;
  line-height: 1.5;
  margin-bottom: 1rem;
}

.homework-info {
  display: flex;
  gap: 1rem;
  font-size: 0.85rem;
  color: #718096;
  margin-bottom: 1rem;
  padding: 0.8rem 0;
  border-top: 1px solid #f1f5f9;
  border-bottom: 1px solid #f1f5f9;
}

.homework-score {
  color: #4a5568;
  font-size: 0.9rem;
  margin-bottom: 1.2rem;
}

.homework-score strong {
  color: #2f855a;
  font-size: 1.2rem;
  margin-left: 0.3rem;
}

/* 按钮样式统一 */
.homework-btn {
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

.submit-btn { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; }
.view-btn { background: linear-gradient(135deg, #f6ad55 0%, #ed8936 100%); color: white; }
.feedback-btn { background: linear-gradient(135deg, #4299e1 0%, #3182ce 100%); color: white; }

.homework-btn:hover {
  filter: brightness(1.1);
  transform: translateY(-1px);
}

.no-content {
  text-align: center;
  padding: 5rem 0;
  color: #a0aec0;
}
</style>
