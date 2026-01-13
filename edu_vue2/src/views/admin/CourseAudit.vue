<template>
  <div class="course-audit-container">
    <div class="page-header">
      <h1>课程审核</h1>
      <p class="subtitle">管理员课程审核与批准</p>
    </div>

    <!-- 统计卡片 -->
    <div class="stats-row">
      <div class="stat-card">
        <div class="stat-number">{{ stats.pending }}</div>
        <div class="stat-label">待审核</div>
      </div>
      <div class="stat-card">
        <div class="stat-number">{{ stats.approved }}</div>
        <div class="stat-label">已批准</div>
      </div>
      <div class="stat-card">
        <div class="stat-number">{{ stats.rejected }}</div>
        <div class="stat-label">已拒绝</div>
      </div>
      <div class="stat-card">
        <div class="stat-number">{{ stats.total }}</div>
        <div class="stat-label">总计</div>
      </div>
    </div>

    <!-- 筛选和操作 -->
    <el-card shadow="hover" class="audit-wrapper">
      <div class="filters">
        <el-select
          v-model="filterStatus"
          placeholder="按状态筛选"
          style="width: 150px"
          clearable
        >
          <el-option label="待审核" value="pending" />
          <el-option label="已批准" value="approved" />
          <el-option label="已拒绝" value="rejected" />
        </el-select>

        <el-input
          v-model="searchKeyword"
          placeholder="搜索课程名称或讲师..."
          prefix-icon="el-icon-search"
          style="width: 250px; margin-left: 10px"
          clearable
        />

        <el-button
          type="primary"
          icon="el-icon-refresh"
          @click="fetchCourses"
          style="margin-left: 10px"
        >
          刷新
        </el-button>
      </div>

      <!-- 课程列表 -->
      <el-table
        :data="filteredCourses"
        style="width: 100%; margin-top: 20px"
        v-loading="loading"
      >
        <el-table-column prop="id" label="ID" width="80" />

        <el-table-column label="课程信息" width="280" class-name="course-info-col">
          <template slot-scope="scope">
            <div class="course-info">
              <img :src="scope.row.coverImage" :alt="scope.row.title" class="course-thumb" />
              <div class="course-details">
                <p class="course-title">{{ scope.row.title }}</p>
                <p class="course-instructor">讲师: {{ scope.row.instructor }}</p>
                <p class="course-category">分类: {{ getCategoryText(scope.row.category) }}</p>
              </div>
            </div>
          </template>
        </el-table-column>

        <el-table-column prop="description" label="描述" width="200">
          <template slot-scope="scope">
            <span>{{ scope.row.description | truncate(50) }}</span>
          </template>
        </el-table-column>

        <el-table-column prop="studentCount" label="学生数" width="80" />

        <el-table-column prop="price" label="价格" width="80">
          <template slot-scope="scope">
            ¥{{ scope.row.price }}
          </template>
        </el-table-column>

        <el-table-column prop="status" label="状态" width="100">
          <template slot-scope="scope">
            <el-tag :type="getStatusType(scope.row.status)">
              {{ getStatusText(scope.row.status) }}
            </el-tag>
          </template>
        </el-table-column>

        <el-table-column prop="submittedAt" label="提交时间" width="150">
          <template slot-scope="scope">
            {{ formatDate(scope.row.submittedAt) }}
          </template>
        </el-table-column>

        <el-table-column label="操作" width="150" fixed="right">
          <template slot-scope="scope">
            <el-button
              type="text"
              size="small"
              @click="viewCourseDetail(scope.row)"
            >
              查看详情
            </el-button>
            <el-button
              v-if="scope.row.status === 'pending'"
              type="text"
              size="small"
              @click="approveCourse(scope.row)"
            >
              批准
            </el-button>
            <el-button
              v-if="scope.row.status === 'pending'"
              type="text"
              size="small"
              @click="rejectCourse(scope.row)"
            >
              拒绝
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <el-pagination
        :current-page.sync="pagination.page"
        :page-size="pagination.pageSize"
        :total="total"
        layout="total, prev, pager, next"
        style="text-align: right; margin-top: 20px"
      />
    </el-card>

    <!-- 课程详情对话框 -->
    <el-dialog
      title="课程详情审核"
      :visible.sync="detailDialogVisible"
      width="70%"
      @close="handleDetailDialogClose"
    >
      <div v-if="selectedCourse" class="course-detail">
        <el-row :gutter="20">
          <el-col :span="8">
            <img :src="selectedCourse.coverImage" :alt="selectedCourse.title" class="detail-thumb" />
          </el-col>
          <el-col :span="16">
            <h3>{{ selectedCourse.title }}</h3>
            <p><strong>讲师:</strong> {{ selectedCourse.instructor }}</p>
            <p><strong>分类:</strong> {{ getCategoryText(selectedCourse.category) }}</p>
            <p><strong>价格:</strong> ¥{{ selectedCourse.price }}</p>
            <p><strong>状态:</strong>
              <el-tag :type="getStatusType(selectedCourse.status)">
                {{ getStatusText(selectedCourse.status) }}
              </el-tag>
            </p>
            <p><strong>学生数:</strong> {{ selectedCourse.studentCount }}</p>
            <p><strong>课时数:</strong> {{ selectedCourse.lessonCount }}</p>
            <p><strong>难度:</strong> {{ getLevelText(selectedCourse.level) }}</p>
            <p><strong>学习周期:</strong> {{ selectedCourse.duration }} 周</p>
            <p><strong>提交时间:</strong> {{ formatDate(selectedCourse.submittedAt) }}</p>
          </el-col>
        </el-row>

        <el-divider />

        <h4>课程描述</h4>
        <p>{{ selectedCourse.description }}</p>

        <h4>学习目标</h4>
        <p>{{ selectedCourse.objectives }}</p>

        <h4>前置要求</h4>
        <p>{{ selectedCourse.prerequisites }}</p>

        <!-- 审核意见 -->
        <div v-if="selectedCourse.status !== 'pending'" class="review-info">
          <el-divider />
          <h4>审核意见</h4>
          <p class="review-comment">{{ selectedCourse.reviewComment }}</p>
          <p v-if="selectedCourse.reviewedAt"><strong>审核时间:</strong> {{ formatDate(selectedCourse.reviewedAt) }}</p>
          <p v-if="selectedCourse.reviewer"><strong>审核人:</strong> {{ selectedCourse.reviewer }}</p>
        </div>
      </div>

      <!-- 审核操作 -->
      <div v-if="selectedCourse && selectedCourse.status === 'pending'" class="dialog-footer">
        <el-form
          :model="auditForm"
          label-width="100px"
          size="small"
        >
          <el-form-item label="审核意见" prop="comment">
            <el-input
              v-model="auditForm.comment"
              type="textarea"
              rows="4"
              placeholder="请输入审核意见（可选）"
            />
          </el-form-item>
        </el-form>

        <div style="text-align: right; margin-top: 20px">
          <el-button @click="detailDialogVisible = false">关闭</el-button>
          <el-button
            type="success"
            :loading="auditSubmitting"
            @click="confirmApprove"
          >
            批准课程
          </el-button>
          <el-button
            type="danger"
            :loading="auditSubmitting"
            @click="confirmReject"
          >
            拒绝课程
          </el-button>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script>
export default {
  name: 'CourseAudit',
  filters: {
    truncate(text, length) {
      if (text && text.length > length) {
        return text.substring(0, length) + '...'
      }
      return text
    }
  },
  data() {
    return {
      loading: false,
      auditSubmitting: false,
      filterStatus: '',
      searchKeyword: '',
      detailDialogVisible: false,
      selectedCourse: null,
      auditAction: null, // 'approve' 或 'reject'
      auditForm: {
        comment: ''
      },
      pagination: {
        page: 1,
        pageSize: 10
      },
      total: 0,
      stats: {
        pending: 0,
        approved: 0,
        rejected: 0,
        total: 0
      },
      courses: [
        {
          id: '1',
          title: 'Vue.js 全栈开发',
          description: '掌握 Vue.js 框架，学习现代前端开发技术',
          category: 'web',
          price: 599,
          instructor: '张老师',
          studentCount: 125,
          lessonCount: 48,
          level: 'intermediate',
          duration: 12,
          coverImage: 'https://via.placeholder.com/300x200?text=Vue.js',
          objectives: '学生将学会使用Vue.js开发单页应用，掌握组件化开发...',
          prerequisites: '熟悉JavaScript基础语法',
          status: 'pending',
          submittedAt: '2024-11-14T10:30:00',
          reviewComment: '',
          reviewedAt: null,
          reviewer: null
        },
        {
          id: '2',
          title: 'React 开发实战',
          description: '深入学习 React，打造高性能前端应用',
          category: 'web',
          price: 699,
          instructor: '李老师',
          studentCount: 98,
          lessonCount: 42,
          level: 'intermediate',
          duration: 10,
          coverImage: 'https://via.placeholder.com/300x200?text=React',
          objectives: '掌握React的核心概念和最佳实践...',
          prerequisites: '了解JavaScript基础',
          status: 'pending',
          submittedAt: '2024-11-13T14:20:00',
          reviewComment: '',
          reviewedAt: null,
          reviewer: null
        },
        {
          id: '3',
          title: 'Python 数据科学',
          description: '学习 Python 进行数据分析和机器学习',
          category: 'data',
          price: 799,
          instructor: '王老师',
          studentCount: 234,
          lessonCount: 56,
          level: 'advanced',
          duration: 16,
          coverImage: 'https://via.placeholder.com/300x200?text=Python',
          objectives: '掌握数据分析和机器学习技能...',
          prerequisites: '需要 Python 基础和数学基础',
          status: 'approved',
          submittedAt: '2024-11-10T09:00:00',
          reviewComment: '课程质量优秀，已批准',
          reviewedAt: '2024-11-12T16:45:00',
          reviewer: '管理员张三'
        },
        {
          id: '4',
          title: 'Node.js 后端开发',
          description: '构建高效的 Node.js 后端服务',
          category: 'backend',
          price: 649,
          instructor: '周老师',
          studentCount: 87,
          lessonCount: 38,
          level: 'beginner',
          duration: 8,
          coverImage: 'https://via.placeholder.com/300x200?text=Node.js',
          objectives: '学会使用Node.js进行服务器开发...',
          prerequisites: '熟悉JavaScript',
          status: 'rejected',
          submittedAt: '2024-11-08T11:30:00',
          reviewComment: '课程内容需要进一步完善，建议补充案例项目',
          reviewedAt: '2024-11-11T10:15:00',
          reviewer: '管理员李四'
        }
      ]
    }
  },

  computed: {
    filteredCourses() {
      return this.courses.filter(course => {
        const matchStatus = !this.filterStatus || course.status === this.filterStatus
        const matchKeyword = !this.searchKeyword || 
          course.title.includes(this.searchKeyword) || 
          course.instructor.includes(this.searchKeyword)
        return matchStatus && matchKeyword
      })
    }
  },

  created() {
    this.fetchCourses()
  },

  methods: {
    fetchCourses() {
      this.loading = true
      // 模拟API调用
      setTimeout(() => {
        // 计算统计数据
        this.stats = {
          pending: this.courses.filter(c => c.status === 'pending').length,
          approved: this.courses.filter(c => c.status === 'approved').length,
          rejected: this.courses.filter(c => c.status === 'rejected').length,
          total: this.courses.length
        }
        this.total = this.filteredCourses.length
        this.loading = false
      }, 500)
    },

    viewCourseDetail(course) {
      this.selectedCourse = JSON.parse(JSON.stringify(course))
      this.auditForm.comment = ''
      this.auditAction = null
      this.detailDialogVisible = true
    },

    approveCourse(course) {
      this.selectedCourse = JSON.parse(JSON.stringify(course))
      this.auditForm.comment = ''
      this.auditAction = 'approve'
      this.detailDialogVisible = true
    },

    rejectCourse(course) {
      this.selectedCourse = JSON.parse(JSON.stringify(course))
      this.auditForm.comment = ''
      this.auditAction = 'reject'
      this.detailDialogVisible = true
    },

    confirmApprove() {
      if (!this.selectedCourse) return

      this.auditSubmitting = true
      // 模拟API调用
      setTimeout(() => {
        const index = this.courses.findIndex(c => c.id === this.selectedCourse.id)
        if (index > -1) {
          this.courses[index].status = 'approved'
          this.courses[index].reviewComment = this.auditForm.comment || '已批准'
          this.courses[index].reviewedAt = new Date().toISOString()
          this.courses[index].reviewer = '当前管理员'
        }
        this.$message.success('课程已批准')
        this.detailDialogVisible = false
        this.auditSubmitting = false
        this.fetchCourses()
      }, 800)
    },

    confirmReject() {
      if (!this.selectedCourse) return

      if (!this.auditForm.comment.trim()) {
        this.$message.warning('请输入拒绝原因')
        return
      }

      this.auditSubmitting = true
      // 模拟API调用
      setTimeout(() => {
        const index = this.courses.findIndex(c => c.id === this.selectedCourse.id)
        if (index > -1) {
          this.courses[index].status = 'rejected'
          this.courses[index].reviewComment = this.auditForm.comment
          this.courses[index].reviewedAt = new Date().toISOString()
          this.courses[index].reviewer = '当前管理员'
        }
        this.$message.success('课程已拒绝')
        this.detailDialogVisible = false
        this.auditSubmitting = false
        this.fetchCourses()
      }, 800)
    },

    handleDetailDialogClose() {
      this.selectedCourse = null
      this.auditForm.comment = ''
      this.auditAction = null
    },

    getCategoryText(category) {
      const texts = {
        'web': 'Web 前端',
        'backend': '后端开发',
        'mobile': '移动开发',
        'data': '数据科学',
        'devops': 'DevOps',
        'other': '其他'
      }
      return texts[category] || category
    },

    getStatusType(status) {
      const types = {
        'pending': 'warning',
        'approved': 'success',
        'rejected': 'danger',
        'draft': 'info'
      }
      return types[status] || 'info'
    },

    getStatusText(status) {
      const texts = {
        'pending': '待审核',
        'approved': '已批准',
        'rejected': '已拒绝',
        'draft': '草稿'
      }
      return texts[status] || status
    },

    getLevelText(level) {
      const texts = {
        'beginner': '入门',
        'intermediate': '中级',
        'advanced': '高级',
        'expert': '专家'
      }
      return texts[level] || level
    },

    formatDate(dateStr) {
      if (!dateStr) return '-'
      const date = new Date(dateStr)
      return date.toLocaleDateString('zh-CN') + ' ' + date.toLocaleTimeString('zh-CN')
    }
  }
}
</script>

<style scoped lang="scss">
.course-audit-container {
  padding: 20px;
  background: #f5f7fa;
  min-height: 100vh;
}

.page-header {
  margin-bottom: 30px;

  h1 {
    margin: 0 0 10px 0;
    font-size: 28px;
    color: #333;
  }

  .subtitle {
    margin: 0;
    font-size: 14px;
    color: #999;
  }
}

.stats-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 30px;

  .stat-card {
    background: white;
    border-radius: 8px;
    padding: 20px;
    text-align: center;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    transition: all 0.3s;

    &:hover {
      transform: translateY(-5px);
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    }

    .stat-number {
      font-size: 32px;
      font-weight: bold;
      color: #3498db;
      margin-bottom: 10px;
    }

    .stat-label {
      font-size: 14px;
      color: #999;
    }
  }
}

.audit-wrapper {
  background: white;

  .filters {
    display: flex;
    gap: 10px;
    align-items: center;
    margin-bottom: 20px;
  }

  ::v-deep .el-table {
    .course-info-col {
      padding: 0 !important;
    }

    .course-info {
      display: flex;
      gap: 15px;
      padding: 10px;
      align-items: center;

      .course-thumb {
        width: 60px;
        height: 60px;
        border-radius: 4px;
        object-fit: cover;
      }

      .course-details {
        flex: 1;

        p {
          margin: 2px 0;
          font-size: 12px;
        }

        .course-title {
          font-size: 14px;
          font-weight: bold;
          color: #333;
        }

        .course-instructor,
        .course-category {
          color: #999;
        }
      }
    }
  }
}

.course-detail {
  .detail-thumb {
    width: 100%;
    height: auto;
    border-radius: 4px;
    margin-bottom: 20px;
  }

  h3 {
    font-size: 20px;
    color: #333;
    margin-bottom: 15px;
    font-weight: bold;
  }

  h4 {
    font-size: 14px;
    color: #333;
    margin-top: 15px;
    margin-bottom: 10px;
    font-weight: bold;
    border-bottom: 2px solid #f0f0f0;
    padding-bottom: 8px;
  }

  p {
    margin: 10px 0;
    color: #666;
    font-size: 13px;
    line-height: 1.6;
  }

  .review-info {
    background: #f5f7fa;
    padding: 15px;
    border-radius: 4px;
    margin-top: 15px;

    .review-comment {
      background: white;
      padding: 10px;
      border-left: 3px solid #3498db;
      margin: 10px 0;
      font-style: italic;
      color: #555;
    }
  }
}

.dialog-footer {
  margin-top: 30px;
  padding-top: 20px;
  border-top: 1px solid #f0f0f0;
}
</style>
