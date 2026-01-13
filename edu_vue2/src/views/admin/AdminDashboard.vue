<template>
  <div class="admin-dashboard">
    <h1 class="page-title">管理员仪表板</h1>

    <!-- 数据统计卡片 -->
    <div class="stats-cards">
      <div class="stat-card">
        <div class="stat-icon" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
          <i class="el-icon-user"></i>
        </div>
        <div class="stat-content">
          <p class="stat-label">总用户数</p>
          <h2 class="stat-value">{{ stats.totalUsers }}</h2>
          <span class="stat-change positive">+{{ stats.newUsersToday }} 今日新增</span>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">
          <i class="el-icon-reading"></i>
        </div>
        <div class="stat-content">
          <p class="stat-label">总课程数</p>
          <h2 class="stat-value">{{ stats.totalCourses }}</h2>
          <span class="stat-change positive">+{{ stats.newCoursesToday }} 今日新增</span>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">
          <i class="el-icon-medal"></i>
        </div>
        <div class="stat-content">
          <p class="stat-label">颁发证书数</p>
          <h2 class="stat-value">{{ stats.totalCertificates }}</h2>
          <span class="stat-change positive">+{{ stats.newCertificatesToday }} 今日新增</span>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon" style="background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);">
          <i class="el-icon-bell"></i>
        </div>
        <div class="stat-content">
          <p class="stat-label">待处理任务</p>
          <h2 class="stat-value">{{ stats.pendingTasks }}</h2>
          <span class="stat-change">需要处理</span>
        </div>
      </div>
    </div>

    <!-- 待处理任务列表 -->
    <el-card class="task-card" shadow="hover">
      <div slot="header" class="card-header">
        <span class="card-title">⚡ 待处理任务</span>
      </div>
      
      <div class="task-list">
        <div class="task-item" @click="goToPage('/admin/course-audit')">
          <div class="task-info">
            <i class="el-icon-document-checked task-icon"></i>
            <span class="task-name">待审核课程</span>
          </div>
          <el-badge :value="tasks.pendingCourses" class="task-badge" />
          <i class="el-icon-arrow-right"></i>
        </div>

        <div class="task-item" @click="goToPage('/admin/content-review')">
          <div class="task-info">
            <i class="el-icon-warning task-icon"></i>
            <span class="task-name">用户举报内容</span>
          </div>
          <el-badge :value="tasks.pendingReports" class="task-badge" />
          <i class="el-icon-arrow-right"></i>
        </div>

        <div class="task-item" @click="goToPage('/admin/certificates')">
          <div class="task-info">
            <i class="el-icon-medal task-icon"></i>
            <span class="task-name">证书申诉</span>
          </div>
          <el-badge :value="tasks.certificateAppeals" class="task-badge" />
          <i class="el-icon-arrow-right"></i>
        </div>
      </div>
    </el-card>

    <!-- 图表区域 -->
    <div class="charts-container">
      <el-card class="chart-card" shadow="hover">
        <div slot="header" class="card-header">
          <span class="card-title">📈 用户增长趋势</span>
        </div>
        <div class="chart-placeholder">
          <i class="el-icon-data-line" style="font-size: 64px; color: #dcdfe6;"></i>
          <p>图表数据加载中...</p>
          <p class="chart-hint">提示：可接入 ECharts 显示用户增长趋势图</p>
        </div>
      </el-card>

      <el-card class="chart-card" shadow="hover">
        <div slot="header" class="card-header">
          <span class="card-title">📊 课程分类统计</span>
        </div>
        <div class="chart-placeholder">
          <i class="el-icon-pie-chart" style="font-size: 64px; color: #dcdfe6;"></i>
          <p>图表数据加载中...</p>
          <p class="chart-hint">提示：可接入 ECharts 显示课程分类分布</p>
        </div>
      </el-card>
    </div>

    <!-- 最近活动 -->
    <el-card class="activity-card" shadow="hover">
      <div slot="header" class="card-header">
        <span class="card-title">🕐 最近活动</span>
      </div>
      
      <el-timeline>
        <el-timeline-item
          v-for="activity in recentActivities"
          :key="activity.id"
          :timestamp="activity.time"
          placement="top"
        >
          <p>{{ activity.description }}</p>
        </el-timeline-item>
      </el-timeline>
    </el-card>
  </div>
</template>

<script>
export default {
  name: 'AdminDashboard',
  data() {
    return {
      stats: {
        totalUsers: 1234,
        newUsersToday: 15,
        totalCourses: 456,
        newCoursesToday: 3,
        totalCertificates: 789,
        newCertificatesToday: 8,
        pendingTasks: 12
      },
      tasks: {
        pendingCourses: 5,
        pendingReports: 3,
        certificateAppeals: 2
      },
      recentActivities: [
        {
          id: 1,
          time: '2024-03-15 14:30',
          description: '用户 张三 注册了账号'
        },
        {
          id: 2,
          time: '2024-03-15 13:20',
          description: '课程 "前端开发基础" 提交审核'
        },
        {
          id: 3,
          time: '2024-03-15 11:45',
          description: '用户 李四 获得了证书'
        },
        {
          id: 4,
          time: '2024-03-15 10:30',
          description: '审核通过课程 "Python入门"'
        }
      ]
    }
  },
  mounted() {
    this.fetchDashboardData()
  },
  methods: {
    async fetchDashboardData() {
      // TODO: 从API获取仪表板数据
      // const data = await this.$api.get('/admin/dashboard')
      // this.stats = data.stats
      // this.tasks = data.tasks
      // this.recentActivities = data.activities
    },
    
    goToPage(path) {
      this.$router.push(path)
    }
  }
}
</script>

<style scoped>
.admin-dashboard {
  max-width: 1400px;
  margin: 0 auto;
}

.page-title {
  margin: 0 0 2rem 0;
  font-size: 1.75rem;
  color: #2c3e50;
}

/* 统计卡片 */
.stats-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.stat-card {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  display: flex;
  gap: 1rem;
  transition: transform 0.2s;
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.stat-icon {
  width: 60px;
  height: 60px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 28px;
}

.stat-content {
  flex: 1;
}

.stat-label {
  margin: 0 0 0.5rem 0;
  font-size: 0.875rem;
  color: #7f8c8d;
}

.stat-value {
  margin: 0 0 0.5rem 0;
  font-size: 2rem;
  font-weight: 700;
  color: #2c3e50;
}

.stat-change {
  font-size: 0.875rem;
  color: #7f8c8d;
}

.stat-change.positive {
  color: #27ae60;
}

/* 卡片样式 */
.task-card,
.chart-card,
.activity-card {
  margin-bottom: 1.5rem;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-title {
  font-size: 1.1rem;
  font-weight: 600;
  color: #2c3e50;
}

/* 任务列表 */
.task-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.task-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s;
}

.task-item:hover {
  background: #e9ecef;
  transform: translateX(4px);
}

.task-info {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  flex: 1;
}

.task-icon {
  font-size: 20px;
  color: #667eea;
}

.task-name {
  font-weight: 500;
  color: #2c3e50;
}

.task-badge {
  margin-right: 0.5rem;
}

/* 图表区域 */
.charts-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 1.5rem;
  margin-bottom: 1.5rem;
}

.chart-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 300px;
  color: #7f8c8d;
}

.chart-hint {
  font-size: 0.875rem;
  color: #95a5a6;
  margin-top: 0.5rem;
}

/* 响应式 */
@media (max-width: 768px) {
  .stats-cards {
    grid-template-columns: 1fr;
  }
  
  .charts-container {
    grid-template-columns: 1fr;
  }
}
</style>
