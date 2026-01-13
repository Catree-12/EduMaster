<template>
  <div class="user-profile-container">
    <div class="profile-header">
      <div class="avatar-section">
        <img :src="user.avatar" :alt="user.name" class="avatar">
        <button class="btn-upload">更换头像</button>
      </div>
      <div class="header-info">
        <h1>{{ user.name }}</h1>
        <p class="email">{{ user.email }}</p>
        <p class="joined">加入于 {{ user.joinDate }}</p>
        <button class="btn-edit-profile">编辑资料</button>
      </div>
    </div>

    <div class="profile-stats">
      <div class="stat-card">
        <div class="stat-number">{{ user.coursesCreated }}</div>
        <div class="stat-label">已创建课程</div>
      </div>
      <div class="stat-card">
        <div class="stat-number">{{ user.coursesEnrolled }}</div>
        <div class="stat-label">已加入课程</div>
      </div>
      <div class="stat-card">
        <div class="stat-number">{{ user.totalStudents }}</div>
        <div class="stat-label">教授学生数</div>
      </div>
      <div class="stat-card">
        <div class="stat-number">{{ user.rating }}</div>
        <div class="stat-label">平均评分</div>
      </div>
    </div>

    <div class="profile-content">
      <div class="tabs">
        <button 
          v-for="tab in tabs" 
          :key="tab"
          :class="{ active: activeTab === tab }"
          @click="activeTab = tab"
          class="tab-btn"
        >
          {{ tab }}
        </button>
      </div>

      <div class="tab-content">
        <div v-if="activeTab === '个人信息'" class="personal-info">
          <div class="info-group">
            <label>用户名</label>
            <p>{{ user.name }}</p>
          </div>
          <div class="info-group">
            <label>邮箱</label>
            <p>{{ user.email }}</p>
          </div>
          <div class="info-group">
            <label>简介</label>
            <p>{{ user.bio }}</p>
          </div>
          <div class="info-group">
            <label>职位</label>
            <p>{{ user.title }}</p>
          </div>
          <button class="btn-edit">编辑信息</button>
        </div>

        <div v-if="activeTab === '安全设置'" class="security-settings">
          <div class="setting-item">
            <div>
              <h3>更改密码</h3>
              <p>定期更改密码以保护您的账户</p>
            </div>
            <button class="btn-action">更改</button>
          </div>
          <div class="setting-item">
            <div>
              <h3>两步验证</h3>
              <p>启用两步验证增强账户安全</p>
            </div>
            <button class="btn-action">设置</button>
          </div>
          <div class="setting-item">
            <div>
              <h3>登录历史</h3>
              <p>查看您的账户登录记录</p>
            </div>
            <button class="btn-action">查看</button>
          </div>
        </div>

        <div v-if="activeTab === '通知设置'" class="notification-settings">
          <div class="setting-item">
            <div>
              <h3>课程通知</h3>
              <p>接收课程更新和公告</p>
            </div>
            <input type="checkbox" v-model="notifications.course" class="toggle">
          </div>
          <div class="setting-item">
            <div>
              <h3>消息通知</h3>
              <p>接收来自其他用户的消息</p>
            </div>
            <input type="checkbox" v-model="notifications.message" class="toggle">
          </div>
          <div class="setting-item">
            <div>
              <h3>邮件通知</h3>
              <p>通过邮件接收重要更新</p>
            </div>
            <input type="checkbox" v-model="notifications.email" class="toggle">
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'UserProfile',
  data() {
    return {
      activeTab: '个人信息',
      tabs: ['个人信息', '安全设置', '通知设置'],
      user: {
        name: '张三',
        email: 'zhangsan@example.com',
        avatar: 'https://via.placeholder.com/120?text=Avatar',
        joinDate: '2023年1月15日',
        bio: '一名热爱教学的技术工程师',
        title: '高级开发工程师',
        coursesCreated: 8,
        coursesEnrolled: 15,
        totalStudents: 3500,
        rating: 4.8
      },
      notifications: {
        course: true,
        message: true,
        email: false
      }
    }
  }
}
</script>

<style scoped>
.user-profile-container {
  padding: 30px;
  background: #f5f5f5;
  min-height: 100vh;
}

.profile-header {
  display: flex;
  gap: 40px;
  background: white;
  padding: 40px;
  border-radius: 8px;
  margin-bottom: 30px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.avatar-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 15px;
}

.avatar {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  object-fit: cover;
  border: 4px solid #667eea;
}

.btn-upload {
  padding: 8px 16px;
  background: #f0f0f0;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 600;
  transition: all 0.3s;
}

.btn-upload:hover {
  background: #e0e0e0;
}

.header-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.header-info h1 {
  font-size: 28px;
  margin-bottom: 10px;
}

.email {
  color: #667eea;
  margin-bottom: 5px;
}

.joined {
  color: #999;
  font-size: 14px;
  margin-bottom: 15px;
}

.btn-edit-profile {
  width: 150px;
  padding: 10px 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 600;
  transition: opacity 0.3s;
}

.btn-edit-profile:hover {
  opacity: 0.9;
}

.profile-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.stat-card {
  background: white;
  padding: 25px;
  border-radius: 8px;
  text-align: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.stat-number {
  font-size: 32px;
  font-weight: 700;
  color: #667eea;
  margin-bottom: 10px;
}

.stat-label {
  color: #999;
  font-size: 14px;
}

.profile-content {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.tabs {
  display: flex;
  border-bottom: 1px solid #eee;
}

.tab-btn {
  padding: 20px 30px;
  background: none;
  border: none;
  cursor: pointer;
  font-size: 16px;
  font-weight: 600;
  color: #999;
  transition: all 0.3s;
  border-bottom: 3px solid transparent;
}

.tab-btn.active {
  color: #667eea;
  border-bottom-color: #667eea;
}

.tab-content {
  padding: 30px;
}

.info-group {
  margin-bottom: 20px;
}

.info-group label {
  display: block;
  color: #999;
  font-size: 14px;
  margin-bottom: 8px;
}

.info-group p {
  color: #333;
  font-size: 16px;
}

.btn-edit {
  margin-top: 20px;
  padding: 10px 30px;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s;
}

.btn-edit:hover {
  opacity: 0.9;
}

.setting-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  border-bottom: 1px solid #eee;
}

.setting-item:last-child {
  border-bottom: none;
}

.setting-item h3 {
  margin-bottom: 5px;
  color: #333;
}

.setting-item p {
  color: #999;
  font-size: 14px;
}

.btn-action {
  padding: 8px 20px;
  background: #f0f0f0;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s;
}

.btn-action:hover {
  background: #e0e0e0;
}

.toggle {
  width: 50px;
  height: 30px;
  cursor: pointer;
}
</style>
