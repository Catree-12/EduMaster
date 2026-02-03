<template>
  <div class="term-manage-container">
    <!-- 页面头部 -->
    <div class="page-header">
      <div class="title-section">
        <el-button icon="el-icon-arrow-left" type="text" @click="$router.back()" />
        <h1>班期管理</h1>
      </div>
      <p class="subtitle">管理课程的班期安排和学期信息</p>
    </div>

    <!-- 操作栏 -->
    <div class="operation-bar">
      <el-button type="primary" icon="el-icon-plus" @click="showAddTermDialog">
        新建班期
      </el-button>
    </div>

    <!-- 班期列表 -->
    <div class="term-list">
      <div v-for="term in terms" :key="term.id" class="term-card">
        <!-- 班期头部 -->
        <div class="term-header">
          <div class="term-info">
            <h3 class="term-name">{{ term.name }}</h3>
            <div class="term-meta">
              <span class="term-date">
                <i class="el-icon-date"></i>
                {{ term.startDate }} ~ {{ term.endDate }}
              </span>
              <el-tag 
                :type="getTermStatusType(term.status)" 
                size="small"
              >
                {{ getTermStatusText(term.status) }}
              </el-tag>
            </div>
          </div>
          <div class="term-actions">
            <el-button type="text" @click="editTerm(term)">
              <i class="el-icon-edit"></i> 编辑
            </el-button>
            <el-button type="text" @click="viewTermClasses(term)">
              <i class="el-icon-school"></i> 查看班级
            </el-button>
            <el-button type="text" style="color: #F56C6C;" @click="deleteTerm(term)">
              <i class="el-icon-delete"></i> 删除
            </el-button>
          </div>
        </div>

        <!-- 班期统计 -->
        <div class="term-stats">
          <div class="stat-item">
            <div class="stat-value">{{ getTermClasses(term.id).length }}</div>
            <div class="stat-label">班级数</div>
          </div>
          <div class="stat-item">
            <div class="stat-value">{{ getTermStudentCount(term.id) }}</div>
            <div class="stat-label">学生数</div>
          </div>
          <div class="stat-item">
            <div class="stat-value">{{ term.duration || '-' }}</div>
            <div class="stat-label">学时</div>
          </div>
        </div>

        <!-- 班期描述 -->
        <div v-if="term.description" class="term-description">
          {{ term.description }}
        </div>
      </div>

      <!-- 空状态 -->
      <div v-if="terms.length === 0" class="empty-state">
        <i class="el-icon-folder-opened"></i>
        <p>暂无班期信息</p>
        <el-button type="primary" @click="showAddTermDialog">创建第一个班期</el-button>
      </div>
    </div>

    <!-- 新建/编辑班期对话框 -->
    <el-dialog 
      :title="editingTerm ? '编辑班期' : '新建班期'" 
      :visible.sync="showTermDialog"
      width="500px"
    >
      <el-form :model="termForm" label-width="100px">
        <el-form-item label="班期名称">
          <el-input v-model="termForm.name" placeholder="如：2026春季学期" />
        </el-form-item>
        <el-form-item label="开始日期">
          <el-date-picker 
            v-model="termForm.startDate" 
            type="date" 
            placeholder="选择日期"
            value-format="yyyy-MM-dd"
            style="width: 100%;"
          />
        </el-form-item>
        <el-form-item label="结束日期">
          <el-date-picker 
            v-model="termForm.endDate" 
            type="date" 
            placeholder="选择日期"
            value-format="yyyy-MM-dd"
            style="width: 100%;"
          />
        </el-form-item>
        <el-form-item label="学时">
          <el-input-number 
            v-model="termForm.duration" 
            :min="1" 
            placeholder="总学时"
            style="width: 100%;"
          />
        </el-form-item>
        <el-form-item label="班期描述">
          <el-input 
            v-model="termForm.description" 
            type="textarea"
            :rows="3"
            placeholder="班期说明信息"
          />
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="showTermDialog = false">取消</el-button>
        <el-button type="primary" @click="submitTerm">确定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
export default {
  name: 'TermManage',
  data() {
    return {
      showTermDialog: false,
      editingTerm: null,
      termForm: {
        name: '',
        startDate: '',
        endDate: '',
        duration: null,
        description: ''
      },
      terms: [
        {
          id: 1,
          name: '2026春季学期',
          startDate: '2026-03-01',
          endDate: '2026-06-30',
          status: 'active', // active, upcoming, ended
          duration: 60,
          description: '2026年春季学期'
        },
        {
          id: 2,
          name: '2025秋季学期',
          startDate: '2025-09-01',
          endDate: '2025-12-31',
          status: 'ended',
          duration: 48,
          description: '2025年秋季学期'
        }
      ],
      classes: [
        {
          id: 1,
          termId: 1,
          name: '高一（1）班',
          studentCount: 48
        },
        {
          id: 2,
          termId: 1,
          name: '高一（2）班',
          studentCount: 45
        }
      ]
    }
  },
  methods: {
    showAddTermDialog() {
      this.editingTerm = null
      this.termForm = {
        name: '',
        startDate: '',
        endDate: '',
        duration: null,
        description: ''
      }
      this.showTermDialog = true
    },

    editTerm(term) {
      this.editingTerm = term
      this.termForm = {
        name: term.name,
        startDate: term.startDate,
        endDate: term.endDate,
        duration: term.duration,
        description: term.description
      }
      this.showTermDialog = true
    },

    submitTerm() {
      if (!this.termForm.name || !this.termForm.startDate || !this.termForm.endDate) {
        this.$message.error('请填写完整信息')
        return
      }

      if (this.editingTerm) {
        // 编辑
        Object.assign(this.editingTerm, this.termForm)
        this.$message.success('班期更新成功')
      } else {
        // 新增
        const newTerm = {
          id: Date.now(),
          ...this.termForm,
          status: 'upcoming'
        }
        this.terms.unshift(newTerm)
        this.$message.success('班期创建成功')
      }

      this.showTermDialog = false
      this.editingTerm = null
    },

    deleteTerm(term) {
      this.$confirm('确认删除该班期吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        const index = this.terms.findIndex(t => t.id === term.id)
        if (index > -1) {
          this.terms.splice(index, 1)
          this.$message.success('删除成功')
        }
      }).catch(() => {})
    },

    viewTermClasses(term) {
      this.$router.push({
        path: '/teacher/classes',
        query: { termId: term.id }
      })
    },

    getTermClasses(termId) {
      return this.classes.filter(c => c.termId === termId)
    },

    getTermStudentCount(termId) {
      return this.classes
        .filter(c => c.termId === termId)
        .reduce((sum, c) => sum + (c.studentCount || 0), 0)
    },

    getTermStatusText(status) {
      const map = {
        'active': '进行中',
        'upcoming': '未开始',
        'ended': '已结束'
      }
      return map[status] || status
    },

    getTermStatusType(status) {
      const map = {
        'active': 'success',
        'upcoming': 'info',
        'ended': 'info'
      }
      return map[status] || 'info'
    }
  }
}
</script>

<style scoped lang="scss">
.term-manage-container {
  padding: 20px;
  background: #f5f7fa;
  min-height: 100vh;
}

.page-header {
  margin-bottom: 30px;

  .title-section {
    display: flex;
    align-items: center;
    gap: 10px;

    h1 {
      margin: 0;
      font-size: 28px;
      color: #333;
      font-weight: bold;
    }
  }

  .subtitle {
    margin: 10px 0 0 0;
    color: #999;
    font-size: 14px;
  }
}

.operation-bar {
  margin-bottom: 20px;
}

.term-list {
  display: flex;
  flex-direction: column;
  gap: 20px;

  .term-card {
    border: 1px solid #E4E7ED;
    border-radius: 8px;
    padding: 20px;
    background: white;

    .term-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 16px;
      padding-bottom: 16px;
      border-bottom: 1px solid #E4E7ED;

      .term-info {
        .term-name {
          font-size: 18px;
          font-weight: 600;
          color: #303133;
          margin: 0 0 8px 0;
        }

        .term-meta {
          display: flex;
          align-items: center;
          gap: 12px;

          .term-date {
            color: #606266;
            font-size: 14px;

            i {
              margin-right: 4px;
            }
          }
        }
      }

      .term-actions {
        display: flex;
        gap: 8px;
      }
    }

    .term-stats {
      display: flex;
      gap: 40px;
      margin-bottom: 12px;

      .stat-item {
        text-align: center;

        .stat-value {
          font-size: 24px;
          font-weight: 600;
          color: #409EFF;
        }

        .stat-label {
          font-size: 13px;
          color: #909399;
          margin-top: 4px;
        }
      }
    }

    .term-description {
      color: #606266;
      font-size: 14px;
      line-height: 1.6;
    }
  }

  .empty-state {
    text-align: center;
    padding: 60px 20px;
    background: white;
    border-radius: 8px;

    i {
      font-size: 64px;
      color: #C0C4CC;
      margin-bottom: 16px;
    }

    p {
      color: #909399;
      font-size: 14px;
      margin-bottom: 20px;
    }
  }
}
</style>
