<template>
  <div class="register-container">
    <div class="register-box">
      <h1>注册新账号</h1>
      
      <form @submit.prevent="handleRegister">
        <div class="form-group">
          <label for="real_name">用户名</label>
          <input 
            v-model="form.real_name" 
            type="text" 
            id="real_name"
            placeholder="请输入用户名"
            required
          >
        </div>

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
            placeholder="请输入密码（至少8位）"
            required
          >
        </div>

        <div class="form-group">
          <label for="confirmPassword">确认密码</label>
          <input 
            v-model="form.confirmPassword" 
            type="password" 
            id="confirmPassword"
            placeholder="再次输入密码"
            required
          >
        </div>

        <button type="submit" class="register-btn" :disabled="loading">
          {{ loading ? '注册中...' : '注册' }}
        </button>
      </form>

      <p class="login-link">
        已有账号？<router-link to="/login">立即登录</router-link>
      </p>
    </div>
  </div>
</template>

<script>
import { authAPI } from '@/api'
export default {
  name: 'UserRegister',
  data() {
    return {
      form: {
        real_name: '',
        email: '',
        password: '',
        confirmPassword: ''
      },
      loading: false
    }
  },
  methods: {
    async handleRegister() {
      // 1. 本地逻辑校验：密码一致性
      if (this.form.password !== this.form.confirmPassword) {
        this.$message.error('两次输入的密码不一致')
        return
      }

      this.loading = true
      try {
        // 2. 真正发送请求到后端
        // 建议只发送后端需要的字段
        const submitData = {
          real_name: this.form.real_name,
          email: this.form.email,
          password: this.form.password
        }

        // 调用我们在 main.js 挂载的 $http (即 http.js 实例)
        // await this.$http.post('/auth/register/', submitData)
        await authAPI.register(submitData)

        this.$message.success('注册成功，请登录')
        this.$router.push('/login')
      } catch (error) {
        // 错误通常会被 http.js 的拦截器统一处理弹出消息
        // 如果拦截器没处理，可以在这里补上：
        // this.$message.error(error.response?.data?.message || '注册失败')
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>
.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 2rem 0;
}

.register-box {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 450px;
}

.register-box h1 {
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

.form-group input[type="text"],
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

.register-btn {
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
  margin-top: 1rem;
}

.register-btn:hover:not(:disabled) {
  opacity: 0.9;
}

.register-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.login-link {
  text-align: center;
  margin-top: 1.5rem;
  color: #7f8c8d;
}

.login-link a {
  color: #667eea;
  text-decoration: none;
  font-weight: 600;
}

.login-link a:hover {
  text-decoration: underline;
}
</style>