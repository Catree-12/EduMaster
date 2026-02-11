/**
 * 用户状态管理
 * 管理用户登录状态、用户信息、Token 等
 */
const state = {
  // 核心修复：先取出字符串，判断有效性后再解析
  userInfo: (function() {
    const user = localStorage.getItem('userInfo');
    // 只有当 user 存在且不是 "undefined" 字符串时才解析
    if (user && user !== 'undefined') {
      try {
        return JSON.parse(user);
      } catch (e) {
        return null;
      }
    }
    return null;
  })(),
  
  // 访问令牌
  token: localStorage.getItem('token') || '',
  // 刷新令牌
  refreshToken: localStorage.getItem('refreshToken') || '',
  // 登录状态
  isLoggedIn: !!localStorage.getItem('token')
}

const mutations = {
  /**
   * 设置用户信息
   */
  SET_USER_INFO(state, userInfo) {
    state.userInfo = userInfo
    localStorage.setItem('userInfo', JSON.stringify(userInfo))
  },

  /**
   * 设置访问令牌
   */
  SET_TOKEN(state, token) {
    state.token = token
    localStorage.setItem('token', token)
  },

  /**
   * 设置刷新令牌
   */
  SET_REFRESH_TOKEN(state, refreshToken) {
    state.refreshToken = refreshToken
    localStorage.setItem('refreshToken', refreshToken)
  },

  /**
   * 设置登录状态
   */
  SET_LOGIN_STATUS(state, status) {
    state.isLoggedIn = status
  },

  /**
   * 登出，清除所有用户信息
   */
  LOGOUT(state) {
    state.userInfo = null
    state.token = ''
    state.refreshToken = ''
    state.isLoggedIn = false
    
    // 清除 localStorage
    localStorage.removeItem('userInfo')
    localStorage.removeItem('token')
    localStorage.removeItem('refreshToken')
  }
}

const actions = {
  /**
   * 用户注册
   * POST /api/auth/register/
   * @param {Object} data - { username, email, password, password_confirm }
   */
  async register( data) {
    const { authAPI } = require('@/api')
    const response = await authAPI.register(data)
    return response
  },

  /**
   * 刷新访问令牌
   * POST /api/auth/refresh/
   * 使用 refresh token 获取新的 access token
   */

  async refreshAccessToken({ commit, state }) {
    const { authAPI } = require('@/api')
    
    if (!state.refreshToken) {
      throw new Error('没有可用的 refresh token')
    }
    
    try {
      const response = await authAPI.refreshToken(state.refreshToken)
      const newAccessToken = response.access || response.access_token
      
      if (newAccessToken) {
        commit('SET_TOKEN', newAccessToken)
        commit('SET_LOGIN_STATUS', true)
        return newAccessToken
      }
      
      throw new Error('刷新 token 失败')
    } catch (error) {
      // 刷新失败,清除所有状态
      commit('LOGOUT')
      throw error
    }
  },

  /**
   * 用户登录
   * POST /api/auth/login/
   * @param {Object} payload - 后端返回的 data 对象
   * 后端结构: { access_token, refresh_token, user }
   */
  login({ commit }, payload) {
    // 后端返回的字段是 access_token 和 refresh_token
    const { access_token, refresh_token, access, refresh, token, user } = payload
    
    // 兼容多种命名格式
    const accessToken = access_token || access || token
    const refreshTokenValue = refresh_token || refresh

    if (!accessToken) {
      console.error('登录响应中未找到 token:', payload)
      throw new Error('登录失败: 未获取到 token')
    }

    // 保存 token
    commit('SET_TOKEN', accessToken)
    if (refreshTokenValue) {
      commit('SET_REFRESH_TOKEN', refreshTokenValue)
    }

    // 规范化用户信息,适配后端字段
    const normalizedUser = {
      id: user.id,
      real_name: user.real_name || user.username,
      nickname: user.nickname,
      email: user.email,
      phone: user.phone,
      avatar: user.avatar,
      bio: user.bio,
      gender: user.gender,
      school: user.school,
      major: user.major,
      // 管理员判断: 后端返回 is_admin 字段
      is_staff: user.is_admin || user.is_staff || false,
      is_superuser: user.is_superuser || false,
      // 学生和教师 profile
      student_profile: user.student_id ? { student_id: user.student_id } : null,
      teacher_profile: user.teacher_id ? { teacher_id: user.teacher_id, is_verified: true } : null
    }

    // 保存用户信息
    commit('SET_USER_INFO', normalizedUser)

    // 设置登录状态
    commit('SET_LOGIN_STATUS', true)
  },

  /**
   * 用户登出
   * POST /api/auth/logout/
   * 调用后端API将token加入黑名单，然后清除本地状态
   */
  async logout({ commit, state }) {
    // 只有存在 token 时才调用后端 API
    if (state.token) {
      try {
        const { authAPI } = require('@/api')
        // 调用后端API，将当前token加入黑名单
        await authAPI.logout()
      } catch (error) {
        console.error('调用退出登录API失败:', error)
        // API调用失败也继续清除本地状态
      }
    }
    // 清除本地状态
    commit('LOGOUT')
  },

  /**
   * 获取当前用户信息
   * GET /api/users/me/ 或 GET /api/users/profile/
   */
  async getUserInfo({ commit }) {
    const { userAPI } = require('@/api')
    // 使用 getCurrentUserProfile 获取完整信息
    // 响应拦截器已经返回了 data 部分,所以这里直接是用户数据
    const userData = await userAPI.getCurrentUserProfile()
    
    // 规范化用户信息,适配后端字段
    const normalizedUser = {
      id: userData.id,
      real_name: userData.real_name,
      nickname: userData.nickname,
      email: userData.email,
      phone: userData.phone,
      avatar: userData.avatar,
      bio: userData.bio,
      gender: userData.gender,
      school: userData.school,
      major: userData.major,
      // 管理员判断
      is_staff: userData.is_admin || userData.is_staff || false,
      is_superuser: userData.is_superuser || false,
      // 学生和教师 profile
      student_profile: userData.student_id ? { student_id: userData.student_id } : null,
      teacher_profile: userData.teacher_id ? { teacher_id: userData.teacher_id, is_verified: true } : null,
      created_at: userData.created_at
    }
    
    commit('SET_USER_INFO', normalizedUser)
    return normalizedUser
  },

  /**
   * 更新用户信息（本地更新，不调用 API）
   */
  updateUserInfo({ commit }, userInfo) {
    commit('SET_USER_INFO', userInfo)
  },

  /**
   * 忘记密码
   * POST /api/auth/forget-password/
   * @param {Object} data - { email }
   */
  async forgetPassword( data) {
    const { authAPI } = require('@/api')
    const response = await authAPI.forgetPassword(data)
    return response
  },

  /**
   * 修改密码
   * POST /api/auth/change-password/
   * @param {Object} data - { old_password, new_password, new_password_confirm }
   */
  async changePassword( data) {
    const { authAPI } = require('@/api')
    const response = await authAPI.changePassword(data)
    return response
  },

  /**
   * 刷新 Token（如果后端支持 refresh token）
   */
  refreshToken({ commit }, token) {
    commit('SET_TOKEN', token)
  }
}

const getters = {
  // 是否已登录
  isLoggedIn: state => state.isLoggedIn,
  
  // 用户信息
  userInfo: state => state.userInfo,
  
  // 是否是管理员 (Django 的 is_staff 或 is_superuser)
  isAdmin: state => state.userInfo?.is_staff || state.userInfo?.is_superuser || false,
  
  // 是否有教师身份 (检查是否有 teacher_profile)
  hasTeacherProfile: state => !!state.userInfo?.teacher_profile,
  
  // 是否有学生身份 (检查是否有 student_profile)
  hasStudentProfile: state => !!state.userInfo?.student_profile,
  
  // 用户 ID
  userId: state => state.userInfo?.id || null,
  
  // 用户名（登录用）
  real_name: state => state.userInfo?.real_name || '',
  
  // 昵称（显示用）
  nickname: state => state.userInfo?.nickname || state.userInfo?.username || '',
  
  // 用户邮箱
  email: state => state.userInfo?.email || '',
  
  // 用户手机号
  phone: state => state.userInfo?.phone || '',
  
  // 用户头像
  avatar: state => {
    if (state.userInfo?.avatar) {
      // 如果是完整 URL，直接返回
      if (state.userInfo.avatar.startsWith('http')) {
        return state.userInfo.avatar
      }
      // 否则拼接 MEDIA_URL
      return `${process.env.VUE_APP_MEDIA_URL}${state.userInfo.avatar}`
    }
    return '/default-avatar.png'
  },
  
  // 个人简介
  bio: state => state.userInfo?.bio || '',
  
  // 性别
  gender: state => state.userInfo?.gender || 'secret',
  
  // 学校
  school: state => state.userInfo?.school || '',
  
  // 专业
  major: state => state.userInfo?.major || '',
  
  // 学号（学生专属，只读）
  studentId: state => state.userInfo?.student_profile?.student_id || '',
  
  // 工号（教师专属，只读）
  teacherId: state => state.userInfo?.teacher_profile?.teacher_id || '',
  
  // 教师认证状态
  isTeacherVerified: state => state.userInfo?.teacher_profile?.is_verified || false,
  
  // 注册时间
  createdAt: state => state.userInfo?.created_at || null
}

export default {
  namespaced: true,
  state,
  mutations,
  actions,
  getters
}

