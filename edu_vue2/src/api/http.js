import axios from 'axios'
import router from '@/router'
import store from '@/store'
import { Message } from 'element-ui'

// 从环境变量读取 API 地址
const API_BASE_URL = process.env.VUE_APP_API_URL || 'http://localhost:8000/api'

// 防止重复跳转登录页的标志
let isRedirectingToLogin = false

const instance = axios.create({
  baseURL: API_BASE_URL,
  timeout: 15000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// ==================== 请求拦截器 ====================
instance.interceptors.request.use(
  config => {
    // 从 localStorage 或 Vuex 获取 token
    const token = store.state.user?.token || localStorage.getItem('token')
    // 排除不需要token的路径
    const isAuthPath = config.url.includes('/auth/login') || 
                       config.url.includes('/auth/register') ||
                       config.url.includes('/auth/refresh')
    
    if (token && !isAuthPath) {
      // Django REST Framework 标准 Token 格式
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  error => {
    console.error('请求错误:', error)
    return Promise.reject(error)
  }
)

// ==================== 响应拦截器 ====================
instance.interceptors.response.use(
  // 成功响应
  response => {
    // 后端返回的结构: { code, message, data }
    const res = response.data
    
    // 如果后端返回的是标准结构,直接返回 data 部分
    if (res && typeof res === 'object' && 'code' in res && 'data' in res) {
      // 如果 code 不是 200 表示业务错误
      if (res.code !== 200) {
        Message.error(res.message || '请求失败')
        return Promise.reject(new Error(res.message || '请求失败'))
      }
      return res.data
    }
    
    // 其他格式直接返回
    return res
  },
  // 错误响应
  async error => {
    const { response } = error

    if (!response) {
      // 网络错误或超时
      Message.error('网络连接失败，请检查网络设置')
      return Promise.reject(error)
    }

    const { status, data } = response

    switch (status) {
      case 400:
        // 请求参数错误
        Message.error(data.message || data.detail || '请求参数错误')
        break

      case 401: {
        // 防止刷新token接口本身触发死循环
        if (error.config.url && error.config.url.includes('/auth/refresh/')) {
          console.error('刷新token失败,请重新登录')
          // 直接执行登出逻辑
          if (!isRedirectingToLogin) {
            isRedirectingToLogin = true
            Message.warning('登录已过期,请重新登录')
            store.commit('user/LOGOUT')
            
            const currentPath = router.currentRoute.path
            if (currentPath !== '/login') {
              setTimeout(() => {
                router.replace('/login').catch(err => {
                  if (err.name !== 'NavigationDuplicated') {
                    console.error('路由跳转失败:', err)
                  }
                }).finally(() => {
                  setTimeout(() => {
                    isRedirectingToLogin = false
                  }, 1000)
                })
              }, 100)
            } else {
              isRedirectingToLogin = false
            }
          }
          break
        }
        
        // Token 过期或无效,先尝试使用 refresh token 刷新
        const refreshToken = store.state.user?.refreshToken || localStorage.getItem('refreshToken')
        
        // 如果有 refresh token 且请求未重试过,尝试刷新
        if (refreshToken && !error.config._retry) {
          error.config._retry = true // 标记该请求已重试,避免无限循环
          
          try {
            // 使用独立的axios实例调用刷新接口,避免触发拦截器
            const refreshResponse = await axios.post(`${API_BASE_URL}/auth/refresh/`, {
              refresh_token: refreshToken
            })
            
            // 刷新成功,更新 access token
            const newAccessToken = refreshResponse.data?.data?.access_token
            
            if (newAccessToken) {
              store.commit('user/SET_TOKEN', newAccessToken)
              localStorage.setItem('token', newAccessToken)
              
              // 重新发起原请求
              error.config.headers.Authorization = `Bearer ${newAccessToken}`
              return instance(error.config)
            }
          } catch (refreshError) {
            console.error('刷新 token 失败:', refreshError)
            // 刷新失败,执行登出逻辑
          }
        }
        
        // 没有 refresh token 或刷新失败,清除状态并跳转登录
        if (isRedirectingToLogin) {
          break
        }
        
        isRedirectingToLogin = true
        Message.warning('登录已过期,请重新登录')
        
        // 清除本地所有状态
        store.commit('user/LOGOUT')
        
        // 跳转到登录页
        const currentPath = router.currentRoute.path
        if (currentPath !== '/login') {
          setTimeout(() => {
            router.replace('/login').catch(err => {
              // 捕获导航错误,避免控制台报错
              if (err.name !== 'NavigationDuplicated') {
                console.error('路由跳转失败:', err)
              }
            }).finally(() => {
              // 重置标志位,允许下次跳转
              setTimeout(() => {
                isRedirectingToLogin = false
              }, 1000)
            })
          }, 100)
        } else {
          isRedirectingToLogin = false
        }
        break
      }

      case 403:
        // 无权限访问
        Message.error('您没有权限执行此操作')
        break

      case 404:
        // 资源不存在
        Message.error(data.message || '请求的资源不存在')
        break

      case 500:
        // 服务器错误
        Message.error('服务器错误，请稍后重试')
        break

      default:
        // 其他错误
        Message.error(data.message || data.detail || '请求失败')
    }

    return Promise.reject(error)
  }
)

export default instance
