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
            <router-link to="/user-center/certificates" class="nav-link">我的证书</router-link>
          </li>
          <li class="nav-item">
            <router-link to="/community" class="nav-link">社区</router-link>
          </li>
        </ul>

        <div class="nav-right">
          <router-link to="/user-center/profile" class="user-icon">
            👤 个人中心
          </router-link>
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
  z-index: 100;
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
  top: 100%;
  left: 0;
  background: #34495e;
  list-style: none;
  margin: 0;
  padding: 0.5rem 0;
  border-radius: 4px;
  min-width: 150px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
}

.dropdown:hover .dropdown-menu {
  display: block;
}

.dropdown-link {
  display: block;
  color: white;
  text-decoration: none;
  padding: 0.75rem 1.5rem;
  transition: all 0.3s;
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

.user-icon {
  color: white;
  text-decoration: none;
  transition: color 0.3s;
}

.user-icon:hover {
  color: #3498db;
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
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}
</style>
