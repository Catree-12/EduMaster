<template>
  <header class="header">
    <div class="header-container">
      <div class="logo">
        <router-link to="/">🎓 EduMster</router-link>
      </div>

      <div class="user-section">
        <div class="search-box">
          <input type="text" placeholder="搜索课程...">
          <button>🔍</button>
        </div>

        <el-dropdown @command="handleCommand" class="user-menu">
          <span class="el-dropdown-link">
            👤 账户<i class="el-icon-arrow-down el-icon--right"></i>
          </span>
          <el-dropdown-menu slot="dropdown">
            <el-dropdown-item command="profile" v-if="$route.path !== '/main/profile'">个人资料</el-dropdown-item>
            <el-dropdown-item command="settings" v-if="$route.path !== '/main/settings'">账号设置</el-dropdown-item>
            <el-dropdown-item command="my-courses" v-if="$route.path !== '/courses/my'">我的课程</el-dropdown-item>
            <el-dropdown-divider></el-dropdown-divider>
            <el-dropdown-item command="logout">退出登录</el-dropdown-item>
          </el-dropdown-menu>
        </el-dropdown>
      </div>
    </div>
  </header>
</template>

<script>
export default {
  name: 'TopHeader',
  methods: {
    handleCommand(command) {
      if (command === 'profile') {
        if (this.$route.path !== '/main/profile') {
          this.$router.push('/main/profile').catch(() => {})
        }
      } else if (command === 'settings') {
        if (this.$route.path !== '/main/settings') {
          this.$router.push('/main/settings').catch(() => {})
        }
      } else if (command === 'my-courses') {
        if (this.$route.path !== '/courses/my') {
          this.$router.push('/courses/my').catch(() => {})
        }
      } else if (command === 'logout') {
        localStorage.removeItem('isLoggedIn')
        localStorage.removeItem('username')
        this.$message.success('退出登录成功')
        this.$router.push('/login').catch(() => {})
      }
    }
  }
}
</script>

<style scoped>
.header {
  background: white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  position: sticky;
  top: 0;
  z-index: 100;
}

.header-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 30px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 70px;
}

.logo {
  font-size: 24px;
  font-weight: 700;
}

.logo a {
  color: #667eea;
  text-decoration: none;
  transition: color 0.3s;
}

.logo a:hover {
  color: #5568d3;
}

.user-section {
  display: flex;
  align-items: center;
  gap: 25px;
}

.search-box {
  display: flex;
  background: #f5f5f5;
  border-radius: 25px;
  padding: 8px 15px;
  min-width: 200px;
}

.search-box input {
  flex: 1;
  background: none;
  border: none;
  outline: none;
  font-size: 14px;
  color: #333;
}

.search-box input::placeholder {
  color: #999;
}

.search-box button {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 16px;
  color: #999;
  transition: color 0.3s;
}

.search-box button:hover {
  color: #667eea;
}

.user-menu {
  cursor: pointer;
}

.el-dropdown-link {
  color: #555;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 5px;
  transition: color 0.3s;
}

.el-dropdown-link:hover {
  color: #667eea;
}

@media (max-width: 768px) {
  .header-container {
    padding: 0 15px;
  }

  .search-box {
    display: none;
  }
}
</style>
