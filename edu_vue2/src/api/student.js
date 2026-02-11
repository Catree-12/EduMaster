import http from './http'

/**
 * 学生相关API
 */

// 注意：选课相关API已迁移到 course.js
// 请使用 courseAPI.getEnrollmentInfo(), courseAPI.enrollCourse(), courseAPI.unenrollCourse()

// ==================== 课程学习 ====================
export const getStudentCourse = (courseId) => {
  return http.get(`/student/courses/${courseId}`)
}

export const updateLearningProgress = (courseId, data) => {
  return http.post(`/student/courses/${courseId}/progress`, data)
}

export const getStudentLesson = (courseId, lessonId) => {
  return http.get(`/student/courses/${courseId}/lessons/${lessonId}`)
}

export const completeLessonStudy = (courseId, lessonId) => {
  return http.post(`/student/courses/${courseId}/lessons/${lessonId}/complete`)
}

// ==================== 作业 ====================
export const getStudentHomeworkList = (params) => {
  return http.get('/student/homework', { params })
}

export const getStudentHomework = (courseId, homeworkId) => {
  return http.get(`/student/courses/${courseId}/homework/${homeworkId}`)
}

export const submitHomework = (courseId, homeworkId, data) => {
  return http.post(`/student/courses/${courseId}/homework/${homeworkId}/submit`, data)
}

export const getStudentHomeworkSubmission = (courseId, homeworkId) => {
  return http.get(`/student/courses/${courseId}/homework/${homeworkId}/submission`)
}

// ==================== 考试 ====================
export const getStudentExamList = (params) => {
  return http.get('/student/exams', { params })
}

export const getStudentExam = (courseId, examId) => {
  return http.get(`/student/courses/${courseId}/exams/${examId}`)
}

export const startExam = (courseId, examId) => {
  return http.post(`/student/courses/${courseId}/exams/${examId}/start`)
}

export const submitExam = (courseId, examId, data) => {
  return http.post(`/student/courses/${courseId}/exams/${examId}/submit`, data)
}

export const getStudentExamResult = (courseId, examId) => {
  return http.get(`/student/courses/${courseId}/exams/${examId}/result`)
}

// ==================== 课程社区 ====================
export const getStudentCourseThreads = (courseId, params) => {
  return http.get(`/student/courses/${courseId}/threads`, { params })
}

export const getStudentThread = (courseId, threadId) => {
  return http.get(`/student/courses/${courseId}/threads/${threadId}`)
}

export const createStudentThread = (courseId, data) => {
  return http.post(`/student/courses/${courseId}/threads`, data)
}

export const updateStudentThread = (courseId, threadId, data) => {
  return http.put(`/student/courses/${courseId}/threads/${threadId}`, data)
}

export const deleteStudentThread = (courseId, threadId) => {
  return http.delete(`/student/courses/${courseId}/threads/${threadId}`)
}

export const createStudentThreadComment = (courseId, threadId, data) => {
  return http.post(`/student/courses/${courseId}/threads/${threadId}/comments`, data)
}
