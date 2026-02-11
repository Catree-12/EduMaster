import http from './http'

/**
 * 课程公共API - 仅包含公开的课程操作
 * 教师课程管理请使用 teacher.js
 * 学生课程学习请使用 student.js
 */
export const courseAPI = {
  // ==================== 公开课程接口 ====================
  
  /**
   * 获取课程列表(公开)
   * GET /api/courses/
   * @param {Object} params - 查询参数
   *   - page: 页码
   *   - pageSize: 每页数量
   *   - category: 分类名称
   *   - keyword: 搜索关键词
   * @returns {Promise} 返回格式: {results: [], count, next, previous, page, pageSize, totalPages}
   */
  getCourseList(params) {
    return http.get('/courses/', { params })
  },

  /**
   * 获取课程详情(公开)
   */
  getCourseDetail(courseId) {
    return http.get(`/courses/${courseId}`)
  },

  // 获取课程资源（公开）
  // getCourseResources(courseId) {
  //   return http.get(`/courses/${courseId}/resources`)
  // },
  
  // ==================== 已选课程 ====================
  
  // 获取我的课程（需要登录）
  getMyCourses(params) {
    return http.get('/courses/mycourses/', { params })
  },

  // ==================== 选课管理 ====================
  
  /**
   * 获取课程班期班级信息（选课前）
   * GET /api/courses/{course_id}/enrollment/
   * @param {String|Number} courseId - 课程ID
   * @returns {Promise} 返回课程、班期、班级信息
   */
  getEnrollmentInfo(courseId) {
    return http.get(`/courses/${courseId}/enrollment/`)
  },

  /**
   * 选课
   * POST /api/courses/{course_id}/enrollment/
   * @param {String|Number} courseId - 课程ID
   * @param {Object} data - { term_id, class_id? }
   * @returns {Promise} 返回选课结果
   */
  enrollCourse(courseId, data) {
    return http.post(`/courses/${courseId}/enrollment/`, data)
  },

  /**
   * 退课
   * DELETE /api/courses/{course_id}/enrollment/
   * @param {String|Number} courseId - 课程ID
   * @returns {Promise}
   */
  unenrollCourse(courseId) {
    return http.delete(`/courses/${courseId}/enrollment/`)
  }
}
