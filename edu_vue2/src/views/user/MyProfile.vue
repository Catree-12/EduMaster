<template>
  <div class="my-profile">
    <div class="profile-header">
      <div class="profile-card">
        <div class="avatar">👤</div>
        <div class="user-info">
          <h2>张三</h2>
          <p class="email">zhangsan@example.com</p>
          <p class="status">学生 · 已加入 3 个月</p>
        </div>
        <button class="edit-btn">编辑资料</button>
      </div>
    </div>

    <div class="profile-stats">
      <div class="stat-card">
        <div class="stat-value">5</div>
        <div class="stat-label">正在学习</div>
      </div>
      <div class="stat-card">
        <div class="stat-value">3</div>
        <div class="stat-label">已完成</div>
      </div>
      <div class="stat-card">
        <div class="stat-value">12</div>
        <div class="stat-label">学习时长(小时)</div>
      </div>
      <div class="stat-card">
        <div class="stat-value">4.5</div>
        <div class="stat-label">平均评分</div>
      </div>
    </div>

    <div class="profile-content">
      <div class="section">
        <h3>个人信息</h3>
        <div class="info-group">
          <label>用户名</label>
          <p>张三</p>
        </div>
        <div class="info-group">
          <label>邮箱</label>
          <p>zhangsan@example.com</p>
        </div>
        <div class="info-group">
          <label>手机</label>
          <p>138****1234</p>
        </div>
        <div class="info-group">
          <label>身份</label>
          <p>学生</p>
        </div>
      </div>

      <div class="section">
        <h3>账号设置</h3>
        <div class="setting-item">
          <span>修改密码</span>
          <button class="action-link">修改 →</button>
        </div>
        <div class="setting-item">
          <span>隐私设置</span>
          <button class="action-link">设置 →</button>
        </div>
        <div class="setting-item">
          <span>通知设置</span>
          <button class="action-link">设置 →</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'MyProfile',
  data() {
    return {
      user: {
        name: '张三',
        email: 'zhangsan@example.com',
        phone: '138****1234',
        role: '学生',
        joinDate: '3 个月'
      }
    }
  }
}
</script>

<style scoped>
.my-profile {
  width: 100%;
}

.profile-header {
  margin-bottom: 2rem;
}

.profile-card {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  display: flex;
  gap: 2rem;
  align-items: center;
}

.avatar {
  width: 80px;
  height: 80px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 3rem;
  flex-shrink: 0;
}

.user-info {
  flex: 1;
}

.user-info h2 {
  margin: 0 0 0.5rem 0;
  color: #2c3e50;
}

.email {
  color: #7f8c8d;
  margin: 0 0 0.25rem 0;
  font-size: 0.9rem;
}

.status {
  color: #95a5a6;
  margin: 0;
  font-size: 0.85rem;
}

.edit-btn {
  padding: 0.6rem 1.5rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 600;
  transition: opacity 0.3s;
}

.edit-btn:hover {
  opacity: 0.9;
}

.profile-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 1rem;
  margin-bottom: 2rem;
}

.stat-card {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  text-align: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.stat-value {
  font-size: 2rem;
  font-weight: 800;
  color: #667eea;
  margin-bottom: 0.5rem;
}

.stat-label {
  color: #7f8c8d;
  font-size: 0.875rem;
}

.profile-content {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 2rem;
}

.section {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.section h3 {
  margin: 0 0 1.5rem 0;
  color: #2c3e50;
  font-size: 1.1rem;
}

.info-group {
  margin-bottom: 1.5rem;
}

.info-group label {
  display: block;
  color: #7f8c8d;
  font-size: 0.875rem;
  margin-bottom: 0.5rem;
  font-weight: 500;
}

.info-group p {
  margin: 0;
  color: #2c3e50;
}

.setting-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 0;
  border-bottom: 1px solid #ecf0f1;
}

.setting-item:last-child {
  border-bottom: none;
}

.action-link {
  background: none;
  border: none;
  color: #667eea;
  cursor: pointer;
  font-weight: 600;
  transition: color 0.3s;
}

.action-link:hover {
  color: #764ba2;
}

@media (max-width: 768px) {
  .profile-card {
    flex-direction: column;
    text-align: center;
  }

  .profile-stats {
    grid-template-columns: repeat(2, 1fr);
  }

  .profile-content {
    grid-template-columns: 1fr;
  }
}
</style>
