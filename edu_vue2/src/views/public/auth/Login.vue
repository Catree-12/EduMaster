<template>
  <div class="login-container">
    <div class="login-box">
      <h1>登录</h1>
      
      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label for="email">邮箱</label>
          <input 
            v-model="form.email" 
            type="email" 
            id="email"
            placeholder="请输入邮箱"
            required
          >
        </div>

        <div class="form-group">
          <label for="password">密码</label>
          <input 
            v-model="form.password" 
            type="password" 
            id="password"
            placeholder="请输入密码"
            required
          >
        </div>

        <div class="form-options">
          <label>
            <input type="checkbox" v-model="form.rememberMe">
            记住我
          </label>
          <router-link to="/forgot-password">忘记密码？</router-link>
        </div>

        <button type="submit" class="login-btn" :disabled="loading">
          {{ loading ? '登录中...' : '登录' }}
        </button>
      </form>

      <p class="signup-link">
        还没有账号？<router-link to="/register">立即注册</router-link>
      </p>
    </div>
  </div>
</template>

<script>
import { authAPI } from '@/api'

export default {
  name: 'UserLogin',
  data() {
    return {
      form: {
        email: '',
        password: '',
        rememberMe: false
      },
      loading: false
    }
  },
  methods: {
    async handleLogin() {
  // 1. 基本前端校验
  if (!this.form.email || !this.form.password) {
    this.$message.warning('请输入邮箱和密码')
    return
  }

  this.loading = true
  
  // 【关键一步】登录前先彻底清理旧 Token
  // 防止 http.js 拦截器自动带上之前过期的 Token 导致后端报 401
  localStorage.removeItem('token')
  localStorage.clear()

  try {
    // 2. 调用登录 API
    // 假设返回结构：{ access: '...', refresh: '...', user: { is_staff: true, username: '...' } }
    const response = await authAPI.login({
      email: this.form.email,
      password: this.form.password
    })

    // 3. 更新 Vuex 状态 (保存 Token 和用户信息)
    await this.$store.dispatch('user/login', response)

  this.$message({
    message: '登录成功！',
    type: 'success',
    duration: 500  // 设置为 1.5 秒后自动关闭
  });

    // 4. 根据是否是管理员进行跳转
    // 使用 getter 判断是否是管理员
    if (this.$store.getters['user/isAdmin']) {
      // 管理员进入管理后台
      this.$router.push('/admin/dashboard')
    } else {
      // 普通用户跳转到首页
      this.$router.push('/')
    }

  } catch (error) {
    console.error('登录逻辑异常:', error)
    
    // 获取后端返回的错误详情
    const serverMessage = error.response?.data?.detail || error.response?.data?.message
    if (serverMessage) {
      this.$message.error(serverMessage)
    } else {
      this.$message.error('登录失败，请检查网络或账号密码')
    }
  } finally {
    this.loading = false
  }
}
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.login-box {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
}

.login-box h1 {
  text-align: center;
  color: #2c3e50;
  margin-bottom: 2rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  color: #2c3e50;
  font-weight: 500;
}

.form-group input[type="email"],
.form-group input[type="password"] {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #bdc3c7;
  border-radius: 4px;
  font-size: 1rem;
  box-sizing: border-box;
}

.form-group input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.form-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  font-size: 0.875rem;
}

.form-options a {
  color: #667eea;
  text-decoration: none;
}

.form-options a:hover {
  text-decoration: underline;
}

.login-btn {
  width: 100%;
  padding: 0.75rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: opacity 0.3s;
}

.login-btn:hover:not(:disabled) {
  opacity: 0.9;
}

.login-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.signup-link {
  text-align: center;
  margin-top: 1.5rem;
  color: #7f8c8d;
}

.signup-link a {
  color: #667eea;
  text-decoration: none;
  font-weight: 600;
}

.signup-link a:hover {
  text-decoration: underline;
}
</style>
