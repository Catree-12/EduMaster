// 合并并整理所有服务
import http from './http'

// 用户相关
export const userService = {
  getProfile: () => http.get('/users/profile'),
  updateProfile: (data) => http.put('/users/profile', data),
  changePassword: (data) => http.post('/users/change-password', data),
  getStatistics: () => http.get('/users/statistics'),
  uploadAvatar: (file) => {
    const formData = new FormData()
    formData.append('avatar', file)
    return http.post('/users/avatar', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
  }
}

// 课程相关 - 统一接口
export const courseService = {
  // 列表和详情
  getList: (params) => http.get('/courses', { params }),
  getDetail: (id) => http.get(`/courses/${id}`),
  
  // CRUD操作
  create: (data) => http.post('/courses', data),
  update: (id, data) => http.put(`/courses/${id}`, data),
  delete: (id) => http.delete(`/courses/${id}`),
  
  // 用户课程
  getEnrolled: (params) => http.get('/courses/enrolled', { params }),
  getTeaching: (params) => http.get('/courses/teaching', { params }),
  getPending: (params) => http.get('/courses/pending', { params }),
  
  // 课程操作
  enroll: (id) => http.post(`/courses/${id}/enroll`),
  unenroll: (id) => http.post(`/courses/${id}/unenroll`),
  publish: (id) => http.post(`/courses/${id}/publish`),
  
  // 课程资源
  getResources: (id) => http.get(`/courses/${id}/resources`),
  getStudents: (id, params) => http.get(`/courses/${id}/students`, { params })
}

// 社区相关
export const communityService = {
  getPosts: (params) => Vue.prototype.$http.get('/community/posts', { params }),
  getPostDetail: (id) => Vue.prototype.$http.get(`/community/posts/${id}`),
  createPost: (data) => Vue.prototype.$http.post('/community/posts', data),
  getHotTopics: () => Vue.prototype.$http.get('/community/hot-topics'),
  likePost: (id) => Vue.prototype.$http.post(`/community/posts/${id}/like`)
}

// 管理员相关
export const adminService = {
  getPendingCourses: (params) => Vue.prototype.$http.get('/admin/courses/pending', { params }),
  approveCourse: (id) => Vue.prototype.$http.post(`/admin/courses/${id}/approve`),
  rejectCourse: (id, data) => Vue.prototype.$http.post(`/admin/courses/${id}/reject`, data)
}
