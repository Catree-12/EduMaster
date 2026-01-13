<template>
  <div class="user-management">
    <!-- 页面标题 -->
    <div class="page-header">
      <h1>用户管理</h1>
      <p class="subtitle">查看和管理平台用户</p>
    </div>

    <!-- 统计卡片 -->
    <el-row :gutter="20" class="stats-row">
      <el-col :span="6">
        <el-card class="stat-card total">
          <div class="stat-content">
            <i class="el-icon-user"></i>
            <div>
              <div class="stat-value">{{ statistics.total }}</div>
              <div class="stat-label">总用户数</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card active">
          <div class="stat-content">
            <i class="el-icon-success"></i>
            <div>
              <div class="stat-value">{{ statistics.active }}</div>
              <div class="stat-label">活跃用户</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card disabled">
          <div class="stat-content">
            <i class="el-icon-warning"></i>
            <div>
              <div class="stat-value">{{ statistics.disabled }}</div>
              <div class="stat-label">已禁用</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card newToday">
          <div class="stat-content">
            <i class="el-icon-plus"></i>
            <div>
              <div class="stat-value">{{ statistics.newToday }}</div>
              <div class="stat-label">今日新增</div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 搜索和筛选 -->
    <el-card class="filter-card">
      <el-form :inline="true" :model="filters" class="filter-form">
        <el-form-item label="用户状态">
          <el-select v-model="filters.status" placeholder="全部状态" clearable @change="fetchUsers">
            <el-option label="活跃" value="active"></el-option>
            <el-option label="已禁用" value="disabled"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="用户类型">
          <el-select v-model="filters.role" placeholder="全部类型" clearable @change="fetchUsers">
            <el-option label="普通用户" value="user"></el-option>
            <el-option label="管理员" value="admin"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="搜索">
          <el-input 
            v-model="filters.keyword" 
            placeholder="姓名/邮箱/ID" 
            clearable
            @keyup.enter.native="fetchUsers"
            style="width: 250px;">
            <el-button slot="append" icon="el-icon-search" @click="fetchUsers"></el-button>
          </el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" icon="el-icon-download" @click="exportUsers">导出数据</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 用户列表 -->
    <el-card class="user-list-card">
      <div slot="header" class="card-header">
        <span>用户列表</span>
        <el-button type="text" @click="fetchUsers">
          <i class="el-icon-refresh"></i> 刷新
        </el-button>
      </div>

      <el-table
        :data="users"
        v-loading="loading"
        style="width: 100%"
        @selection-change="handleSelectionChange">
        <el-table-column type="selection" width="55"></el-table-column>
        <el-table-column prop="id" label="ID" width="80"></el-table-column>
        <el-table-column label="用户信息" min-width="250">
          <template slot-scope="scope">
            <div class="user-info">
              <el-avatar :src="scope.row.avatar" :size="40">
                {{ scope.row.name.charAt(0) }}
              </el-avatar>
              <div class="user-details">
                <div class="user-name">
                  {{ scope.row.name }}
                  <el-tag v-if="scope.row.role === 'admin'" type="danger" size="mini">管理员</el-tag>
                </div>
                <div class="user-email">{{ scope.row.email }}</div>
              </div>
            </div>
          </template>
        </el-table-column>
        <el-table-column label="创建课程" width="100" align="center">
          <template slot-scope="scope">
            {{ scope.row.courseCount || 0 }}
          </template>
        </el-table-column>
        <el-table-column label="学习课程" width="100" align="center">
          <template slot-scope="scope">
            {{ scope.row.enrolledCount || 0 }}
          </template>
        </el-table-column>
        <el-table-column label="注册时间" width="180">
          <template slot-scope="scope">
            {{ formatDate(scope.row.createdAt) }}
          </template>
        </el-table-column>
        <el-table-column label="最后登录" width="180">
          <template slot-scope="scope">
            {{ formatDate(scope.row.lastLoginAt) }}
          </template>
        </el-table-column>
        <el-table-column label="状态" width="100">
          <template slot-scope="scope">
            <el-tag 
              :type="scope.row.status === 'active' ? 'success' : 'danger'"
              size="small">
              {{ scope.row.status === 'active' ? '活跃' : '已禁用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="220" fixed="right">
          <template slot-scope="scope">
            <el-button 
              type="text" 
              size="small"
              @click="handleViewUser(scope.row)">
              <i class="el-icon-view"></i> 查看
            </el-button>
            <el-button 
              type="text" 
              size="small"
              @click="handleEditUser(scope.row)">
              <i class="el-icon-edit"></i> 编辑
            </el-button>
            <el-button 
              v-if="scope.row.status === 'active' && scope.row.role !== 'admin'"
              type="text" 
              size="small"
              @click="handleDisableUser(scope.row)">
              <i class="el-icon-lock"></i> 禁用
            </el-button>
            <el-button 
              v-if="scope.row.status === 'disabled'"
              type="text" 
              size="small"
              @click="handleEnableUser(scope.row)">
              <i class="el-icon-unlock"></i> 启用
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 批量操作 -->
      <div v-if="selectedUsers.length > 0" class="batch-actions">
        <span>已选择 {{ selectedUsers.length }} 个用户</span>
        <el-button type="danger" size="small" @click="handleBatchDisable">批量禁用</el-button>
        <el-button type="success" size="small" @click="handleBatchEnable">批量启用</el-button>
      </div>

      <!-- 分页 -->
      <div class="pagination-container">
        <el-pagination
          @size-change="handleSizeChange"
          @current-change="handlePageChange"
          :current-page="pagination.page"
          :page-sizes="[10, 20, 50, 100]"
          :page-size="pagination.pageSize"
          :total="pagination.total"
          layout="total, sizes, prev, pager, next, jumper">
        </el-pagination>
      </div>
    </el-card>

    <!-- 用户详情对话框 -->
    <el-dialog
      title="用户详情"
      :visible.sync="detailDialog.visible"
      width="600px">
      <div v-if="detailDialog.user">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="用户ID">
            {{ detailDialog.user.id }}
          </el-descriptions-item>
          <el-descriptions-item label="用户名">
            {{ detailDialog.user.name }}
          </el-descriptions-item>
          <el-descriptions-item label="邮箱" :span="2">
            {{ detailDialog.user.email }}
          </el-descriptions-item>
          <el-descriptions-item label="手机号码" :span="2">
            {{ detailDialog.user.phone || '未绑定' }}
          </el-descriptions-item>
          <el-descriptions-item label="用户类型">
            <el-tag :type="detailDialog.user.role === 'admin' ? 'danger' : 'primary'" size="small">
              {{ detailDialog.user.role === 'admin' ? '管理员' : '普通用户' }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="账户状态">
            <el-tag :type="detailDialog.user.status === 'active' ? 'success' : 'danger'" size="small">
              {{ detailDialog.user.status === 'active' ? '活跃' : '已禁用' }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="创建课程数">
            {{ detailDialog.user.courseCount || 0 }}
          </el-descriptions-item>
          <el-descriptions-item label="学习课程数">
            {{ detailDialog.user.enrolledCount || 0 }}
          </el-descriptions-item>
          <el-descriptions-item label="注册时间" :span="2">
            {{ formatDate(detailDialog.user.createdAt) }}
          </el-descriptions-item>
          <el-descriptions-item label="最后登录" :span="2">
            {{ formatDate(detailDialog.user.lastLoginAt) }}
          </el-descriptions-item>
        </el-descriptions>

        <div v-if="detailDialog.user.bio" style="margin-top: 20px;">
          <h4>个人简介</h4>
          <p>{{ detailDialog.user.bio }}</p>
        </div>
      </div>
      <div slot="footer" class="dialog-footer">
        <el-button @click="detailDialog.visible = false">关闭</el-button>
      </div>
    </el-dialog>

    <!-- 编辑用户对话框 -->
    <el-dialog
      title="编辑用户信息"
      :visible.sync="editDialog.visible"
      width="500px">
      <el-form :model="editDialog.form" label-width="100px">
        <el-form-item label="用户名">
          <el-input v-model="editDialog.form.name"></el-input>
        </el-form-item>
        <el-form-item label="邮箱">
          <el-input v-model="editDialog.form.email"></el-input>
        </el-form-item>
        <el-form-item label="手机号码">
          <el-input v-model="editDialog.form.phone"></el-input>
        </el-form-item>
        <el-form-item label="用户类型">
          <el-select v-model="editDialog.form.role" style="width: 100%">
            <el-option label="普通用户" value="user"></el-option>
            <el-option label="管理员" value="admin"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="账户状态">
          <el-switch
            v-model="editDialog.form.status"
            active-value="active"
            inactive-value="disabled"
            active-text="活跃"
            inactive-text="禁用">
          </el-switch>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="editDialog.visible = false">取消</el-button>
        <el-button type="primary" @click="confirmEdit" :loading="editDialog.loading">
          保存
        </el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
export default {
  name: 'UserManagement',
  data() {
    return {
      loading: false,
      statistics: {
        total: 1234,
        active: 1180,
        disabled: 54,
        newToday: 12
      },
      filters: {
        status: '',
        role: '',
        keyword: ''
      },
      users: [],
      selectedUsers: [],
      pagination: {
        page: 1,
        pageSize: 10,
        total: 0
      },
      detailDialog: {
        visible: false,
        user: null
      },
      editDialog: {
        visible: false,
        loading: false,
        form: {
          id: '',
          name: '',
          email: '',
          phone: '',
          role: '',
          status: ''
        }
      }
    }
  },
  mounted() {
    this.fetchUsers()
  },
  methods: {
    // 获取用户列表
    async fetchUsers() {
      this.loading = true
      try {
        // TODO: 调用实际API
        // const response = await this.$api.admin.getUserList({
        //   ...this.filters,
        //   page: this.pagination.page,
        //   pageSize: this.pagination.pageSize
        // })
        
        setTimeout(() => {
          this.users = this.getMockUsers()
          this.pagination.total = 1234
          this.loading = false
        }, 500)
      } catch (error) {
        this.$message.error('获取用户列表失败')
        this.loading = false
      }
    },

    // 查看用户详情
    handleViewUser(user) {
      this.detailDialog.user = user
      this.detailDialog.visible = true
    },

    // 编辑用户
    handleEditUser(user) {
      this.editDialog.form = {
        id: user.id,
        name: user.name,
        email: user.email,
        phone: user.phone,
        role: user.role,
        status: user.status
      }
      this.editDialog.visible = true
    },

    // 确认编辑
    async confirmEdit() {
      this.editDialog.loading = true
      try {
        // TODO: 调用实际API
        // await this.$api.admin.updateUser(this.editDialog.form)
        
        setTimeout(() => {
          this.$message.success('用户信息已更新')
          this.editDialog.visible = false
          this.editDialog.loading = false
          this.fetchUsers()
        }, 500)
      } catch (error) {
        this.$message.error('更新失败')
        this.editDialog.loading = false
      }
    },

    // 禁用用户
    handleDisableUser(user) {
      this.$confirm(`确认禁用用户 ${user.name}？禁用后该用户将无法登录系统。`, '确认禁用', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(async () => {
        try {
          // TODO: 调用实际API
          // await this.$api.admin.disableUser(user.id)
          
          this.$message.success('用户已禁用')
          this.fetchUsers()
        } catch (error) {
          this.$message.error('操作失败')
        }
      }).catch(() => {})
    },

    // 启用用户
    handleEnableUser(user) {
      this.$confirm(`确认启用用户 ${user.name}？`, '确认启用', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'success'
      }).then(async () => {
        try {
          // TODO: 调用实际API
          // await this.$api.admin.enableUser(user.id)
          
          this.$message.success('用户已启用')
          this.fetchUsers()
        } catch (error) {
          this.$message.error('操作失败')
        }
      }).catch(() => {})
    },

    // 批量操作
    handleSelectionChange(val) {
      this.selectedUsers = val
    },

    handleBatchDisable() {
      this.$confirm(`确认批量禁用选中的 ${this.selectedUsers.length} 个用户？`, '批量禁用', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.$message.success('批量禁用成功')
        this.fetchUsers()
      }).catch(() => {})
    },

    handleBatchEnable() {
      this.$confirm(`确认批量启用选中的 ${this.selectedUsers.length} 个用户？`, '批量启用', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'success'
      }).then(() => {
        this.$message.success('批量启用成功')
        this.fetchUsers()
      }).catch(() => {})
    },

    // 导出用户数据
    exportUsers() {
      this.$message.info('正在导出用户数据...')
      // TODO: 实现导出功能
    },

    // 分页
    handleSizeChange(val) {
      this.pagination.pageSize = val
      this.fetchUsers()
    },
    handlePageChange(val) {
      this.pagination.page = val
      this.fetchUsers()
    },

    // 工具方法
    formatDate(date) {
      if (!date) return '-'
      return new Date(date).toLocaleString('zh-CN')
    },

    // 模拟数据
    getMockUsers() {
      return Array.from({ length: 10 }, (_, i) => ({
        id: 1000 + i,
        name: `用户${String.fromCharCode(65 + i)}`,
        email: `user${i}@example.com`,
        phone: `138${String(Math.floor(Math.random() * 100000000)).padStart(8, '0')}`,
        avatar: `https://i.pravatar.cc/150?img=${i + 1}`,
        role: i === 0 ? 'admin' : 'user',
        status: i % 7 === 0 ? 'disabled' : 'active',
        courseCount: Math.floor(Math.random() * 10),
        enrolledCount: Math.floor(Math.random() * 50),
        bio: i % 3 === 0 ? '这是用户的个人简介，热爱学习，积极向上。' : null,
        createdAt: new Date(Date.now() - Math.random() * 365 * 24 * 60 * 60 * 1000).toISOString(),
        lastLoginAt: new Date(Date.now() - Math.random() * 30 * 24 * 60 * 60 * 1000).toISOString()
      }))
    }
  }
}
</script>

<style scoped>
.user-management {
  padding: 20px;
}

.page-header {
  margin-bottom: 20px;
}

.page-header h1 {
  margin: 0;
  font-size: 24px;
  color: #303133;
}

.page-header .subtitle {
  margin: 8px 0 0 0;
  color: #909399;
  font-size: 14px;
}

/* 统计卡片 */
.stats-row {
  margin-bottom: 20px;
}

.stat-card {
  cursor: default;
}

.stat-card.total {
  border-left: 4px solid #409EFF;
}

.stat-card.active {
  border-left: 4px solid #67C23A;
}

.stat-card.disabled {
  border-left: 4px solid #F56C6C;
}

.stat-card.newToday {
  border-left: 4px solid #E6A23C;
}

.stat-content {
  display: flex;
  align-items: center;
  gap: 15px;
}

.stat-content i {
  font-size: 36px;
}

.stat-card.total i {
  color: #409EFF;
}

.stat-card.active i {
  color: #67C23A;
}

.stat-card.disabled i {
  color: #F56C6C;
}

.stat-card.newToday i {
  color: #E6A23C;
}

.stat-value {
  font-size: 28px;
  font-weight: bold;
  color: #303133;
}

.stat-label {
  font-size: 14px;
  color: #909399;
  margin-top: 5px;
}

/* 筛选卡片 */
.filter-card {
  margin-bottom: 20px;
}

.filter-form {
  margin-bottom: 0;
}

/* 用户列表 */
.user-list-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.user-details {
  flex: 1;
}

.user-name {
  font-weight: 500;
  color: #303133;
  margin-bottom: 5px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.user-email {
  font-size: 12px;
  color: #909399;
}

/* 批量操作 */
.batch-actions {
  margin-top: 15px;
  padding: 10px;
  background-color: #f5f7fa;
  border-radius: 4px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.batch-actions span {
  flex: 1;
  color: #606266;
}

/* 分页 */
.pagination-container {
  margin-top: 20px;
  text-align: right;
}

/* 对话框 */
.dialog-footer {
  text-align: right;
}
</style>
