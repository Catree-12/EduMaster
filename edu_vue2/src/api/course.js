import http from './http'

/**
 * 课程公共API - 仅包含公开的课程操作
 * 教师课程管理请使用 teacher.js
 * 学生课程学习请使用 student.js
 */
export const courseAPI = {
  // ==================== 公开课程接口 ====================
  
  // 获取课程列表（公开）
  getCourseList(params) {
    return http.get('/courses', { params })
  },

  // 获取课程详情（公开）
  getCourseDetail(courseId) {
    return http.get(`/courses/${courseId}`)
  },

  // 获取课程资源（公开）
  getCourseResources(courseId) {
    return http.get(`/courses/${courseId}/resources`)
  },
  
  // ==================== 已选课程 ====================
  
  // 获取我的课程（需要登录）
  getMyCourses(params) {
    return http.get('/courses/my-courses', { params })
  }
}
