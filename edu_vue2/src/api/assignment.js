import http from './http'

export const assignmentAPI = {
  // 获取课程的作业列表
  getAssignmentList(courseId, params) {
    return http.get(`/courses/${courseId}/assignments`, { params })
  },

  // 获取作业详情
  getAssignmentDetail(assignmentId) {
    return http.get(`/assignments/${assignmentId}`)
  },

  // 创建作业（老师）
  createAssignment(courseId, data) {
    return http.post(`/courses/${courseId}/assignments`, data)
  },

  // 编辑作业（老师）
  updateAssignment(assignmentId, data) {
    return http.put(`/assignments/${assignmentId}`, data)
  },

  // 删除作业（老师）
  deleteAssignment(assignmentId) {
    return http.delete(`/assignments/${assignmentId}`)
  },

  // 提交作业
  submitAssignment(assignmentId, data) {
    return http.post(`/assignments/${assignmentId}/submit`, data)
  },

  // 获取作业提交记录
  getSubmissions(assignmentId, params) {
    return http.get(`/assignments/${assignmentId}/submissions`, { params })
  },

  // 批改作业
  gradeSubmission(submissionId, data) {
    return http.post(`/submissions/${submissionId}/grade`, data)
  }
}
