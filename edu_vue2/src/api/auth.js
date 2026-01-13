import http from './http'

export const authAPI = {
  // 注册
  register(data) {
    return http.post('/auth/register', data)
  },

  // 登录
  login(data) {
    return http.post('/auth/login', data)
  },

  // 忘记密码
  forgetPassword(email) {
    return http.post('/auth/forget-password', { email })
  },

  // 重置密码
  resetPassword(data) {
    return http.post('/auth/reset-password', data)
  },

  // 修改密码
  changePassword(data) {
    return http.post('/auth/change-password', data)
  },

  // 获取当前用户信息
  getCurrentUser() {
    return http.get('/auth/current-user')
  },

  // 登出
  logout() {
    return http.post('/auth/logout')
  }
}
