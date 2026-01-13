import http from './http'

export const examAPI = {
  // 获取课程的考试列表
  getExamList(courseId, params) {
    return http.get(`/courses/${courseId}/exams`, { params })
  },

  // 获取考试详情
  getExamDetail(examId) {
    return http.get(`/exams/${examId}`)
  },

  // 创建考试（老师）
  createExam(courseId, data) {
    return http.post(`/courses/${courseId}/exams`, data)
  },

  // 编辑考试（老师）
  updateExam(examId, data) {
    return http.put(`/exams/${examId}`, data)
  },

  // 删除考试（老师）
  deleteExam(examId) {
    return http.delete(`/exams/${examId}`)
  },

  // 开始考试（学生获取题目）
  startExam(examId) {
    return http.post(`/exams/${examId}/start`)
  },

  // 提交考试答案
  submitExam(examId, data) {
    return http.post(`/exams/${examId}/submit`, data)
  },

  // 获取考试成绩
  getExamResult(examId) {
    return http.get(`/exams/${examId}/result`)
  },

  // 获取用户的所有考试成绩
  getUserExamResults(params) {
    return http.get('/exams/results', { params })
  }
}
