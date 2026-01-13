const state = {
  currentExam: null,
  examAnswers: {},
  examStartTime: null,
  examTimeLimit: 0
}

const mutations = {
  SET_CURRENT_EXAM(state, exam) {
    state.currentExam = exam
  },
  SET_EXAM_ANSWERS(state, answers) {
    state.examAnswers = answers
  },
  UPDATE_ANSWER(state, { questionId, answer }) {
    state.examAnswers[questionId] = answer
  },
  SET_EXAM_START_TIME(state, time) {
    state.examStartTime = time
  },
  SET_EXAM_TIME_LIMIT(state, limit) {
    state.examTimeLimit = limit
  },
  CLEAR_EXAM_DATA(state) {
    state.currentExam = null
    state.examAnswers = {}
    state.examStartTime = null
    state.examTimeLimit = 0
  }
}

const actions = {
  setCurrentExam({ commit }, exam) {
    commit('SET_CURRENT_EXAM', exam)
  },
  updateAnswer({ commit }, { questionId, answer }) {
    commit('UPDATE_ANSWER', { questionId, answer })
  },
  clearExamData({ commit }) {
    commit('CLEAR_EXAM_DATA')
  }
}

const getters = {
  currentExam: state => state.currentExam,
  examAnswers: state => state.examAnswers,
  examTimeRemaining: state => {
    if (!state.examStartTime || !state.examTimeLimit) return 0
    const elapsed = (Date.now() - state.examStartTime) / 1000
    return Math.max(0, state.examTimeLimit * 60 - elapsed)
  }
}

export default {
  namespaced: true,
  state,
  mutations,
  actions,
  getters
}
