import http from './http'

/**
 * 教师相关API
 */

// ==================== 课程管理 ====================
// export const getTeacherCourses = (params) => {
//   return http.get('/teacher/courses/', { params })
// }

export const getTeacherCourse = (courseId) => {
  return http.get(`/teacher/courses/${courseId}/`)
}

export const createCourse = (data) => {
  return http.post('/teacher/courses/create/', data)
}

export const updateCourse = (courseId, data) => {
  return http.put(`/teacher/courses/${courseId}`, data)
}

export const deleteCourse = (courseId) => {
  return http.delete(`/teacher/courses/${courseId}/`)
}

export const publishCourse = (courseId) => {
  return http.post(`/teacher/courses/${courseId}/publish/`)
}

// ==================== 章节管理 ====================

export const getCourseChapters = (courseId) => {
  return http.get(`/teacher/courses/${courseId}/chapters/`)
}

export const createChapter = (courseId, data) => {
  return http.post(`/teacher/courses/${courseId}/chapters/`, data)
}

export const updateChapter = (courseId, chapterId, data) => {
  return http.put(`/teacher/courses/${courseId}/chapters/${chapterId}/`, data)
}

export const deleteChapter = (courseId, chapterId) => {
  return http.delete(`/teacher/courses/${courseId}/chapters/${chapterId}/`)
}



export const sortChapters = (courseId, data) => {
  return http.post(`/teacher/courses/${courseId}/chapters/sort/`, data)
}

export const getLessonDetail = (courseId, lessonId) => {
  return http.get(`/teacher/courses/${courseId}/lessons/${lessonId}/`)
}

export const saveAllChapters = (courseId, data) => {
  return http.post(`/teacher/courses/${courseId}/chapters/batch/`, data)
}

// 小节管理
export const createLesson = (courseId, chapterId, data) => {
  return http.post(`/teacher/courses/${courseId}/chapters/${chapterId}/lessons/`, data)
}

export const updateLesson = (courseId, lessonId, data) => {
  return http.put(`/teacher/courses/${courseId}/lessons/${lessonId}/`, data)
}

export const deleteLesson = (courseId, lessonId) => {
  return http.delete(`/teacher/courses/${courseId}/lessons/${lessonId}/`)
}

// 课时内容块管理
export const saveContentBlocks = (courseId, lessonId, data) => {
  return http.post(`/teacher/courses/${courseId}/lessons/${lessonId}/content-blocks/`, data)
}

// 上传内容块文件（视频、文档等）
export const uploadContentBlockFile = (courseId, lessonId, fileData) => {
  const formData = new FormData()
  formData.append('file', fileData.file)
  formData.append('type', fileData.type) // 'video', 'image', 'file'
  
  return http.post(`/teacher/courses/${courseId}/lessons/${lessonId}/content-blocks/upload/`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}

// ==================== 学生管理 ====================
export const getCourseStudents = (courseId, params) => {
  return http.get(`/teacher/courses/${courseId}/students/`, { params })
}

export const getStudentProgress = (courseId, studentId) => {
  return http.get(`/teacher/courses/${courseId}/students/${studentId}/progress/`)
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


// ==================== 题库管理 ====================

// ========== 题目文件夹管理 ==========

/**
 * 获取题目文件夹树状结构
 * @param {number} courseId - 课程ID
 * @returns {Promise} 返回文件夹树状数据
 */
export const getQuestionCategories = (courseId) => {
  return http.get(`/teacher/courses/${courseId}/question-categories/`)
}

/**
 * 创建题目文件夹
 * @param {number} courseId - 课程ID
 * @param {object} data - 文件夹数据
 * @param {string} data.name - 文件夹名称
 * @param {number} data.parent_id - 父文件夹ID（可选）
 * @param {number} data.order - 排序（可选）
 */
export const createQuestionCategory = (courseId, data) => {
  return http.post(`/teacher/courses/${courseId}/question-categories/`, data)
}

/**
 * 获取题目文件夹详情
 * @param {number} courseId - 课程ID
 * @param {number} categoryId - 文件夹ID
 */
export const getQuestionCategoryDetail = (courseId, categoryId) => {
  return http.get(`/teacher/courses/${courseId}/question-categories/${categoryId}/`)
}

/**
 * 更新题目文件夹
 * @param {number} courseId - 课程ID
 * @param {number} categoryId - 文件夹ID
 * @param {object} data - 更新的数据
 * @param {string} data.name - 文件夹名称
 * @param {number} data.order - 排序
 */
export const updateQuestionCategory = (courseId, categoryId, data) => {
  return http.put(`/teacher/courses/${courseId}/question-categories/${categoryId}/`, data)
}

/**
 * 删除题目文件夹（软删除）
 * @param {number} courseId - 课程ID
 * @param {number} categoryId - 文件夹ID
 */
export const deleteQuestionCategory = (courseId, categoryId) => {
  return http.delete(`/teacher/courses/${courseId}/question-categories/${categoryId}/`)
}

// ========== 题目管理 ==========

/**
 * 获取题库列表
 * @param {number} courseId - 课程ID
 * @param {object} params - 查询参数
 * @param {number} params.page - 页码
 * @param {number} params.pageSize - 每页数量
 * @param {number} params.category_id - 文件夹ID（筛选指定文件夹下的题目）
 * @param {string} params.type - 题目类型 (single_choice, multiple_choice, true_false, fill_blank, short_answer)
 * @param {string} params.keyword - 搜索关键词
 * @param {number} params.tag_id - 标签ID
 * @param {number} params.point_id - 知识点ID
 */
export const getQuestionBank = (courseId, params) => {
  return http.get(`/teacher/courses/${courseId}/questions/`, { params })
}

/**
 * 创建题目
 * @param {number} courseId - 课程ID
 * @param {object} data - 题目数据
 * @param {string} data.title - 题目标题
 * @param {string} data.type - 题目类型
 * @param {string} data.content - 题目内容
 * @param {string} data.difficulty - 难度 (easy, medium, hard)
 * @param {array} data.tags - 标签ID数组
 * @param {array} data.knowledge_points - 知识点ID数组
 */
export const createQuestion = (courseId, data) => {
  return http.post(`/teacher/courses/${courseId}/questions/`, data)
}

/**
 * 获取题目详情
 * @param {number} courseId - 课程ID
 * @param {number} questionId - 题目ID
 */
export const getQuestionDetail = (courseId, questionId) => {
  return http.get(`/teacher/courses/${courseId}/questions/${questionId}/`)
}

/**
 * 更新题目
 * @param {number} courseId - 课程ID
 * @param {number} questionId - 题目ID
 * @param {object} data - 更新的题目数据
 */
export const updateQuestion = (courseId, questionId, data) => {
  return http.put(`/teacher/courses/${courseId}/questions/${questionId}/`, data)
}

/**
 * 删除题目
 * @param {number} courseId - 课程ID
 * @param {number} questionId - 题目ID
 */
export const deleteQuestion = (courseId, questionId) => {
  return http.delete(`/teacher/courses/${courseId}/questions/${questionId}/`)
}

// ==================== 数据统计 ====================
export const getCourseStatistics = (courseId) => {
  return http.get(`/teacher/courses/${courseId}/statistics`)
}

export const getTeacherDashboard = () => {
  return http.get('/teacher/dashboard')
}
