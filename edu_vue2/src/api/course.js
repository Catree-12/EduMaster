import http from './http'

export const courseAPI = {
  // 获取课程列表
  getCourseList(params) {
    return http.get('/courses', { params })
  },

  // 获取课程详情
  getCourseDetail(courseId) {
    return http.get(`/courses/${courseId}`)
  },

  // 获取我的课程
  getMyCourses(params) {
    return http.get('/courses/my-courses', { params })
  },

  // 创建课程
  createCourse(data) {
    return http.post('/courses', data)
  },

  // 编辑课程
  updateCourse(courseId, data) {
    return http.put(`/courses/${courseId}`, data)
  },

  // 删除课程
  deleteCourse(courseId) {
    return http.delete(`/courses/${courseId}`)
  },

  // 选课
  enrollCourse(courseId) {
    return http.post(`/courses/${courseId}/enroll`)
  },

  // 退课
  unenrollCourse(courseId) {
    return http.post(`/courses/${courseId}/unenroll`)
  },

  // 发布课程（申请审核）
  publishCourse(courseId) {
    return http.post(`/courses/${courseId}/publish`)
  },

  // 获取课程资源
  getCourseResources(courseId) {
    return http.get(`/courses/${courseId}/resources`)
  },

  // 获取课程学生列表
  getCourseStudents(courseId, params) {
    return http.get(`/courses/${courseId}/students`, { params })
  }
}
