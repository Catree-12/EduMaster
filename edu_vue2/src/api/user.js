import http from './http'

export const userAPI = {
  // 获取用户信息
  getUserInfo(userId) {
    return http.get(`/users/${userId}`)
  },

  // 更新用户信息
  updateUserInfo(data) {
    return http.put('/users/profile', data)
  },

  // 上传头像
  uploadAvatar(file) {
    const formData = new FormData()
    formData.append('avatar', file)
    return http.post('/users/avatar', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
  },

  // 获取学习进度
  getLearningProgress() {
    return http.get('/users/learning-progress')
  },

  // 获取成绩统计
  getGradeStats() {
    return http.get('/users/grade-stats')
  }
}
