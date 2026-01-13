<template>
  <div class="certificate-management">
    <div class="page-header">
      <h1>证书管理</h1>
      <p class="subtitle">管理和查看已颁发的电子证书</p>
    </div>

    <!-- 统计卡片 -->
    <el-row :gutter="20" class="stats-row">
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-content">
            <i class="el-icon-medal"></i>
            <div>
              <div class="stat-value">{{ statistics.total }}</div>
              <div class="stat-label">颁发总数</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-content">
            <i class="el-icon-trophy"></i>
            <div>
              <div class="stat-value">{{ statistics.thisMonth }}</div>
              <div class="stat-label">本月颁发</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-content">
            <i class="el-icon-document"></i>
            <div>
              <div class="stat-value">{{ statistics.courses }}</div>
              <div class="stat-label">课程数量</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-content">
            <i class="el-icon-share"></i>
            <div>
              <div class="stat-value">{{ statistics.shared }}</div>
              <div class="stat-label">分享次数</div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 搜索和筛选 -->
    <el-card class="filter-card">
      <el-form :inline="true" :model="filters">
        <el-form-item label="课程">
          <el-select v-model="filters.courseId" placeholder="全部课程" clearable style="width: 200px">
            <el-option label="Vue.js 全栈开发" value="1"></el-option>
            <el-option label="Python 数据分析" value="2"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="搜索">
          <el-input 
            v-model="filters.keyword" 
            placeholder="证书编号/学生姓名" 
            clearable
            style="width: 250px;">
            <el-button slot="append" icon="el-icon-search"></el-button>
          </el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" icon="el-icon-download">导出数据</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 证书列表 -->
    <el-card>
      <el-table :data="certificates" v-loading="loading">
        <el-table-column prop="certNumber" label="证书编号" width="180"></el-table-column>
        <el-table-column prop="studentName" label="学生姓名" width="120"></el-table-column>
        <el-table-column prop="courseName" label="课程名称" min-width="200"></el-table-column>
        <el-table-column label="考试成绩" width="100" align="center">
          <template slot-scope="scope">
            <span :class="{'high-score': scope.row.score >= 90}">
              {{ scope.row.score }}分
            </span>
          </template>
        </el-table-column>
        <el-table-column label="颁发时间" width="180">
          <template slot-scope="scope">
            {{ formatDate(scope.row.issuedAt) }}
          </template>
        </el-table-column>
        <el-table-column label="分享次数" width="100" align="center">
          <template slot-scope="scope">
            {{ scope.row.shareCount || 0 }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="180" fixed="right">
          <template slot-scope="scope">
            <el-button type="text" size="small" @click="handleView(scope.row)">
              <i class="el-icon-view"></i> 查看
            </el-button>
            <el-button type="text" size="small" @click="handleDownload(scope.row)">
              <i class="el-icon-download"></i> 下载
            </el-button>
            <el-button type="text" size="small" @click="handleRevoke(scope.row)">
              <i class="el-icon-delete"></i> 撤销
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination-container">
        <el-pagination
          @current-change="handlePageChange"
          :current-page="pagination.page"
          :page-size="pagination.pageSize"
          :total="pagination.total"
          layout="total, prev, pager, next">
        </el-pagination>
      </div>
    </el-card>

    <!-- 证书预览对话框 -->
    <el-dialog
      title="证书预览"
      :visible.sync="previewDialog.visible"
      width="700px">
      <div v-if="previewDialog.cert" class="cert-preview">
        <div class="cert-content">
          <h2>结业证书</h2>
          <p class="cert-number">证书编号: {{ previewDialog.cert.certNumber }}</p>
          <div class="cert-body">
            <p>兹证明</p>
            <p class="student-name">{{ previewDialog.cert.studentName }}</p>
            <p>完成了课程</p>
            <p class="course-name">《{{ previewDialog.cert.courseName }}》</p>
            <p>考试成绩: <span class="score">{{ previewDialog.cert.score }}</span> 分</p>
            <p class="issue-date">颁发日期: {{ formatDate(previewDialog.cert.issuedAt) }}</p>
          </div>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script>
export default {
  name: 'CertificateManagement',
  data() {
    return {
      loading: false,
      statistics: {
        total: 789,
        thisMonth: 56,
        courses: 23,
        shared: 234
      },
      filters: {
        courseId: '',
        keyword: ''
      },
      certificates: [],
      pagination: {
        page: 1,
        pageSize: 10,
        total: 0
      },
      previewDialog: {
        visible: false,
        cert: null
      }
    }
  },
  mounted() {
    this.fetchCertificates()
  },
  methods: {
    fetchCertificates() {
      this.loading = true
      setTimeout(() => {
        this.certificates = this.getMockCertificates()
        this.pagination.total = 789
        this.loading = false
      }, 500)
    },
    handleView(cert) {
      this.previewDialog.cert = cert
      this.previewDialog.visible = true
    },
    handleDownload() {
      this.$message.success('证书下载中...')
    },
    handleRevoke() {
      this.$confirm('确认撤销该证书？撤销后无法恢复。', '警告', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.$message.success('证书已撤销')
        this.fetchCertificates()
      })
    },
    handlePageChange(page) {
      this.pagination.page = page
      this.fetchCertificates()
    },
    formatDate(date) {
      return new Date(date).toLocaleDateString('zh-CN')
    },
    getMockCertificates() {
      return Array.from({ length: 10 }, (_, i) => ({
        id: i + 1,
        certNumber: `CERT-2024-${String(10000 + i).padStart(5, '0')}`,
        studentName: `学生${String.fromCharCode(65 + i)}`,
        courseName: ['Vue.js 全栈开发', 'Python 数据分析', '机器学习基础'][i % 3],
        score: 60 + Math.floor(Math.random() * 40),
        issuedAt: new Date(Date.now() - Math.random() * 180 * 24 * 60 * 60 * 1000).toISOString(),
        shareCount: Math.floor(Math.random() * 20)
      }))
    }
  }
}
</script>

<style scoped>
.certificate-management {
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

.stats-row {
  margin: 20px 0;
}

.stat-card {
  border-left: 4px solid #409EFF;
}

.stat-content {
  display: flex;
  align-items: center;
  gap: 15px;
}

.stat-content i {
  font-size: 36px;
  color: #409EFF;
}

.stat-value {
  font-size: 28px;
  font-weight: bold;
}

.stat-label {
  font-size: 14px;
  color: #909399;
  margin-top: 5px;
}

.filter-card {
  margin-bottom: 20px;
}

.high-score {
  color: #67C23A;
  font-weight: bold;
}

.pagination-container {
  margin-top: 20px;
  text-align: right;
}

.cert-preview {
  text-align: center;
  padding: 40px;
  border: 2px solid #409EFF;
  border-radius: 8px;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

.cert-content h2 {
  color: #409EFF;
  font-size: 32px;
  margin-bottom: 20px;
}

.cert-number {
  color: #909399;
  font-size: 14px;
  margin-bottom: 30px;
}

.cert-body {
  margin: 30px 0;
}

.student-name,
.course-name {
  font-size: 24px;
  font-weight: bold;
  color: #303133;
  margin: 15px 0;
}

.score {
  color: #67C23A;
  font-size: 20px;
  font-weight: bold;
}

.issue-date {
  margin-top: 30px;
  color: #606266;
}
</style>
