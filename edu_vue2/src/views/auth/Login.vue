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
      this.loading = true
      try {
        // TODO: 调用登录 API
        // const response = await this.$api.post('/auth/login', this.form)
        
        // 临时演示数据 - 根据邮箱判断角色
        let role = 'user'
        if (this.form.email === 'admin@platform.com' || this.form.email.includes('admin')) {
          role = 'admin'
        }
        
        const mockResponse = {
          token: 'mock-token-' + Date.now(),
          user: {
            id: role === 'admin' ? 'admin_001' : Date.now(),
            name: this.form.email.split('@')[0],
            email: this.form.email,
            avatar: ''
          },
          role: role // 后端返回：'user' 或 'admin'
        }
        
        // 同步更新 Vuex 状态和 localStorage
        await this.$store.dispatch('user/login', {
          token: mockResponse.token,
          userInfo: mockResponse.user,
          role: mockResponse.role
        })
        
        this.$message.success('登录成功')
        
        // 根据角色跳转到不同页面
        if (mockResponse.role === 'admin') {
          this.$router.push('/admin/dashboard')
        } else {
          this.$router.push('/')
        }
      } catch (error) {
        this.$message.error('登录失败：' + error.message)
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
