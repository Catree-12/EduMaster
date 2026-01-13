<template>
  <div class="login-page">
    <div class="login-box">
      <h2>登录</h2>
      <form @submit.prevent="handleLogin">
        <input v-model="email" type="email" placeholder="邮箱" required>
        <input v-model="password" type="password" placeholder="密码" required>
        <button type="submit">登录</button>
      </form>
      <router-link to="/register">注册</router-link>
    </div>
  </div>
</template>

<script>
export default {
  name: 'LoginPage',
  data() {
    return {
      email: '',
      password: ''
    }
  },
  methods: {
    handleLogin() {
      localStorage.setItem('token', 'test-token')
      this.$router.push('/courses')
    }
  }
}
</script>

<style scoped>
.login-page {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: #f5f5f5;
}
.login-box {
  background: white;
  padding: 40px;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.1);
  width: 100%;
  max-width: 400px;
}
h2 {
  text-align: center;
  margin-bottom: 30px;
}
input {
  width: 100%;
  padding: 12px;
  margin-bottom: 15px;
  border: 1px solid #ddd;
  border-radius: 4px;
  box-sizing: border-box;
}
button {
  width: 100%;
  padding: 12px;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
button:hover {
  background: #5568d3;
}
</style>
