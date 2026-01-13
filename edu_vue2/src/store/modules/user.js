const state = {
  userInfo: JSON.parse(localStorage.getItem('userInfo')) || null,
  token: localStorage.getItem('token') || '',
  isLoggedIn: !!localStorage.getItem('token'),
  userRole: localStorage.getItem('userRole') || 'student'
}

const mutations = {
  SET_USER_INFO(state, userInfo) {
    state.userInfo = userInfo
    localStorage.setItem('userInfo', JSON.stringify(userInfo))
  },
  SET_TOKEN(state, token) {
    state.token = token
    localStorage.setItem('token', token)
  },
  SET_LOGIN_STATUS(state, status) {
    state.isLoggedIn = status
  },
  SET_USER_ROLE(state, role) {
    state.userRole = role
    localStorage.setItem('userRole', role)
  },
  LOGOUT(state) {
    state.userInfo = null
    state.token = ''
    state.isLoggedIn = false
    state.userRole = 'student'
    localStorage.removeItem('userInfo')
    localStorage.removeItem('token')
    localStorage.removeItem('userRole')
  }
}

const actions = {
  updateUserInfo({ commit }, userInfo) {
    commit('SET_USER_INFO', userInfo)
  },
  login({ commit }, { token, userInfo, role }) {
    commit('SET_TOKEN', token)
    commit('SET_USER_INFO', userInfo)
    commit('SET_LOGIN_STATUS', true)
    commit('SET_USER_ROLE', role)
  },
  logout({ commit }) {
    commit('LOGOUT')
  }
}

const getters = {
  isLoggedIn: state => state.isLoggedIn,
  userInfo: state => state.userInfo,
  userRole: state => state.userRole,
  isAdmin: state => state.userRole === 'admin'
}

export default {
  namespaced: true,
  state,
  mutations,
  actions,
  getters
}
