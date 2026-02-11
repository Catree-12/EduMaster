<template>
  <div class="admin-layout">
    <!-- 顶部导航栏 -->
    <header class="admin-header">
      <div class="header-left">
        <span class="logo">📚 管理员控制台</span>
      </div>
      <div class="header-right">
        <span class="admin-name">{{ userInfo.name || '管理员' }}</span>
        <el-dropdown @command="handleCommand">
          <span class="el-dropdown-link">
            <i class="el-icon-arrow-down el-icon--right"></i>
          </span>
          <el-dropdown-menu slot="dropdown">
            <el-dropdown-item command="profile">个人信息</el-dropdown-item>
            <el-dropdown-item command="logout" divided>退出登录</el-dropdown-item>
          </el-dropdown-menu>
        </el-dropdown>
      </div>
    </header>

    <div class="admin-container">
      <!-- 左侧导航菜单 -->
      <aside class="admin-sidebar">
        <el-menu
          :default-active="activeMenu"
          class="admin-menu"
          background-color="#2c3e50"
          text-color="#ecf0f1"
          active-text-color="#3498db"
          router
        >
          <el-menu-item index="/admin/dashboard">
            <i class="el-icon-data-analysis"></i>
            <span slot="title">仪表板</span>
          </el-menu-item>
          
          <el-menu-item index="/admin/course-audit">
            <i class="el-icon-document-checked"></i>
            <span slot="title">课程审核</span>
            <el-badge v-if="pendingCourses > 0" :value="pendingCourses" class="badge" />
          </el-menu-item>
          
          <el-menu-item index="/admin/users">
            <i class="el-icon-user"></i>
            <span slot="title">用户管理</span>
          </el-menu-item>
          
          <el-menu-item index="/admin/content-review">
            <i class="el-icon-warning"></i>
            <span slot="title">内容审核</span>
            <el-badge v-if="pendingReports > 0" :value="pendingReports" class="badge" />
          </el-menu-item>
          
          <el-menu-item index="/admin/certificates">
            <i class="el-icon-medal"></i>
            <span slot="title">证书管理</span>
          </el-menu-item>
          
          <el-menu-item index="/admin/analytics">
            <i class="el-icon-pie-chart"></i>
            <span slot="title">数据分析</span>
          </el-menu-item>
          
          <el-menu-item index="/admin/settings">
            <i class="el-icon-setting"></i>
            <span slot="title">系统设置</span>
          </el-menu-item>
        </el-menu>
      </aside>

      <!-- 主内容区 -->
      <main class="admin-main">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'

export default {
  name: 'AdminLayout',
  data() {
    return {
      pendingCourses: 5, // TODO: 从API获取待审核课程数
      pendingReports: 3  // TODO: 从API获取待处理举报数
    }
  },
  computed: {
    ...mapState('user', ['userInfo']),
    activeMenu() {
      return this.$route.path
    }
  },
  mounted() {
    this.checkAdminPermission()
    this.fetchPendingTasks()
  },
  methods: {
    checkAdminPermission() {
      const userRole = localStorage.getItem('userRole')
      if (userRole !== 'admin') {
        this.$message.error('无权限访问管理员页面')
        this.$router.push('/')
      }
    },
    
    async fetchPendingTasks() {
      // TODO: 获取待处理任务数量
      // const { pendingCourses, pendingReports } = await this.$api.get('/admin/pending-tasks')
      // this.pendingCourses = pendingCourses
      // this.pendingReports = pendingReports
    },
    
    handleCommand(command) {
      if (command === 'logout') {
        this.handleLogout()
      } else if (command === 'profile') {
        this.$router.push('/user-center/profile')
      }
    },
    
    async handleLogout() {
      try {
        // 调用 Vuex action，将 token 加入后端黑名单并清理本地状态
        await this.$store.dispatch('user/logout')
        this.$message.success('已退出登录')
        this.$router.push('/login')
      } catch (error) {
        console.error('退出登录失败:', error)
        this.$message.error('退出登录失败')
      }
    }
  }
}
</script>

<style scoped>
.admin-layout {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background: #ecf0f1;
}

/* 顶部导航栏 */
.admin-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 60px;
  background: #34495e;
  color: white;
  padding: 0 2rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  z-index: 1000;
}

.header-left .logo {
  font-size: 1.25rem;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.admin-name {
  font-size: 0.95rem;
}

.el-dropdown-link {
  cursor: pointer;
  color: white;
}

/* 容器布局 */
.admin-container {
  display: flex;
  flex: 1;
  overflow: hidden;
}

/* 左侧菜单 */
.admin-sidebar {
  width: 200px;
  background: #2c3e50;
  overflow-y: auto;
  box-shadow: 2px 0 4px rgba(0, 0, 0, 0.1);
}

.admin-menu {
  border-right: none;
}

.admin-menu .el-menu-item {
  position: relative;
  padding-left: 20px !important;
}

.admin-menu .el-menu-item i {
  margin-right: 8px;
  font-size: 16px;
}

.badge {
  position: absolute;
  right: 15px;
  top: 50%;
  transform: translateY(-50%);
}

/* 主内容区 */
.admin-main {
  flex: 1;
  padding: 2rem;
  overflow-y: auto;
  background: #ecf0f1;
}

/* 滚动条样式 */
.admin-sidebar::-webkit-scrollbar,
.admin-main::-webkit-scrollbar {
  width: 6px;
}

.admin-sidebar::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.2);
  border-radius: 3px;
}

.admin-main::-webkit-scrollbar-thumb {
  background: rgba(0, 0, 0, 0.2);
  border-radius: 3px;
}

/* 响应式 */
@media (max-width: 768px) {
  .admin-sidebar {
    width: 64px;
  }
  
  .admin-menu span {
    display: none;
  }
  
  .admin-main {
    padding: 1rem;
  }
}
</style>
