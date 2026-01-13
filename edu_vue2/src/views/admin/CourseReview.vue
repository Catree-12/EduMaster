<template>
  <div class="course-review-container">
    <div class="header">
      <h1>课程审核</h1>
      <div class="filter-group">
        <select v-model="filterStatus" class="filter-select">
          <option value="">全部状态</option>
          <option value="pending">待审核</option>
          <option value="approved">已通过</option>
          <option value="rejected">已拒绝</option>
        </select>
      </div>
    </div>

    <div class="review-table">
      <table>
        <thead>
          <tr>
            <th>课程名称</th>
            <th>讲师</th>
            <th>分类</th>
            <th>提交时间</th>
            <th>状态</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in filteredCourses" :key="item.id">
            <td>{{ item.title }}</td>
            <td>{{ item.instructor }}</td>
            <td>{{ item.category }}</td>
            <td>{{ item.submittedAt }}</td>
            <td>
              <span :class="`status-badge status-${item.status}`">
                {{ getStatusText(item.status) }}
              </span>
            </td>
            <td class="action-cell">
              <button @click="viewDetail(item.id)" class="btn-view">查看详情</button>
              <button 
                v-if="item.status === 'pending'"
                @click="approveCourse(item.id)" 
                class="btn-approve"
              >
                通过
              </button>
              <button 
                v-if="item.status === 'pending'"
                @click="rejectCourse(item.id)" 
                class="btn-reject"
              >
                拒绝
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- 课程详情弹窗 -->
    <div v-if="selectedCourse" class="modal-overlay" @click="selectedCourse = null">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h2>{{ selectedCourse.title }}</h2>
          <button class="btn-close" @click="selectedCourse = null">✕</button>
        </div>
        <div class="modal-body">
          <div class="detail-section">
            <h3>基本信息</h3>
            <div class="detail-grid">
              <div class="detail-item">
                <label>讲师</label>
                <p>{{ selectedCourse.instructor }}</p>
              </div>
              <div class="detail-item">
                <label>分类</label>
                <p>{{ selectedCourse.category }}</p>
              </div>
              <div class="detail-item">
                <label>难度</label>
                <p>{{ selectedCourse.level }}</p>
              </div>
              <div class="detail-item">
                <label>价格</label>
                <p>¥{{ selectedCourse.price }}</p>
              </div>
            </div>
          </div>

          <div class="detail-section">
            <h3>课程描述</h3>
            <p>{{ selectedCourse.description }}</p>
          </div>

          <div class="detail-section">
            <h3>审核意见</h3>
            <textarea 
              v-model="reviewComment" 
              placeholder="输入审核意见"
              rows="4"
              class="review-textarea"
            ></textarea>
          </div>

          <div v-if="selectedCourse.status === 'rejected'" class="detail-section">
            <h3>拒绝原因</h3>
            <p class="rejection-reason">{{ selectedCourse.rejectionReason }}</p>
          </div>
        </div>

        <div class="modal-footer">
          <button class="btn-cancel" @click="selectedCourse = null">关闭</button>
          <button 
            v-if="selectedCourse.status === 'pending'"
            class="btn-reject-modal" 
            @click="submitReject"
          >
            拒绝
          </button>
          <button 
            v-if="selectedCourse.status === 'pending'"
            class="btn-approve-modal" 
            @click="submitApprove"
          >
            通过审核
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'CourseReview',
  data() {
    return {
      filterStatus: '',
      reviewComment: '',
      selectedCourse: null,
      courses: [
        {
          id: 1,
          title: 'Python 机器学习完全指南',
          instructor: '王五',
          category: '编程',
          level: '高级',
          price: 299,
          submittedAt: '2024-01-15',
          status: 'pending',
          description: '深入学习 Python 机器学习库，掌握各种机器学习算法的实现和应用。',
          rejectionReason: ''
        },
        {
          id: 2,
          title: 'UI/UX 设计基础',
          instructor: '李六',
          category: '设计',
          level: '初级',
          price: 199,
          submittedAt: '2024-01-12',
          status: 'pending',
          description: '从零开始学习现代 UI/UX 设计的基本原理和实践方法。',
          rejectionReason: ''
        },
        {
          id: 3,
          title: 'JavaScript 高级应用',
          instructor: '张三',
          category: '编程',
          level: '高级',
          price: 249,
          submittedAt: '2024-01-10',
          status: 'approved',
          description: '深入学习 JavaScript 的高级特性，包括闭包、原型链、异步编程等。',
          rejectionReason: ''
        },
        {
          id: 4,
          title: 'Web 开发最佳实践',
          instructor: '赵四',
          category: '编程',
          level: '中级',
          price: 199,
          submittedAt: '2024-01-08',
          status: 'rejected',
          description: '学习现代 Web 开发的最佳实践和常见模式。',
          rejectionReason: '课程内容与已有课程重复较多，建议增加独特内容后重新提交。'
        },
        {
          id: 5,
          title: 'React 17 完全开发手册',
          instructor: '刘七',
          category: '编程',
          level: '中级',
          price: 249,
          submittedAt: '2024-01-20',
          status: 'pending',
          description: '全面学习 React 17 的新特性和最佳实践，包括 Hooks 和 Suspense。',
          rejectionReason: ''
        }
      ]
    }
  },
  computed: {
    filteredCourses() {
      if (!this.filterStatus) {
        return this.courses
      }
      return this.courses.filter(course => course.status === this.filterStatus)
    }
  },
  methods: {
    getStatusText(status) {
      const statusMap = {
        'pending': '待审核',
        'approved': '已通过',
        'rejected': '已拒绝'
      }
      return statusMap[status] || status
    },
    viewDetail(courseId) {
      this.selectedCourse = this.courses.find(c => c.id === courseId)
      this.reviewComment = ''
    },
    approveCourse(courseId) {
      const course = this.courses.find(c => c.id === courseId)
      if (course) {
        this.$set(course, 'status', 'approved')
        alert('课程已通过审核')
      }
    },
    rejectCourse(courseId) {
      this.selectedCourse = this.courses.find(c => c.id === courseId)
    },
    submitApprove() {
      if (this.selectedCourse) {
        this.$set(this.selectedCourse, 'status', 'approved')
        alert('课程已通过审核')
        this.selectedCourse = null
      }
    },
    submitReject() {
      if (this.reviewComment.trim()) {
        if (this.selectedCourse) {
          this.$set(this.selectedCourse, 'status', 'rejected')
          this.$set(this.selectedCourse, 'rejectionReason', this.reviewComment)
          alert('课程已拒绝')
          this.selectedCourse = null
        }
      } else {
        alert('请输入拒绝原因')
      }
    }
  }
}
</script>

<style scoped>
.course-review-container {
  padding: 30px;
  background: #f5f5f5;
  min-height: 100vh;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

.header h1 {
  font-size: 28px;
  color: #333;
  margin: 0;
}

.filter-group {
  display: flex;
  gap: 15px;
}

.filter-select {
  padding: 10px 15px;
  border: 1px solid #ddd;
  border-radius: 4px;
  background: white;
  cursor: pointer;
  font-size: 14px;
}

.review-table {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

table {
  width: 100%;
  border-collapse: collapse;
}

thead {
  background: #f9f9f9;
  border-bottom: 2px solid #eee;
}

th {
  padding: 15px;
  text-align: left;
  font-weight: 600;
  color: #555;
  font-size: 14px;
}

tbody tr {
  border-bottom: 1px solid #eee;
  transition: background 0.3s;
}

tbody tr:hover {
  background: #f9f9f9;
}

td {
  padding: 15px;
  font-size: 14px;
  color: #555;
}

.status-badge {
  display: inline-block;
  padding: 6px 12px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 600;
}

.status-pending {
  background: #fff3cd;
  color: #856404;
}

.status-approved {
  background: #d4edda;
  color: #155724;
}

.status-rejected {
  background: #f8d7da;
  color: #721c24;
}

.action-cell {
  display: flex;
  gap: 10px;
}

.btn-view,
.btn-approve,
.btn-reject {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-view {
  background: #e3f2fd;
  color: #1976d2;
}

.btn-view:hover {
  background: #1976d2;
  color: white;
}

.btn-approve {
  background: #d4edda;
  color: #155724;
}

.btn-approve:hover {
  background: #155724;
  color: white;
}

.btn-reject {
  background: #f8d7da;
  color: #721c24;
}

.btn-reject:hover {
  background: #721c24;
  color: white;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 8px;
  max-width: 600px;
  width: 90%;
  max-height: 80vh;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  border-bottom: 1px solid #eee;
}

.modal-header h2 {
  margin: 0;
  font-size: 20px;
  color: #333;
}

.btn-close {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #999;
  transition: color 0.3s;
}

.btn-close:hover {
  color: #333;
}

.modal-body {
  padding: 20px;
}

.detail-section {
  margin-bottom: 25px;
  padding-bottom: 20px;
  border-bottom: 1px solid #eee;
}

.detail-section:last-child {
  border-bottom: none;
  margin-bottom: 0;
  padding-bottom: 0;
}

.detail-section h3 {
  margin: 0 0 15px;
  font-size: 16px;
  color: #333;
}

.detail-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 15px;
}

.detail-item label {
  display: block;
  color: #999;
  font-size: 12px;
  margin-bottom: 5px;
}

.detail-item p {
  margin: 0;
  color: #333;
  font-weight: 500;
}

.review-textarea {
  width: 100%;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-family: inherit;
  font-size: 14px;
  resize: vertical;
  transition: border-color 0.3s;
}

.review-textarea:focus {
  outline: none;
  border-color: #667eea;
}

.rejection-reason {
  margin: 0;
  color: #c62828;
  padding: 12px;
  background: #ffebee;
  border-radius: 4px;
}

.modal-footer {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
  padding: 20px;
  border-top: 1px solid #eee;
}

.btn-cancel,
.btn-reject-modal,
.btn-approve-modal {
  padding: 10px 24px;
  border: none;
  border-radius: 4px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-cancel {
  background: #f0f0f0;
  color: #333;
}

.btn-cancel:hover {
  background: #e0e0e0;
}

.btn-reject-modal {
  background: #f8d7da;
  color: #721c24;
}

.btn-reject-modal:hover {
  background: #721c24;
  color: white;
}

.btn-approve-modal {
  background: #d4edda;
  color: #155724;
}

.btn-approve-modal:hover {
  background: #155724;
  color: white;
}
</style>
