import http from './http'

/**
 * 教师相关API
 */

// ==================== 课程管理 ====================
export const getTeacherCourses = (params) => {
  return http.get('/teacher/courses', { params })
}

export const getTeacherCourse = (courseId) => {
  return http.get(`/teacher/courses/${courseId}`)
}

export const createCourse = (data) => {
  return http.post('/teacher/courses', data)
}

export const updateCourse = (courseId, data) => {
  return http.put(`/teacher/courses/${courseId}`, data)
}

export const deleteCourse = (courseId) => {
  return http.delete(`/teacher/courses/${courseId}`)
}

export const publishCourse = (courseId) => {
  return http.post(`/teacher/courses/${courseId}/publish`)
}

// ==================== 章节管理 ====================
export const getCourseChapters = (courseId) => {
  return http.get(`/teacher/courses/${courseId}/chapters`)
}

export const createChapter = (courseId, data) => {
  return http.post(`/teacher/courses/${courseId}/chapters`, data)
}

export const updateChapter = (courseId, chapterId, data) => {
  return http.put(`/teacher/courses/${courseId}/chapters/${chapterId}`, data)
}

export const deleteChapter = (courseId, chapterId) => {
  return http.delete(`/teacher/courses/${courseId}/chapters/${chapterId}`)
}

export const sortChapters = (courseId, data) => {
  return http.post(`/teacher/courses/${courseId}/chapters/sort`, data)
}

// ==================== 学生管理 ====================
export const getCourseStudents = (courseId, params) => {
  return http.get(`/teacher/courses/${courseId}/students`, { params })
}

export const getStudentProgress = (courseId, studentId) => {
  return http.get(`/teacher/courses/${courseId}/students/${studentId}/progress`)
}

// ==================== 学期与班级 ====================
export const getCourseTerms = (courseId) => {
  return http.get(`/teacher/courses/${courseId}/terms`)
}

export const createTerm = (courseId, data) => {
  return http.post(`/teacher/courses/${courseId}/terms`, data)
}

export const updateTerm = (courseId, termId, data) => {
  return http.put(`/teacher/courses/${courseId}/terms/${termId}`, data)
}

export const deleteTerm = (courseId, termId) => {
  return http.delete(`/teacher/courses/${courseId}/terms/${termId}`)
}

export const getCourseClasses = (courseId, params) => {
  return http.get(`/teacher/courses/${courseId}/classes`, { params })
}

export const createClass = (courseId, data) => {
  return http.post(`/teacher/courses/${courseId}/classes`, data)
}

export const updateClass = (courseId, classId, data) => {
  return http.put(`/teacher/courses/${courseId}/classes/${classId}`, data)
}

export const deleteClass = (courseId, classId) => {
  return http.delete(`/teacher/courses/${courseId}/classes/${classId}`)
}

// ==================== 作业管理 ====================
export const getTeacherHomework = (params) => {
  return http.get('/teacher/homework', { params })
}

export const getHomeworkDetail = (homeworkId) => {
  return http.get(`/teacher/homework/${homeworkId}`)
}

export const createHomework = (data) => {
  return http.post('/teacher/homework', data)
}

export const updateHomework = (homeworkId, data) => {
  return http.put(`/teacher/homework/${homeworkId}`, data)
}

export const deleteHomework = (homeworkId) => {
  return http.delete(`/teacher/homework/${homeworkId}`)
}

export const publishHomework = (homeworkId, data) => {
  return http.post(`/teacher/homework/${homeworkId}/publish`, data)
}

export const getHomeworkSubmissions = (homeworkId, params) => {
  return http.get(`/teacher/homework/${homeworkId}/submissions`, { params })
}

export const gradeHomework = (homeworkId, submissionId, data) => {
  return http.post(`/teacher/homework/${homeworkId}/submissions/${submissionId}/grade`, data)
}

// ==================== 考试管理 ====================
export const getTeacherExams = (params) => {
  return http.get('/teacher/exams', { params })
}

export const getExamDetail = (examId) => {
  return http.get(`/teacher/exams/${examId}`)
}

export const createExam = (data) => {
  return http.post('/teacher/exams', data)
}

export const updateExam = (examId, data) => {
  return http.put(`/teacher/exams/${examId}`, data)
}

export const deleteExam = (examId) => {
  return http.delete(`/teacher/exams/${examId}`)
}

export const publishExam = (examId, data) => {
  return http.post(`/teacher/exams/${examId}/publish`, data)
}

export const getExamSubmissions = (examId, params) => {
  return http.get(`/teacher/exams/${examId}/submissions`, { params })
}

export const gradeExam = (examId, submissionId, data) => {
  return http.post(`/teacher/exams/${examId}/submissions/${submissionId}/grade`, data)
}

// ==================== 课程社区管理 ====================
export const getTeacherCourseThreads = (courseId, params) => {
  return http.get(`/teacher/courses/${courseId}/threads`, { params })
}

export const getTeacherThread = (courseId, threadId) => {
  return http.get(`/teacher/courses/${courseId}/threads/${threadId}`)
}

export const createTeacherThread = (courseId, data) => {
  return http.post(`/teacher/courses/${courseId}/threads`, data)
}

export const updateTeacherThread = (courseId, threadId, data) => {
  return http.put(`/teacher/courses/${courseId}/threads/${threadId}`, data)
}

export const deleteTeacherThread = (courseId, threadId) => {
  return http.delete(`/teacher/courses/${courseId}/threads/${threadId}`)
}

export const pinThread = (courseId, threadId) => {
  return http.post(`/teacher/courses/${courseId}/threads/${threadId}/pin`)
}

export const unpinThread = (courseId, threadId) => {
  return http.post(`/teacher/courses/${courseId}/threads/${threadId}/unpin`)
}

// ==================== 数据统计 ====================
export const getCourseStatistics = (courseId) => {
  return http.get(`/teacher/courses/${courseId}/statistics`)
}

export const getTeacherDashboard = () => {
  return http.get('/teacher/dashboard')
}
