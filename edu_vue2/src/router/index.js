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

      
      // 学生路由
      ...studentRoutes,
      
      // 教师路由
      ...teacherRoutes,
      
      // 用户路由（个人中心、证书）
      ...userRoutes,
      
      // 共享路由（社区、消息等）
      ...sharedRoutes,

      // 公共内容路由（首页、课程中心等）
      ...publicContentRoutes
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
  
  const token = localStorage.getItem('token')
  const isAuthenticated = !!token
  
  // 获取用户信息
  let userInfo = null
  try {
    const userInfoStr = localStorage.getItem('userInfo')
    if (userInfoStr && userInfoStr !== 'undefined') {
      userInfo = JSON.parse(userInfoStr)
    }
  } catch (e) {
    console.error('Failed to parse userInfo:', e)
  }
  
  const isAdmin = userInfo?.is_staff || userInfo?.is_superuser || false
  
  // 1. 定义无需登录即可访问的公共路由
  const publicPaths = ['/login', '/register', '/forgot-password']
  const isPublicPath = publicPaths.includes(to.path)
  
  // 2. 未登录用户只能访问公共路由
  if (!isAuthenticated && !isPublicPath) {
    return next('/login')
  }
  
  // 3. 已登录用户访问登录/注册页面，根据身份重定向
  if (isAuthenticated && isPublicPath) {
    if (isAdmin) {
      return next('/admin/dashboard')
    } else {
      return next('/')  // 普通用户去首页
    }
  }
  
  // 4. 管理员权限检查
  if (to.path.startsWith('/admin')) {
    if (!isAdmin) {
      Vue.prototype.$message?.error('您没有管理员权限')
      return next('/')
    }
  }
  
  next()
})

export default router
