<template>
  <div class="analytics">
    <div class="page-header">
      <h1>数据统计</h1>
      <p class="subtitle">平台运营数据分析与可视化</p>
    </div>

    <!-- 时间范围选择 -->
    <el-card class="time-range-card">
      <el-radio-group v-model="timeRange" @change="fetchData">
        <el-radio-button label="today">今日</el-radio-button>
        <el-radio-button label="week">本周</el-radio-button>
        <el-radio-button label="month">本月</el-radio-button>
        <el-radio-button label="year">本年</el-radio-button>
        <el-radio-button label="custom">自定义</el-radio-button>
      </el-radio-group>
      
      <el-date-picker
        v-if="timeRange === 'custom'"
        v-model="customDateRange"
        type="daterange"
        range-separator="至"
        start-placeholder="开始日期"
        end-placeholder="结束日期"
        style="margin-left: 20px">
      </el-date-picker>
    </el-card>

    <!-- 核心指标 -->
    <el-row :gutter="20" class="metrics-row">
      <el-col :span="6">
        <el-card class="metric-card">
          <div class="metric-content">
            <i class="el-icon-user metric-icon user"></i>
            <div>
              <div class="metric-value">{{ metrics.users }}</div>
              <div class="metric-label">新增用户</div>
              <div class="metric-trend up">
                <i class="el-icon-top"></i> {{ metrics.usersTrend }}%
              </div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="metric-card">
          <div class="metric-content">
            <i class="el-icon-document metric-icon course"></i>
            <div>
              <div class="metric-value">{{ metrics.courses }}</div>
              <div class="metric-label">新增课程</div>
              <div class="metric-trend up">
                <i class="el-icon-top"></i> {{ metrics.coursesTrend }}%
              </div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="metric-card">
          <div class="metric-content">
            <i class="el-icon-reading metric-icon enrollment"></i>
            <div>
              <div class="metric-value">{{ metrics.enrollments }}</div>
              <div class="metric-label">选课次数</div>
              <div class="metric-trend down">
                <i class="el-icon-bottom"></i> {{ metrics.enrollmentsTrend }}%
              </div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="metric-card">
          <div class="metric-content">
            <i class="el-icon-medal metric-icon cert"></i>
            <div>
              <div class="metric-value">{{ metrics.certificates }}</div>
              <div class="metric-label">颁发证书</div>
              <div class="metric-trend up">
                <i class="el-icon-top"></i> {{ metrics.certificatesTrend }}%
              </div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 图表区域 -->
    <el-row :gutter="20" class="charts-row">
      <el-col :span="12">
        <el-card>
          <div slot="header">
            <span>用户增长趋势</span>
          </div>
          <div class="chart-placeholder">
            <i class="el-icon-s-data"></i>
            <p>用户增长折线图</p>
            <p class="tip">TODO: 集成 ECharts 或 Chart.js</p>
          </div>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card>
          <div slot="header">
            <span>课程分类分布</span>
          </div>
          <div class="chart-placeholder">
            <i class="el-icon-pie-chart"></i>
            <p>课程分类饼图</p>
            <p class="tip">TODO: 集成 ECharts 或 Chart.js</p>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" class="charts-row">
      <el-col :span="12">
        <el-card>
          <div slot="header">
            <span>热门课程排行</span>
          </div>
          <div class="chart-placeholder">
            <i class="el-icon-s-marketing"></i>
            <p>热门课程条形图</p>
            <p class="tip">TODO: 集成 ECharts 或 Chart.js</p>
          </div>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card>
          <div slot="header">
            <span>学习活跃度</span>
          </div>
          <div class="chart-placeholder">
            <i class="el-icon-data-line"></i>
            <p>学习活跃度热力图</p>
            <p class="tip">TODO: 集成 ECharts 或 Chart.js</p>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 详细数据表格 -->
    <el-card class="data-table-card">
      <div slot="header">
        <span>详细数据</span>
        <el-button type="text" style="float: right" @click="exportData">
          <i class="el-icon-download"></i> 导出
        </el-button>
      </div>
      
      <el-tabs v-model="activeTab">
        <el-tab-pane label="用户数据" name="users">
          <el-table :data="userData" style="width: 100%">
            <el-table-column prop="date" label="日期" width="120"></el-table-column>
            <el-table-column prop="newUsers" label="新增用户" width="100"></el-table-column>
            <el-table-column prop="activeUsers" label="活跃用户" width="100"></el-table-column>
            <el-table-column prop="totalUsers" label="累计用户" width="100"></el-table-column>
          </el-table>
        </el-tab-pane>
        
        <el-tab-pane label="课程数据" name="courses">
          <el-table :data="courseData" style="width: 100%">
            <el-table-column prop="date" label="日期" width="120"></el-table-column>
            <el-table-column prop="newCourses" label="新增课程" width="100"></el-table-column>
            <el-table-column prop="enrollments" label="选课人次" width="100"></el-table-column>
            <el-table-column prop="completions" label="完成人次" width="100"></el-table-column>
          </el-table>
        </el-tab-pane>
      </el-tabs>
    </el-card>
  </div>
</template>

<script>
export default {
  name: 'AdminAnalytics',
  data() {
    return {
      timeRange: 'month',
      customDateRange: null,
      metrics: {
        users: 156,
        usersTrend: 12.5,
        courses: 23,
        coursesTrend: 8.3,
        enrollments: 432,
        enrollmentsTrend: -3.2,
        certificates: 89,
        certificatesTrend: 15.7
      },
      activeTab: 'users',
      userData: [],
      courseData: []
    }
  },
  mounted() {
    this.fetchData()
  },
  methods: {
    fetchData() {
      // TODO: 调用API获取数据
      this.generateMockData()
    },
    generateMockData() {
      this.userData = Array.from({ length: 7 }, (_, i) => ({
        date: new Date(Date.now() - i * 24 * 60 * 60 * 1000).toLocaleDateString('zh-CN'),
        newUsers: Math.floor(Math.random() * 50) + 10,
        activeUsers: Math.floor(Math.random() * 200) + 100,
        totalUsers: 1000 + i * 10
      })).reverse()

      this.courseData = Array.from({ length: 7 }, (_, i) => ({
        date: new Date(Date.now() - i * 24 * 60 * 60 * 1000).toLocaleDateString('zh-CN'),
        newCourses: Math.floor(Math.random() * 5),
        enrollments: Math.floor(Math.random() * 100) + 20,
        completions: Math.floor(Math.random() * 30) + 5
      })).reverse()
    },
    exportData() {
      this.$message.success('数据导出中...')
    }
  }
}
</script>

<style scoped>
.analytics {
  padding: 20px;
}

.page-header h1 {
  margin: 0 0 8px 0;
  font-size: 24px;
}

.page-header .subtitle {
  margin: 0;
  color: #909399;
  font-size: 14px;
}

.time-range-card {
  margin: 20px 0;
}

.metrics-row {
  margin: 20px 0;
}

.metric-card {
  border-left: 4px solid #409EFF;
}

.metric-content {
  display: flex;
  align-items: center;
  gap: 15px;
}

.metric-icon {
  font-size: 48px;
}

.metric-icon.user { color: #409EFF; }
.metric-icon.course { color: #67C23A; }
.metric-icon.enrollment { color: #E6A23C; }
.metric-icon.cert { color: #F56C6C; }

.metric-value {
  font-size: 32px;
  font-weight: bold;
  color: #303133;
}

.metric-label {
  font-size: 14px;
  color: #909399;
  margin-top: 5px;
}

.metric-trend {
  font-size: 12px;
  margin-top: 5px;
}

.metric-trend.up {
  color: #67C23A;
}

.metric-trend.down {
  color: #F56C6C;
}

.charts-row {
  margin: 20px 0;
}

.chart-placeholder {
  height: 300px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background-color: #f5f7fa;
  border-radius: 4px;
}

.chart-placeholder i {
  font-size: 64px;
  color: #909399;
  margin-bottom: 10px;
}

.chart-placeholder p {
  margin: 5px 0;
  color: #606266;
}

.chart-placeholder .tip {
  font-size: 12px;
  color: #909399;
}

.data-table-card {
  margin-top: 20px;
}
</style>
