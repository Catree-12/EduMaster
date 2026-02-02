import http from './http'

/**
 * 考试公共API
 * 教师考试管理请使用 teacher.js 中的考试相关方法
 * 学生考试答题请使用 student.js 中的考试相关方法
 * 
 * 本文件仅包含通用的考试操作（如果后端有这些端点的话）
 * 注意：如果使用 teacher.js 和 student.js，本文件可能不需要使用
 */
export const examAPI = {
  // 获取考试详情（公开）
  getExamDetail(examId) {
    return http.get(`/exams/${examId}`)
  }
}
