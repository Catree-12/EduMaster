<template>
  <div class="certificates-container">
    <div class="page-header">
      <h1>我的证书</h1>
      <p class="subtitle">查看你获得的电子证书</p>
    </div>

    <!-- 统计信息 -->
    <el-row :gutter="20" class="stats-row">
      <el-col :xs="24" :sm="6">
        <div class="stat-card">
          <i class="el-icon-trophy" />
          <div>
            <p class="stat-value">{{ stats.total }}</p>
            <p class="stat-label">总证书数</p>
          </div>
        </div>
      </el-col>
      <el-col :xs="24" :sm="6">
        <div class="stat-card success">
          <i class="el-icon-circle-check" />
          <div>
            <p class="stat-value">{{ stats.active }}</p>
            <p class="stat-label">有效证书</p>
          </div>
        </div>
      </el-col>
      <el-col :xs="24" :sm="6">
        <div class="stat-card warning">
          <i class="el-icon-info" />
          <div>
            <p class="stat-value">{{ stats.revoked }}</p>
            <p class="stat-label">已吊销</p>
          </div>
        </div>
      </el-col>
      <el-col :xs="24" :sm="6">
        <div class="stat-card danger">
          <i class="el-icon-circle-close" />
          <div>
            <p class="stat-value">{{ stats.expired }}</p>
            <p class="stat-label">已过期</p>
          </div>
        </div>
      </el-col>
    </el-row>

    <!-- 筛选和搜索 -->
    <el-card class="filter-card" shadow="hover">
      <el-row :gutter="20">
        <el-col :xs="24" :sm="8">
          <el-input
            v-model="searchKey"
            placeholder="搜索课程名或证书编号..."
            @keyup.enter="search"
          >
            <el-button slot="append" icon="el-icon-search" @click="search" />
          </el-input>
        </el-col>
        <el-col :xs="24" :sm="8">
          <el-select v-model="filterStatus" placeholder="筛选状态" clearable @change="search">
            <el-option label="全部" value="" />
            <el-option label="有效" value="active" />
            <el-option label="已吊销" value="revoked" />
            <el-option label="已过期" value="expired" />
          </el-select>
        </el-col>
        <el-col :xs="24" :sm="8">
          <el-button type="primary" @click="search" icon="el-icon-search">
            搜索
          </el-button>
          <el-button @click="resetFilter" icon="el-icon-refresh">
            重置
          </el-button>
        </el-col>
      </el-row>
    </el-card>

    <!-- 证书列表 -->
    <el-card class="certificates-card" shadow="hover">
      <el-table
        :data="certificates"
        v-loading="loading"
        class="certificates-table"
        stripe
        style="width: 100%"
      >
        <!-- 课程名 -->
        <el-table-column prop="courseName" label="课程名称" min-width="180">
          <template slot-scope="scope">
            <div class="course-info">
              <p class="name">{{ scope.row.courseName }}</p>
              <p class="term">{{ scope.row.termName }}</p>
            </div>
          </template>
        </el-table-column>

        <!-- 成绩 -->
        <el-table-column prop="score" label="成绩" width="100" align="center">
          <template slot-scope="scope">
            <el-tag
              :type="scope.row.score >= scope.row.passingScore ? 'success' : 'danger'"
            >
              {{ scope.row.score }} 分
            </el-tag>
          </template>
        </el-table-column>

        <!-- 颁发日期 -->
        <el-table-column prop="issueDate" label="颁发日期" width="120" align="center" />

        <!-- 证书编号 -->
        <el-table-column prop="certificateNo" label="证书编号" min-width="160">
          <template slot-scope="scope">
            <span class="cert-no">{{ scope.row.certificateNo }}</span>
          </template>
        </el-table-column>

        <!-- 状态 -->
        <el-table-column prop="status" label="状态" width="100" align="center">
          <template slot-scope="scope">
            <el-tag :type="getStatusType(scope.row.status)">
              {{ getStatusText(scope.row.status) }}
            </el-tag>
          </template>
        </el-table-column>

        <!-- 操作 -->
        <el-table-column label="操作" width="180" align="center" fixed="right">
          <template slot-scope="scope">
            <el-button
              type="text"
              size="small"
              @click="viewCertificate(scope.row)"
            >
              查看
            </el-button>
            <el-button
              type="text"
              size="small"
              @click="downloadCertificate(scope.row)"
            >
              下载
            </el-button>
            <el-button
              type="text"
              size="small"
              @click="shareCertificate(scope.row)"
            >
              分享
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <el-pagination
        :current-page="page"
        :page-size="pageSize"
        :total="total"
        :page-sizes="[10, 20, 50]"
        layout="total, sizes, prev, pager, next, jumper"
        @size-change="pageSize = $event; search()"
        @current-change="page = $event; search()"
        class="pagination"
      />
    </el-card>

    <!-- 空状态 -->
    <div v-if="!loading && certificates.length === 0" class="empty-state">
      <i class="el-icon-document" />
      <p>还没有获得任何证书</p>
      <p class="tip">完成课程学习并通过考试即可获得电子证书</p>
      <el-button type="primary" @click="goCourseCenter">
        去选课学习
      </el-button>
    </div>

    <!-- 证书详情对话框 -->
    <CertificateDetail
      v-if="detailVisible"
      :visible.sync="detailVisible"
      :certificate="selectedCertificate"
    />

    <!-- 证书分享对话框 -->
    <CertificateShare
      v-if="shareVisible"
      :visible.sync="shareVisible"
      :certificate="selectedCertificate"
    />
  </div>
</template>

<script>
import CertificateDetail from './CertificateDetail.vue'
import CertificateShare from './CertificateShare.vue'

export default {
  name: 'MyCertificates',
  components: {
    CertificateDetail,
    CertificateShare
  },
  data() {
    return {
      loading: false,
      certificates: [],
      page: 1,
      pageSize: 10,
      total: 0,
      searchKey: '',
      filterStatus: '',
      stats: {
        total: 0,
        active: 0,
        revoked: 0,
        expired: 0
      },
      detailVisible: false,
      shareVisible: false,
      selectedCertificate: null
    }
  },
  created() {
    // 使用模拟数据代替 API 调用
    this.loadMockData()
  },
  methods: {
    // 加载模拟数据
    loadMockData() {
      this.loading = true
      
      // 模拟统计数据
      this.stats = {
        total: 5,
        active: 3,
        revoked: 1,
        expired: 1
      }
      
      // 模拟证书列表数据
      setTimeout(() => {
        this.certificates = [
          {
            id: 1,
            courseName: 'Vue.js 从入门到精通',
            termName: '2024年春季班',
            score: 95,
            status: 'active',
            issueDate: '2024-06-15',
            expiryDate: '2026-06-15',
            certificateNumber: 'CERT-VUE-2024-001'
          },
          {
            id: 2,
            courseName: 'React 现代实战指南',
            termName: '2024年夏季班',
            score: 88,
            status: 'active',
            issueDate: '2024-08-20',
            expiryDate: '2026-08-20',
            certificateNumber: 'CERT-REACT-2024-002'
          },
          {
            id: 3,
            courseName: 'Node.js 全栈开发',
            termName: '2024年春季班',
            score: 92,
            status: 'active',
            issueDate: '2024-05-10',
            expiryDate: '2026-05-10',
            certificateNumber: 'CERT-NODE-2024-003'
          },
          {
            id: 4,
            courseName: 'Python 数据分析',
            termName: '2023年秋季班',
            score: 85,
            status: 'expired',
            issueDate: '2023-12-01',
            expiryDate: '2025-12-01',
            certificateNumber: 'CERT-PY-2023-004'
          },
          {
            id: 5,
            courseName: 'UI/UX 设计原则',
            termName: '2024年春季班',
            score: 78,
            status: 'revoked',
            issueDate: '2024-04-15',
            expiryDate: '2026-04-15',
            certificateNumber: 'CERT-UIUX-2024-005'
          }
        ]
        this.total = this.certificates.length
        this.loading = false
      }, 500)
    },
    
    // 获取证书列表
    fetchCertificates() {
      this.loadMockData()
    },

    // 获取统计信息
    fetchStats() {
      // 已在 loadMockData 中处理
    },

    // 搜索
    search() {
      this.page = 1
      this.fetchCertificates()
    },

    // 重置筛选
    resetFilter() {
      this.searchKey = ''
      this.filterStatus = ''
      this.page = 1
      this.fetchCertificates()
    },

    // 获取状态样式
    getStatusType(status) {
      const types = {
        active: 'success',
        revoked: 'danger',
        expired: 'warning'
      }
      return types[status] || 'info'
    },

    // 获取状态文本
    getStatusText(status) {
      const texts = {
        active: '有效',
        revoked: '已吊销',
        expired: '已过期'
      }
      return texts[status] || status
    },

    // 查看证书
    viewCertificate(certificate) {
      this.selectedCertificate = certificate
      this.detailVisible = true
    },

    // 下载证书
    downloadCertificate(certificate) {
      window.location.href = `/api/certificate/${certificate.id}/download`
      this.$message.success('下载开始...')
    },

    // 分享证书
    shareCertificate(certificate) {
      this.selectedCertificate = certificate
      this.shareVisible = true
    },

    // 去选课
    goCourseCenter() {
      this.$router.push('/course/center')
    }
  }
}
</script>

<style scoped lang="scss">
.certificates-container {
  padding: 1.5rem;
  background: #f9fafb;
  min-height: 100vh;

  .page-header {
    margin-bottom: 1rem;
    text-align: center;
    padding: 0.8rem 1rem;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 8px;
    color: white;
    box-shadow: 0 2px 6px rgba(102, 126, 234, 0.2);

    h1 {
      margin: 0;
      font-size: 1.25rem;
      font-weight: 700;
    }

    .subtitle {
      margin: 0.25rem 0 0 0;
      color: rgba(255, 255, 255, 0.9);
      font-size: 0.875rem;
    }
  }

  .stats-row {
    margin-bottom: 30px;

    .stat-card {
      background: white;
      border-radius: 4px;
      padding: 20px;
      display: flex;
      align-items: center;
      gap: 15px;
      box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
      transition: all 0.3s ease;

      &:hover {
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        transform: translateY(-2px);
      }

      i {
        font-size: 32px;
        color: #1890ff;
      }

      .stat-value {
        font-size: 24px;
        font-weight: bold;
        color: #333;
        margin: 0;
      }

      .stat-label {
        font-size: 12px;
        color: #999;
        margin: 5px 0 0 0;
      }

      &.success i {
        color: #67c23a;
      }

      &.warning i {
        color: #e6a23c;
      }

      &.danger i {
        color: #f56c6c;
      }
    }
  }

  .filter-card {
    margin-bottom: 20px;
    border: none;
    border-radius: 4px;
  }

  .certificates-card {
    border: none;
    border-radius: 4px;

    .certificates-table {
      .course-info {
        .name {
          font-size: 13px;
          color: #333;
          margin: 0;
          font-weight: 500;
        }

        .term {
          font-size: 12px;
          color: #999;
          margin: 4px 0 0 0;
        }
      }

      .cert-no {
        font-family: monospace;
        font-size: 12px;
        color: #1890ff;
      }
    }

    .pagination {
      text-align: right;
      margin-top: 20px;
      padding-top: 15px;
      border-top: 1px solid #f0f0f0;
    }
  }

  .empty-state {
    text-align: center;
    padding: 60px 20px;
    background: white;
    border-radius: 4px;
    margin-top: 20px;

    i {
      font-size: 64px;
      color: #ddd;
      display: block;
      margin-bottom: 20px;
    }

    p {
      font-size: 14px;
      color: #999;
      margin: 10px 0;

      &.tip {
        font-size: 12px;
        margin-bottom: 20px;
      }
    }
  }
}
</style>
