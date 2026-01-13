import http from './http'

export const communityAPI = {
  // 获取公共社区问题列表
  getPublicQuestions(params) {
    return http.get('/community/questions', { params })
  },

  // 获取课程社区问题列表
  getCourseQuestions(courseId, params) {
    return http.get(`/courses/${courseId}/community/questions`, { params })
  },

  // 获取问题详情
  getQuestionDetail(questionId) {
    return http.get(`/community/questions/${questionId}`)
  },

  // 发布问题
  postQuestion(data) {
    return http.post('/community/questions', data)
  },

  // 编辑问题
  updateQuestion(questionId, data) {
    return http.put(`/community/questions/${questionId}`, data)
  },

  // 删除问题
  deleteQuestion(questionId) {
    return http.delete(`/community/questions/${questionId}`)
  },

  // 回答问题
  postAnswer(questionId, data) {
    return http.post(`/community/questions/${questionId}/answers`, data)
  },

  // 编辑回答
  updateAnswer(answerId, data) {
    return http.put(`/community/answers/${answerId}`, data)
  },

  // 删除回答
  deleteAnswer(answerId) {
    return http.delete(`/community/answers/${answerId}`)
  },

  // 点赞问题/回答
  likeQuestion(questionId) {
    return http.post(`/community/questions/${questionId}/like`)
  },

  likeAnswer(answerId) {
    return http.post(`/community/answers/${answerId}/like`)
  }
}
