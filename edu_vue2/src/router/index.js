import Vue from 'vue'
import VueRouter from 'vue-router'

// 导入布局组件
import MainLayout from '@/layouts/MainLayout.vue'
import AdminLayout from '@/layouts/AdminLayout.vue'

// 导入模块化路由
import { authRoutes, publicContentRoutes } from './modules/public'
import studentRoutes from './modules/student'
import teacherRoutes from './modules/teacher'
import adminRoutes from './modules/admin'
import sharedRoutes from './modules/shared'
import userRoutes from './modules/user'

Vue.use(VueRouter)

// 解决重复导航报错
const originalPush = VueRouter.prototype.push
VueRouter.prototype.push = function push(location) {
  return originalPush.call(this, location).catch(err => {
    if (err.name !== 'NavigationDuplicated') {
      return Promise.reject(err)
    }
  })
}

const originalReplace = VueRouter.prototype.replace
VueRouter.prototype.replace = function replace(location) {
  return originalReplace.call(this, location).catch(err => {
    if (err.name !== 'NavigationDuplicated') {
      return Promise.reject(err)
    }
  })
}

// 路由配置
const routes = [
  // ==================== 认证路由（无布局）====================
  ...authRoutes,

  // ==================== 主应用路由（使用MainLayout）====================
  {
    path: '/',
    component: MainLayout,
    children: [
      // 公共内容路由（首页、课程中心等）
      ...publicContentRoutes,
      
      // 学生路由
      ...studentRoutes,
      
      // 教师路由
      ...teacherRoutes,
      
      // 用户路由（个人中心、证书）
      ...userRoutes,
      
      // 共享路由（社区、消息等）
      ...sharedRoutes
    ]
  },

  // ==================== 管理员路由（使用AdminLayout）====================
  {
    path: '/admin',
    component: AdminLayout,
    children: adminRoutes
  },

  // ==================== 404页面 ====================
  {
    path: '*',
    name: 'NotFound',
    component: () => import('@/views/shared/NotFound.vue'),
    meta: { title: '页面未找到' }
  }
]

// 创建路由实例
const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    } else {
      return { x: 0, y: 0 }
    }
  }
})

// ==================== 路由守卫 ====================
router.beforeEach((to, from, next) => {
  // 设置页面标题
  document.title = to.meta.title ? `${to.meta.title} - EduMaster` : 'EduMaster 在线教育平台'
  
  // ========== 开发模式自动登录（仅开发环境）==========
  const isDevelopment = process.env.NODE_ENV === 'development'
  
  if (isDevelopment) {
    // 开发模式下，自动设置测试用户信息
    if (!localStorage.getItem('token')) {
      localStorage.setItem('token', 'dev-test-token')
      localStorage.setItem('userRole', 'student')
      localStorage.setItem('userId', '1')
      localStorage.setItem('userName', '测试用户')
    }
    // 开发模式直接放行所有路由
    return next()
  }
  // =====================================================
  
  const token = localStorage.getItem('token')
  const userRole = localStorage.getItem('userRole') || 'student'
  const isAuthenticated = !!token
  
  // 1. 公共路由（无需认证）
  if (to.meta.requiresAuth === false) {
    // 已登录用户访问登录/注册页面，根据角色重定向
    if ((to.path === '/login' || to.path === '/register') && isAuthenticated) {
      if (userRole === 'admin') {
        return next('/admin/dashboard')
      } else if (userRole === 'teacher') {
        return next('/teacher/courses')
      } else {
        return next('/student/courses')
      }
    }
    return next()
  }
  
  // 2. 需要认证但未登录
  if (to.meta.requiresAuth && !isAuthenticated) {
    return next('/login')
  }
  
  // 3. 角色权限检查（基于路径前缀）
  if (to.path.startsWith('/student') && userRole !== 'student') {
    Vue.prototype.$message?.error('您没有权限访问该页面')
    return next('/')
  }
  
  if (to.path.startsWith('/teacher') && userRole !== 'teacher') {
    Vue.prototype.$message?.error('您没有权限访问该页面')
    return next('/')
  }
  
  if (to.path.startsWith('/admin') && userRole !== 'admin') {
    Vue.prototype.$message?.error('您没有权限访问该页面')
    return next('/')
  }
  
  // 4. Meta字段中的角色检查（兼容方式）
  if (to.meta.roles && to.meta.roles.length > 0) {
    if (!to.meta.roles.includes(userRole)) {
      Vue.prototype.$message?.error('您没有权限访问该页面')
      if (userRole === 'admin') {
        return next('/admin/dashboard')
      } else if (userRole === 'teacher') {
        return next('/teacher/courses')
      } else {
        return next('/student/courses')
      }
    }
  }
  
  next()
})

export default router
