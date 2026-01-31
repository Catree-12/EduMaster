<template>
  <div class="main-layout">
    <!-- 顶部导航栏 -->
    <nav class="navbar">
      <div class="nav-container">
        <div class="nav-logo">
          <router-link to="/"><h2>EduMaster</h2></router-link>
        </div>
        
        <ul class="nav-menu">
          <li class="nav-item">
            <router-link to="/" class="nav-link">首页</router-link>
          </li>
          <li class="nav-item">
            <router-link to="/course" class="nav-link">课程中心</router-link>
          </li>
          <li class="nav-item">
            <router-link to="/course/my-courses" class="nav-link">我的课程</router-link>
          </li>
          <li class="nav-item">
            <router-link to="/community" class="nav-link">社区</router-link>
          </li>
          <li class="nav-item">
            <router-link to="/messages" class="nav-link">消息</router-link>
          </li>
        </ul>

        <div class="nav-right">
          <!-- 设置下拉菜单 -->
          <div class="dropdown">
            <span class="user-icon">
              ⚙️ 设置
            </span>
            <ul class="dropdown-menu">
              <li>
                <router-link to="/user-center/profile" class="dropdown-link">
                  👤 个人中心
                </router-link>
              </li>
              <li>
                <router-link to="/user-center/certificates" class="dropdown-link">
                  🎓 我的证书
                </router-link>
              </li>
            </ul>
          </div>
          <button @click="logout" class="logout-btn">退出登录</button>
        </div>
      </div>
    </nav>

    <!-- 主容器 -->
    <div class="main-container">
      <router-view />
    </div>
  </div>
</template>

<script>
export default {
  name: 'MainLayout',
  methods: {
    logout() {
      // 清理 Vuex 状态
      this.$store.dispatch('user/logout')
      // localStorage 在 Vuex mutation 中已清理
      this.$message.success('已退出登录')
      this.$router.push('/login')
    }
  }
}
</script>

<style scoped>
.main-layout {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.navbar {
  background-color: #2c3e50;
  padding: 1rem 0;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  position: sticky;
  top: 0;
  z-index: 1000;
  height: 64px;
}

.nav-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  
}

.nav-logo h2 {
  color: white;
  margin: 0;
  text-align: left; /* 确保文字在容器内也是靠左的 */
  
}

.nav-logo a {
  text-decoration: none;
}

.nav-menu {
  display: flex;
  list-style: none;
  gap: 2rem;
  margin: 0;
  padding: 0;
  align-items: center;
}

.nav-item {
  position: relative;
}

.nav-link {
  color: white;
  text-decoration: none;
  transition: color 0.3s;
  cursor: pointer;
}

.nav-link:hover {
  color: #3498db;
}

.dropdown {
  position: relative;
}

.dropdown-menu {
  display: none;
  position: absolute;
  top: calc(100% + 0.5rem);
  right: 0;
  background: #34495e;
  list-style: none;
  margin: 0;
  padding: 0.5rem 0;
  border-radius: 8px;
  min-width: 160px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  z-index: 1000;
}

/* 添加延迟和扩展hover区域 */
.dropdown-menu::before {
  content: '';
  position: absolute;
  top: -0.5rem;
  left: 0;
  right: 0;
  height: 0.5rem;
  background: transparent;
}

.dropdown:hover .dropdown-menu {
  display: block;
  animation: fadeIn 0.2s ease-in-out;
  animation-delay: 0.1s;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.dropdown-menu li {
  margin: 0;
}

.dropdown-link {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: white;
  text-decoration: none;
  padding: 0.75rem 1.25rem;
  transition: all 0.2s;
  font-size: 0.95rem;
}

.dropdown-link:hover {
  background: #2c3e50;
  color: #3498db;
}

.nav-right {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.dropdown {
  position: relative;
  cursor: pointer;
}

.user-icon {
  color: white;
  text-decoration: none;
  transition: color 0.3s;
  display: flex;
  align-items: center;
  gap: 0.25rem;
  padding: 0.5rem 0.75rem;
  border-radius: 4px;
}

.user-icon:hover,
.dropdown:hover .user-icon {
  color: #3498db;
  background: rgba(52, 152, 219, 0.1);
}

.logout-btn {
  background-color: #e74c3c;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
  font-weight: 600;
}

.logout-btn:hover {
  background-color: #c0392b;
}

.main-container {
  flex: 1;
  width: 100%;
}
</style>
