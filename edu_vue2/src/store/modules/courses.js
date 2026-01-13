const state = {
  courses: [],
  currentCourse: null
}

const mutations = {
  SET_COURSES(state, courses) {
    state.courses = courses
  },
  SET_CURRENT_COURSE(state, course) {
    state.currentCourse = course
  }
}

const actions = {
  fetchCourses({ commit }) {
    // TODO: 调用 API 获取课程列表
    commit('SET_COURSES', [])
  },
  fetchCourseDetail({ commit }) {
    // TODO: 调用 API 获取课程详情
    commit('SET_CURRENT_COURSE', {})
  }
}

export default {
  namespaced: true,
  state,
  mutations,
  actions
}
