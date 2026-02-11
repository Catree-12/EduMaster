import http from './http'

/**
 * 用户认证 API
 * 对接后端 apps/users/ 模块
 * 
 * 后端路径规范：
 * - 前端 baseURL: http://localhost:8000/api
 * - 后端 URL 配置: /api/auth/*
 */
export const authAPI = {
  /**
   * 用户注册
   * POST /api/auth/register/
   * @param {Object} data - { username, email, password, password_confirm, role }
   */
  register(data) {
    return http.post('/auth/register/', data)
  },

  /**
   * 用户登录 (JWT)
   * POST /api/auth/login/
   * @param {Object} data - { email, password }
   * @returns {Promise} { token, refresh_token, user: { id, username, email, role, avatar, ... } }
   */
  login(data) {
    return http.post('/auth/login/', data)
  },

  /**
   * 用户登出
   * POST /api/auth/logout/
   * 前端需销毁 Token
   */
  logout() {
    return http.post('/auth/logout/')
  },

  /**
   * 忘记密码（发送重置邮件）
   * POST /api/auth/forget-password/
   * @param {Object} data - { email }
   */
  forgetPassword(data) {
    return http.post('/auth/forget-password/', data)
  },

  /**
   * 修改密码(已登录用户)
   * POST /api/auth/change-password/
   * @param {Object} data - { old_password, new_password, new_password_confirm }
   */
  changePassword(data) {
    return http.post('/auth/change-password/', data)
  },

  /**
   * 刷新访问令牌
   * POST /api/auth/refresh/
   * @param {Object} data - { refresh: refresh_token }
   * @returns {Promise} { access: new_access_token }
   */
  refreshToken(refreshToken) {
    return http.post('/auth/refresh/', { refresh: refreshToken })
  }
}


