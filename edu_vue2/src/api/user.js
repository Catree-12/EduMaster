import http from './http'

/**
 * 用户信息管理 API
 * 对接后端 apps/users/ 模块
 * 
 * 用户模型字段说明：
 * - real_name: 用户名/真实姓名（可更新）
 * - nickname: 昵称（可更新）
 * - email: 邮箱（只读，不可修改）
 * - phone: 手机号（可更新）
 * - avatar: 头像（通过独立的上传接口更新）
 * - bio: 个人简介（可更新）
 * - gender: 性别 (male/female/secret)（可更新）
 * - school: 学校（可更新）
 * - major: 专业（可更新）
 * - student_id: 学号（只读，系统分配）
 * - teacher_id: 工号（只读，系统分配）
 */
export const userAPI = {
  // /**
  //  * 获取当前登录用户基本信息
  //  * GET /api/users/me/
  //  * 用于获取当前用户的基本信息（登录后立即获取）
  //  */
  // getCurrentUser() {
  //   return http.get('/users/me/')
  // },

  /**
   * 获取用户详情
   * GET /api/users/{id}/
   */
  getUserInfo(userId) {
    return http.get(`/users/${userId}/`)
  },

  /**
   * 获取当前用户完整信息
   * GET /api/users/profile/
   * 包含 student_profile 或 teacher_profile（更详细的信息）
   */
  getCurrentUserProfile() {
    return http.get('/users/profile/')
  },

  /**
   * 更新用户基本信息
   * PUT /api/users/profile/
   * @param {Object} data - 可更新字段（对应后端updatable_fields）：
   *   - real_name: 用户名/真实姓名
   *   - nickname: 昵称
   *   - bio: 个人简介
   *   - gender: 性别 (male/female/secret)
   *   - school: 学校
   *   - major: 专业
   *   - phone: 手机号
   * 注意：email、student_id 和 teacher_id 不可更新
   */
  updateUserInfo(data) {
    return http.put('/users/profile/', data)
  },

  /**
   * 上传用户头像（独立接口）
   * POST /api/users/avatar/
   * @param {File} file - 头像文件
   * @returns {Promise} 返回格式: {code: 200, message: '上传成功', data: {avatar: 'url'}}
   */
  uploadAvatar(file) {
    const formData = new FormData()
    formData.append('avatar', file)
    return http.post('/users/avatar/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
  },

  /**
   * 获取用户学习统计
   * GET /api/users/stats/learning/
   */
  getLearningStats() {
    return http.get('/users/stats/learning/')
  },

  /**
   * 获取用户成绩统计
   * GET /api/users/stats/grades/
   */
  getGradeStats() {
    return http.get('/users/stats/grades/')
  },

  /**
   * 获取证书统计信息
   * GET /api/users/stats/certificates/
   */
  getCertificateStats() {
    return http.get('/users/stats/certificates/')
  },

  /**
   * 获取用户证书列表
   * GET /api/users/certificates/
   */
  getCertificates(params) {
    return http.get('/users/certificates/', { params })
  },

  /**
   * 获取证书详情
   * GET /api/users/certificates/{id}/
   */
  getCertificateDetail(certificateId) {
    return http.get(`/users/certificates/${certificateId}/`)
  },

  /**
   * 生成课程证书
   * POST /api/users/courses/{courseId}/certificate/
   */
  generateCourseCertificate(courseId) {
    return http.post(`/users/courses/${courseId}/certificate/`)
  },

  /**
   * 生成证书分享链接
   * POST /api/users/certificates/{id}/share/
   */
  generateCertificateShareLink(certificateId, data) {
    return http.post(`/users/certificates/${certificateId}/share/`, data)
  },

  /**
   * 下载证书
   * GET /api/users/certificates/{id}/download/
   */
  downloadCertificate(certificateId) {
    return http.get(`/users/certificates/${certificateId}/download/`, {
      responseType: 'blob'
    })
  },

  /**
   * 获取用户消息列表
   * GET /api/users/messages/
   */
  getMessages(params) {
    return http.get('/users/messages/', { params })
  },

  /**
   * 标记消息为已读
   * POST /api/users/messages/{id}/read/
   */
  markMessageAsRead(messageId) {
    return http.post(`/users/messages/${messageId}/read/`)
  }
}


