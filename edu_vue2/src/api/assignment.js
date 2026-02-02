import http from './http'

/**
 * 作业公共API
 * 教师作业管理请使用 teacher.js 中的作业相关方法
 * 学生作业提交请使用 student.js 中的作业相关方法
 * 
 * 本文件仅包含通用的作业操作（如果后端有这些端点的话）
 * 注意：如果使用 teacher.js 和 student.js，本文件可能不需要使用
 */
export const assignmentAPI = {
  // 获取作业详情（公开）
  getAssignmentDetail(assignmentId) {
    return http.get(`/assignments/${assignmentId}`)
  }
}
