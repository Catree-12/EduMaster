<template>
  <div class="my-profile">
    <div class="profile-header">
      <div class="profile-card">
        <div class="avatar">👤</div>
        <div class="user-info">
          <h2>张三</h2>
          <p class="email">zhangsan@example.com</p>
        </div>
      </div>
    </div>

    <div class="profile-content">
      <el-tabs v-model="activeTab" type="card">
        <!-- 个人信息标签页 -->
        <el-tab-pane label="个人信息" name="info">
          <div class="tab-content">
            <div class="info-form">
              <div class="info-group">
                <label>用户名</label>
                <el-input v-model="userInfo.name" :disabled="!editingInfo" placeholder="请输入用户名"></el-input>
              </div>
              <div class="info-group">
                <label>邮箱</label>
                <el-input v-model="userInfo.email" :disabled="!editingInfo" placeholder="请输入邮箱"></el-input>
              </div>
              <div class="info-group">
                <label>手机</label>
                <el-input v-model="userInfo.phone" :disabled="!editingInfo" placeholder="请输入手机号"></el-input>
              </div>
            </div>
            <div class="action-buttons">
              <el-button v-if="!editingInfo" type="primary" @click="startEditInfo">编辑</el-button>
              <template v-else>
                <el-button type="primary" @click="saveInfo">保存</el-button>
                <el-button @click="cancelEditInfo">取消</el-button>
              </template>
            </div>
          </div>
        </el-tab-pane>

        <!-- 密码设置标签页 -->
        <el-tab-pane label="密码设置" name="password">
          <div class="tab-content">
            <div class="password-form">
              <div class="info-group">
                <label>当前密码</label>
                <el-input v-model="passwordForm.currentPassword" type="password" :disabled="!editingPassword" placeholder="请输入当前密码" show-password></el-input>
              </div>
              <div class="info-group">
                <label>新密码</label>
                <el-input v-model="passwordForm.newPassword" type="password" :disabled="!editingPassword" placeholder="请输入新密码" show-password></el-input>
              </div>
              <div class="info-group">
                <label>确认新密码</label>
                <el-input v-model="passwordForm.confirmPassword" type="password" :disabled="!editingPassword" placeholder="请再次输入新密码" show-password></el-input>
              </div>
            </div>
            <div class="action-buttons">
              <el-button v-if="!editingPassword" type="primary" @click="startEditPassword">编辑</el-button>
              <template v-else>
                <el-button type="primary" @click="savePassword">保存</el-button>
                <el-button @click="cancelEditPassword">取消</el-button>
              </template>
            </div>
          </div>
        </el-tab-pane>
      </el-tabs>
    </div>
  </div>
</template>

<script>
export default {
  name: 'MyProfile',
  data() {
    return {
      activeTab: 'info',
      editingInfo: false,
      editingPassword: false,
      userInfo: {
        name: '张三',
        email: 'zhangsan@example.com',
        phone: '138****1234'
      },
      originalUserInfo: {},
      passwordForm: {
        currentPassword: '',
        newPassword: '',
        confirmPassword: ''
      }
    }
  },
  methods: {
    // 个人信息编辑
    startEditInfo() {
      this.originalUserInfo = { ...this.userInfo }
      this.editingInfo = true
    },
    saveInfo() {
      if (!this.userInfo.name || !this.userInfo.email || !this.userInfo.phone) {
        this.$message.error('请填写完整信息')
        return
      }
      // 这里应该调用API保存信息
      this.$message.success('个人信息保存成功')
      this.editingInfo = false
    },
    cancelEditInfo() {
      this.userInfo = { ...this.originalUserInfo }
      this.editingInfo = false
    },
    
    // 密码设置编辑
    startEditPassword() {
      this.editingPassword = true
      this.passwordForm = {
        currentPassword: '',
        newPassword: '',
        confirmPassword: ''
      }
    },
    savePassword() {
      if (!this.passwordForm.currentPassword || !this.passwordForm.newPassword || !this.passwordForm.confirmPassword) {
        this.$message.error('请填写完整密码信息')
        return
      }
      if (this.passwordForm.newPassword !== this.passwordForm.confirmPassword) {
        this.$message.error('两次输入的新密码不一致')
        return
      }
      if (this.passwordForm.newPassword.length < 6) {
        this.$message.error('密码长度不能少于6位')
        return
      }
      // 这里应该调用API修改密码
      this.$message.success('密码修改成功')
      this.editingPassword = false
      this.passwordForm = {
        currentPassword: '',
        newPassword: '',
        confirmPassword: ''
      }
    },
    cancelEditPassword() {
      this.editingPassword = false
      this.passwordForm = {
        currentPassword: '',
        newPassword: '',
        confirmPassword: ''
      }
    }
  }
}
</script>

<style scoped>
.my-profile {
  padding: 2rem;
  max-width: 900px;
  margin: 0 auto;
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

.profile-content {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.tab-content {
  padding: 1.5rem 0;
}

.info-form,
.password-form {
  max-width: 500px;
}

.info-group {
  margin-bottom: 1.5rem;
}

.info-group label {
  display: block;
  margin-bottom: 0.5rem;
  color: #2c3e50;
  font-weight: 600;
  font-size: 0.9rem;
}

.action-buttons {
  margin-top: 2rem;
  display: flex;
  gap: 1rem;
}

@media (max-width: 768px) {
  .profile-card {
    flex-direction: column;
    text-align: center;
  }
}
</style>
