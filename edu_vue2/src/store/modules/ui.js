// 新增 UI 状态管理 - 减少组件内部状态
const state = {
  sidebarCollapsed: false,
  activeTab: {},
  modals: {}
}

const mutations = {
  TOGGLE_SIDEBAR(state) {
    state.sidebarCollapsed = !state.sidebarCollapsed
  },
  SET_ACTIVE_TAB(state, { key, value }) {
    state.activeTab[key] = value
  },
  OPEN_MODAL(state, modalName) {
    state.modals[modalName] = true
  },
  CLOSE_MODAL(state, modalName) {
    state.modals[modalName] = false
  }
}

export default {
  namespaced: true,
  state,
  mutations
}
