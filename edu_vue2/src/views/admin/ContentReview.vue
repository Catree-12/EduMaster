<template>
  <div class="content-review">
    <div class="page-header">
      <h1>内容审核</h1>
      <p class="subtitle">处理用户举报的违规内容</p>
    </div>

    <!-- 统计卡片 -->
    <el-row :gutter="20" class="stats-row">
      <el-col :span="6">
        <el-card class="stat-card pending">
          <div class="stat-content">
            <i class="el-icon-warning"></i>
            <div>
              <div class="stat-value">{{ statistics.pending }}</div>
              <div class="stat-label">待处理</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card handled">
          <div class="stat-content">
            <i class="el-icon-success"></i>
            <div>
              <div class="stat-value">{{ statistics.handled }}</div>
              <div class="stat-label">已处理</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card deleted">
          <div class="stat-content">
            <i class="el-icon-delete"></i>
            <div>
              <div class="stat-value">{{ statistics.deleted }}</div>
              <div class="stat-label">已删除</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card rejected">
          <div class="stat-content">
            <i class="el-icon-close"></i>
            <div>
              <div class="stat-value">{{ statistics.rejected }}</div>
              <div class="stat-label">举报驳回</div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 筛选 -->
    <el-card class="filter-card">
      <el-form :inline="true" :model="filters">
        <el-form-item label="内容类型">
          <el-select v-model="filters.type" placeholder="全部类型" clearable>
            <el-option label="帖子" value="post"></el-option>
            <el-option label="评论" value="comment"></el-option>
            <el-option label="课程" value="course"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="处理状态">
          <el-select v-model="filters.status" placeholder="全部状态" clearable>
            <el-option label="待处理" value="pending"></el-option>
            <el-option label="已处理" value="handled"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" icon="el-icon-search">搜索</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 举报列表 -->
    <el-card>
      <el-table :data="reports" v-loading="loading">
        <el-table-column prop="id" label="ID" width="80"></el-table-column>
        <el-table-column label="内容类型" width="100">
          <template slot-scope="scope">
            <el-tag size="small">{{ getTypeLabel(scope.row.type) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="content" label="被举报内容" min-width="250"></el-table-column>
        <el-table-column prop="reason" label="举报理由" width="150"></el-table-column>
        <el-table-column prop="reporter" label="举报人" width="120"></el-table-column>
        <el-table-column label="举报时间" width="180">
          <template slot-scope="scope">
            {{ formatDate(scope.row.reportTime) }}
          </template>
        </el-table-column>
        <el-table-column label="状态" width="100">
          <template slot-scope="scope">
            <el-tag :type="getStatusType(scope.row.status)" size="small">
              {{ getStatusLabel(scope.row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" fixed="right">
          <template slot-scope="scope">
            <el-button 
              v-if="scope.row.status === 'pending'"
              type="text" 
              size="small"
              @click="handleView(scope.row)">
              查看详情
            </el-button>
            <el-button 
              v-if="scope.row.status === 'pending'"
              type="text" 
              size="small"
              @click="handleDelete(scope.row)">
              删除内容
            </el-button>
            <el-button 
              v-if="scope.row.status === 'pending'"
              type="text" 
              size="small"
              @click="handleReject(scope.row)">
              驳回举报
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
  </div>
</template>

<script>
export default {
  name: 'ContentReview',
  data() {
    return {
      loading: false,
      statistics: {
        pending: 8,
        handled: 45,
        deleted: 23,
        rejected: 22
      },
      filters: {
        type: '',
        status: ''
      },
      reports: [],
      pagination: {
        page: 1,
        pageSize: 10,
        total: 0
      }
    }
  },
  mounted() {
    this.fetchReports()
  },
  methods: {
    fetchReports() {
      this.loading = true
      // TODO: 调用API获取举报列表
      setTimeout(() => {
        this.reports = this.getMockReports()
        this.pagination.total = 53
        this.loading = false
      }, 500)
    },
    handleView() {
      this.$message.info('查看详情')
    },
    handleDelete() {
      this.$confirm('确认删除该内容？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.$message.success('内容已删除')
        this.fetchReports()
      })
    },
    handleReject() {
      this.$confirm('确认驳回该举报？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消'
      }).then(() => {
        this.$message.success('举报已驳回')
        this.fetchReports()
      })
    },
    handlePageChange(page) {
      this.pagination.page = page
      this.fetchReports()
    },
    getTypeLabel(type) {
      const map = { post: '帖子', comment: '评论', course: '课程' }
      return map[type] || type
    },
    getStatusLabel(status) {
      const map = { pending: '待处理', handled: '已处理' }
      return map[status] || status
    },
    getStatusType(status) {
      return status === 'pending' ? 'warning' : 'success'
    },
    formatDate(date) {
      return new Date(date).toLocaleString('zh-CN')
    },
    getMockReports() {
      return Array.from({ length: 10 }, (_, i) => ({
        id: 2000 + i,
        type: ['post', 'comment', 'course'][i % 3],
        content: `这是被举报的内容 ${i + 1}，可能包含不当言论或违规信息...`,
        reason: ['垃圾广告', '不当言论', '侵权内容'][i % 3],
        reporter: `用户${i + 1}`,
        reportTime: new Date(Date.now() - Math.random() * 7 * 24 * 60 * 60 * 1000).toISOString(),
        status: i % 4 === 0 ? 'pending' : 'handled'
      }))
    }
  }
}
</script>

<style scoped>
.content-review {
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
  border-left: 4px solid;
}

.stat-card.pending {
  border-left-color: #E6A23C;
}

.stat-card.handled {
  border-left-color: #67C23A;
}

.stat-card.deleted {
  border-left-color: #F56C6C;
}

.stat-card.rejected {
  border-left-color: #909399;
}

.stat-content {
  display: flex;
  align-items: center;
  gap: 15px;
}

.stat-content i {
  font-size: 36px;
}

.stat-card.pending i { color: #E6A23C; }
.stat-card.handled i { color: #67C23A; }
.stat-card.deleted i { color: #F56C6C; }
.stat-card.rejected i { color: #909399; }

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

.pagination-container {
  margin-top: 20px;
  text-align: right;
}
</style>
