<template>
  <div class="user-settings-container">
    <h1>账号设置</h1>

    <div class="settings-content">
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
        <!-- 账号信息 -->
        <div v-if="activeTab === '账号信息'" class="settings-section">
          <div class="setting-item">
            <label>用户名</label>
            <input v-model="settings.username" type="text" disabled class="disabled-input">
          </div>
          <div class="setting-item">
            <label>邮箱地址</label>
            <div class="email-group">
              <input v-model="settings.email" type="email" placeholder="输入邮箱地址">
              <button class="btn-verify">验证</button>
            </div>
            <p class="hint">我们会发送验证链接到您的邮箱</p>
          </div>
          <div class="setting-item">
            <label>手机号码</label>
            <input v-model="settings.phone" type="tel" placeholder="输入手机号码">
          </div>
          <button class="btn-save" @click="saveSettings">保存更改</button>
        </div>

        <!-- 密码安全 -->
        <div v-if="activeTab === '密码安全'" class="settings-section">
          <div class="setting-item">
            <label>当前密码</label>
            <input v-model="password.current" type="password" placeholder="输入当前密码">
          </div>
          <div class="setting-item">
            <label>新密码</label>
            <input v-model="password.new" type="password" placeholder="输入新密码（至少6位）">
          </div>
          <div class="setting-item">
            <label>确认新密码</label>
            <input v-model="password.confirm" type="password" placeholder="确认新密码">
          </div>
          <button class="btn-save" @click="changePassword">修改密码</button>
        </div>

        <!-- 隐私设置 -->
        <div v-if="activeTab === '隐私设置'" class="settings-section">
          <div class="setting-toggle">
            <div>
              <h3>个人资料可见性</h3>
              <p>允许其他用户查看您的个人资料</p>
            </div>
            <input v-model="privacy.profileVisible" type="checkbox" class="toggle-switch">
          </div>
          <div class="setting-toggle">
            <div>
              <h3>显示学习进度</h3>
              <p>允许其他用户看到您的课程学习进度</p>
            </div>
            <input v-model="privacy.showProgress" type="checkbox" class="toggle-switch">
          </div>
          <div class="setting-toggle">
            <div>
              <h3>接收消息</h3>
              <p>允许其他用户向您发送私信</p>
            </div>
            <input v-model="privacy.receiveMessages" type="checkbox" class="toggle-switch">
          </div>
          <button class="btn-save" @click="savePrivacy">保存隐私设置</button>
        </div>

        <!-- 登录活动 -->
        <div v-if="activeTab === '登录活动'" class="settings-section">
          <div class="activity-list">
            <div v-for="activity in loginActivities" :key="activity.id" class="activity-item">
              <div class="activity-info">
                <p class="device">{{ activity.device }}</p>
                <p class="location">{{ activity.location }}</p>
              </div>
              <div class="activity-time">{{ activity.time }}</div>
              <button v-if="activity.id !== 'current'" class="btn-logout-device" @click="logoutDevice(activity.id)">登出</button>
              <span v-else class="current-session">当前会话</span>
            </div>
          </div>
        </div>

        <!-- 账号删除 -->
        <div v-if="activeTab === '账号删除'" class="settings-section danger-zone">
          <h3>删除账户</h3>
          <p>⚠️ 这是一个不可撤销的操作。删除账户后，您的所有数据将被永久删除。</p>
          <button class="btn-delete" @click="showDeleteConfirm = true">删除我的账户</button>
        </div>
      </div>
    </div>

    <!-- 删除确认对话框 -->
    <div v-if="showDeleteConfirm" class="modal-overlay" @click="showDeleteConfirm = false">
      <div class="modal-content" @click.stop>
        <h2>确认删除账户</h2>
        <p>您确定要删除账户吗？此操作无法撤销。</p>
        <div class="modal-footer">
          <button class="btn-cancel" @click="showDeleteConfirm = false">取消</button>
          <button class="btn-delete-confirm" @click="deleteAccount">确认删除</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'UserSettings',
  data() {
    return {
      activeTab: '账号信息',
      tabs: ['账号信息', '密码安全', '隐私设置', '登录活动', '账号删除'],
      showDeleteConfirm: false,
      settings: {
        username: 'zhangsan',
        email: 'zhangsan@example.com',
        phone: '138****8888'
      },
      password: {
        current: '',
        new: '',
        confirm: ''
      },
      privacy: {
        profileVisible: true,
        showProgress: true,
        receiveMessages: true
      },
      loginActivities: [
        {
          id: 'current',
          device: 'Chrome - Windows 10',
          location: '北京',
          time: '当前会话'
        },
        {
          id: '1',
          device: 'Safari - macOS',
          location: '上海',
          time: '2024年1月20日 14:30'
        },
        {
          id: '2',
          device: 'Chrome Mobile - iOS',
          location: '深圳',
          time: '2024年1月18日 09:15'
        }
      ]
    }
  },
  methods: {
    saveSettings() {
      this.$message.success('账号信息已保存')
    },
    changePassword() {
      if (!this.password.current || !this.password.new || !this.password.confirm) {
        this.$message.error('请填写所有密码字段')
        return
      }
      if (this.password.new !== this.password.confirm) {
        this.$message.error('两次输入的密码不一致')
        return
      }
      if (this.password.new.length < 6) {
        this.$message.error('新密码长度至少为6位')
        return
      }
      this.$message.success('密码修改成功')
      this.password = { current: '', new: '', confirm: '' }
    },
    savePrivacy() {
      this.$message.success('隐私设置已保存')
    },
    logoutDevice(deviceId) {
      this.loginActivities = this.loginActivities.filter(a => a.id !== deviceId)
      this.$message.success('已在该设备上登出')
    },
    deleteAccount() {
      this.$message.success('账户已删除')
      localStorage.removeItem('isLoggedIn')
      localStorage.removeItem('username')
      this.$router.push('/login')
      this.showDeleteConfirm = false
    }
  }
}
</script>

<style scoped>
.user-settings-container {
  padding: 30px;
  background: #f5f5f5;
  min-height: 100vh;
}

h1 {
  font-size: 28px;
  margin-bottom: 30px;
  color: #333;
}

.settings-content {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.tabs {
  display: flex;
  border-bottom: 1px solid #eee;
  flex-wrap: wrap;
}

.tab-btn {
  padding: 20px 25px;
  background: none;
  border: none;
  cursor: pointer;
  font-size: 16px;
  font-weight: 600;
  color: #999;
  transition: all 0.3s;
  border-bottom: 3px solid transparent;
  margin-bottom: -1px;
}

.tab-btn.active {
  color: #667eea;
  border-bottom-color: #667eea;
}

.tab-content {
  padding: 30px;
  max-width: 600px;
}

.settings-section h3 {
  margin-top: 0;
  color: #333;
}

.setting-item {
  margin-bottom: 25px;
}

.setting-item label {
  display: block;
  margin-bottom: 10px;
  color: #555;
  font-weight: 600;
}

.setting-item input {
  width: 100%;
  padding: 12px 15px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 14px;
  transition: border-color 0.3s;
  box-sizing: border-box;
}

.setting-item input:focus {
  outline: none;
  border-color: #667eea;
}

.disabled-input {
  background: #f5f5f5;
  cursor: not-allowed;
}

.email-group {
  display: flex;
  gap: 10px;
}

.email-group input {
  flex: 1;
}

.btn-verify {
  padding: 12px 20px;
  background: #f0f0f0;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
  color: #667eea;
  transition: all 0.3s;
}

.btn-verify:hover {
  background: #667eea;
  color: white;
}

.hint {
  margin: 8px 0 0;
  font-size: 12px;
  color: #999;
}

.setting-toggle {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  background: #f9f9f9;
  border-radius: 6px;
  margin-bottom: 15px;
}

.setting-toggle h3 {
  margin: 0 0 5px;
  font-size: 16px;
}

.setting-toggle p {
  margin: 0;
  font-size: 12px;
  color: #999;
}

.toggle-switch {
  width: 50px;
  height: 30px;
  cursor: pointer;
}

.activity-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.activity-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px;
  background: #f9f9f9;
  border-radius: 6px;
}

.activity-info p {
  margin: 0;
  font-size: 14px;
}

.device {
  font-weight: 600;
  color: #333;
}

.location {
  color: #999;
  font-size: 12px;
  margin-top: 5px;
}

.activity-time {
  color: #999;
  font-size: 12px;
  min-width: 120px;
  text-align: right;
}

.btn-logout-device {
  padding: 6px 12px;
  background: #ffebee;
  border: none;
  border-radius: 4px;
  color: #c62828;
  cursor: pointer;
  font-size: 12px;
  font-weight: 600;
  transition: all 0.3s;
}

.btn-logout-device:hover {
  background: #c62828;
  color: white;
}

.current-session {
  color: #4caf50;
  font-weight: 600;
  font-size: 12px;
}

.danger-zone {
  padding: 20px;
  background: #ffebee;
  border-radius: 6px;
  border-left: 4px solid #c62828;
}

.danger-zone h3 {
  color: #c62828;
  margin-top: 0;
}

.danger-zone p {
  color: #c62828;
  font-size: 14px;
}

.btn-save,
.btn-delete {
  padding: 12px 30px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s;
}

.btn-save {
  background: #667eea;
  color: white;
}

.btn-save:hover {
  opacity: 0.9;
}

.btn-delete {
  background: #c62828;
  color: white;
}

.btn-delete:hover {
  opacity: 0.9;
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
  padding: 30px;
  border-radius: 8px;
  max-width: 400px;
  width: 90%;
}

.modal-content h2 {
  margin-top: 0;
  color: #c62828;
}

.modal-content p {
  color: #666;
  line-height: 1.6;
}

.modal-footer {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
  margin-top: 25px;
}

.btn-cancel {
  padding: 10px 24px;
  background: #f0f0f0;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s;
}

.btn-cancel:hover {
  background: #e0e0e0;
}

.btn-delete-confirm {
  padding: 10px 24px;
  background: #c62828;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s;
}

.btn-delete-confirm:hover {
  opacity: 0.9;
}
</style>
