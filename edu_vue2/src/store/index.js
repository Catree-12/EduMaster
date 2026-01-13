import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

import user from './modules/user'
import course from './modules/courses'
import exam from './modules/exam'

export default new Vuex.Store({
  modules: {
    user,
    course,
    exam
  }
})
