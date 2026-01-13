<template>
  <div class="register-container">
    <div class="register-box">
      <h1>注册新账号</h1>
      
      <form @submit.prevent="handleRegister">
        <div class="form-group">
          <label for="username">用户名</label>
          <input 
            v-model="form.username" 
            type="text" 
            id="username"
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

        <div class="form-group checkbox">
          <label>
            <input type="checkbox" v-model="form.agreeTerms" required>
            我同意<a href="#">用户协议</a>和<a href="#">隐私政策</a>
          </label>
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
export default {
  name: 'UserRegister',
  data() {
    return {
      form: {
        username: '',
        email: '',
        password: '',
        confirmPassword: '',
        agreeTerms: false
      },
      loading: false
    }
  },
  methods: {
    async handleRegister() {
      if (this.form.password !== this.form.confirmPassword) {
        this.$message.error('两次输入的密码不一致')
        return
      }

      this.loading = true
      try {
        // TODO: 调用注册 API
        // const response = await this.$api.post('/auth/register', this.form)
        this.$message.success('注册成功，请登录')
        this.$router.push('/login')
      } catch (error) {
        this.$message.error('注册失败：' + error.message)
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

.form-group.checkbox label {
  display: flex;
  align-items: center;
  cursor: pointer;
}

.form-group.checkbox input {
  margin-right: 0.5rem;
}

.form-group.checkbox a {
  color: #667eea;
  text-decoration: none;
}

.form-group.checkbox a:hover {
  text-decoration: underline;
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
