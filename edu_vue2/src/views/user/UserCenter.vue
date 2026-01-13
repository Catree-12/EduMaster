<template>
  <div class="user-center">
    <div class="user-header">
      <div class="user-info">
        <div class="avatar">👤</div>
        <div class="user-details">
          <h2>{{ userInfo.name }}</h2>
          <p>{{ userInfo.email }}</p>
        </div>
      </div>
    </div>

    <div class="center-layout">
      <nav class="center-nav">
        <router-link 
          to="/user-center/profile" 
          class="nav-item"
          :class="{ active: $route.name === 'MyProfile' }"
        >
          📋 个人信息
        </router-link>
        <router-link 
          to="/user-center/my-courses" 
          class="nav-item"
          :class="{ active: $route.name === 'MyCourses' }"
        >
          📚 我的课程
        </router-link>
        <router-link 
          to="/user-center/course-management" 
          class="nav-item"
          :class="{ active: $route.name === 'CourseManagement' }"
        >
          🎓 我的讲座
        </router-link>
      </nav>

      <main class="center-content">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script>
export default {
  name: 'UserCenter',
  data() {
    return {
      userInfo: {
        name: '张三',
        email: 'zhangsan@example.com',
        avatar: '👤'
      }
    }
  }
}
</script>

<style scoped>
.user-center {
  width: 100%;
}

.user-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 2rem;
  border-radius: 8px;
  margin-bottom: 2rem;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.avatar {
  font-size: 3rem;
  width: 80px;
  height: 80px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 50%;
}

.user-details h2 {
  margin: 0;
}

.user-details p {
  margin: 0.5rem 0 0 0;
  opacity: 0.9;
}

.center-layout {
  display: grid;
  grid-template-columns: 200px 1fr;
  gap: 2rem;
}

.center-nav {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  height: fit-content;
  position: sticky;
  top: 100px;
}

.nav-item {
  display: block;
  padding: 1rem;
  color: #7f8c8d;
  text-decoration: none;
  border-left: 4px solid transparent;
  transition: all 0.3s;
  border-bottom: 1px solid #ecf0f1;
}

.nav-item:last-child {
  border-bottom: none;
}

.nav-item:hover {
  background-color: #f8f9fa;
  color: #667eea;
}

.nav-item.active {
  background-color: #f0f0ff;
  color: #667eea;
  border-left-color: #667eea;
}

.center-content {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

@media (max-width: 768px) {
  .center-layout {
    grid-template-columns: 1fr;
  }

  .center-nav {
    position: static;
    display: flex;
    overflow-x: auto;
  }

  .nav-item {
    flex-shrink: 0;
  }
}
</style>