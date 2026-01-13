<template>
  <div class="register-page">
    <div class="register-box">
      <h2>注册</h2>
      <form @submit.prevent="handleRegister">
        <input v-model="username" type="text" placeholder="用户名" required>
        <input v-model="email" type="email" placeholder="邮箱" required>
        <input v-model="password" type="password" placeholder="密码" required>
        <input v-model="confirmPassword" type="password" placeholder="确认密码" required>
        <button type="submit">注册</button>
      </form>
      <router-link to="/login">已有账户，去登录</router-link>
    </div>
  </div>
</template>

<script>
export default {
  name: 'RegisterPage',
  data() {
    return {
      username: '',
      email: '',
      password: '',
      confirmPassword: ''
    }
  },
  methods: {
    handleRegister() {
      if (this.password !== this.confirmPassword) {
        alert('密码不一致')
        return
      }
      alert('注册成功')
      this.$router.push('/login')
    }
  }
}
</script>

<style scoped>
.register-page {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: #f5f5f5;
}
.register-box {
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
</style>
