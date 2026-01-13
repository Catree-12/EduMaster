import http from './http'

export const adminAPI = {
  // ==================== 仪表板 ====================
  
  // 获取平台统计数据
  getDashboardStats() {
    return http.get('/admin/dashboard/stats')
  },

  // 获取待处理任务
  getPendingTasks() {
    return http.get('/admin/dashboard/pending-tasks')
  },

  // ==================== 课程审核 ====================
  
  // 获取待审核课程列表
  getPendingCourses(params) {
    return http.get('/admin/courses/pending', { params })
  },

  // 获取课程审核列表
  getCourseAuditList(params) {
    return http.get('/admin/courses/audit-list', { params })
  },

  // 获取课程审核详情
  getCourseAuditDetail(courseId) {
    return http.get(`/admin/courses/${courseId}/audit-detail`)
  },

  // 审核通过课程
  approveCourse(courseId, data) {
    return http.post(`/admin/courses/${courseId}/approve`, data)
  },

  // 拒绝课程
  rejectCourse(courseId, data) {
    return http.post(`/admin/courses/${courseId}/reject`, data)
  },

  // ==================== 用户管理 ====================
  
  // 获取所有用户
  getAllUsers(params) {
    return http.get('/admin/users', { params })
  },

  // 获取用户详情
  getUserDetail(userId) {
    return http.get(`/admin/users/${userId}`)
  },

  // 更新用户信息
  updateUser(userId, data) {
    return http.put(`/admin/users/${userId}`, data)
  },

  // 禁用用户
  disableUser(userId, data) {
    return http.post(`/admin/users/${userId}/disable`, data)
  },

  // 启用用户
  enableUser(userId) {
    return http.post(`/admin/users/${userId}/enable`)
  },

  // 批量禁用用户
  batchDisableUsers(data) {
    return http.post('/admin/users/batch-disable', data)
  },

  // 批量启用用户
  batchEnableUsers(data) {
    return http.post('/admin/users/batch-enable', data)
  },

  // 导出用户数据
  exportUsers(params) {
    return http.get('/admin/users/export', { params, responseType: 'blob' })
  },

  // 禁用/启用用户 (兼容旧代码)
  toggleUserStatus(userId) {
    return http.post(`/admin/users/${userId}/toggle-status`)
  },

  // ==================== 内容审核 ====================
  
  // 获取举报列表
  getReportList(params) {
    return http.get('/admin/reports', { params })
  },

  // 获取举报详情
  getReportDetail(reportId) {
    return http.get(`/admin/reports/${reportId}`)
  },

  // 删除被举报内容
  deleteReportedContent(reportId, data) {
    return http.post(`/admin/reports/${reportId}/delete-content`, data)
  },

  // 驳回举报
  rejectReport(reportId, data) {
    return http.post(`/admin/reports/${reportId}/reject`, data)
  },

  // ==================== 证书管理 ====================
  
  // 获取证书列表
  getCertificateList(params) {
    return http.get('/admin/certificates', { params })
  },

  // 获取证书详情
  getCertificateDetail(certId) {
    return http.get(`/admin/certificates/${certId}`)
  },

  // 撤销证书
  revokeCertificate(certId, data) {
    return http.post(`/admin/certificates/${certId}/revoke`, data)
  },

  // 导出证书数据
  exportCertificates(params) {
    return http.get('/admin/certificates/export', { params, responseType: 'blob' })
  },

  // ==================== 数据统计 ====================
  
  // 获取统计指标
  getAnalyticsMetrics(params) {
    return http.get('/admin/analytics/metrics', { params })
  },

  // 获取用户增长数据
  getUserGrowthData(params) {
    return http.get('/admin/analytics/user-growth', { params })
  },

  // 获取课程分类分布
  getCourseDistribution() {
    return http.get('/admin/analytics/course-distribution')
  },

  // 获取热门课程
  getPopularCourses(params) {
    return http.get('/admin/analytics/popular-courses', { params })
  },

  // 获取学习活跃度
  getLearningActivity(params) {
    return http.get('/admin/analytics/learning-activity', { params })
  },

  // 导出统计数据
  exportAnalyticsData(params) {
    return http.get('/admin/analytics/export', { params, responseType: 'blob' })
  },

  // ==================== 系统设置 ====================
  
  // 获取系统设置
  getSystemSettings(category) {
    return http.get('/admin/settings', { params: { category } })
  },

  // 更新系统设置
  updateSystemSettings(category, data) {
    return http.put('/admin/settings', { category, settings: data })
  },

  // 发送测试邮件
  sendTestEmail(data) {
    return http.post('/admin/settings/test-email', data)
  },

  // 上传Logo
  uploadLogo(formData) {
    return http.post('/admin/settings/upload-logo', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
  },

  // 上传证书模板
  uploadCertificateTemplate(formData) {
    return http.post('/admin/settings/upload-cert-template', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
  },

  // ==================== 操作日志 ====================
  
  // 获取操作日志
  getOperationLogs(params) {
    return http.get('/admin/logs', { params })
  }
}

