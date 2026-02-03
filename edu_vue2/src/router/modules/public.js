/**
 * 公共路由 - 无需登录即可访问
 * 分为两类：
 * 1. authRoutes - 不需要布局的认证页面（登录、注册）
 * 2. publicRoutes - 需要 MainLayout 的公共页面（首页、课程中心）
 */

// 认证路由 - 无需布局
export const authRoutes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/public/auth/Login.vue'),
    meta: { requiresAuth: false, title: '登录' }
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('@/views/public/auth/Register.vue'),
    meta: { requiresAuth: false, title: '注册' }
  },
  {
    path: '/forgot-password',
    name: 'ForgotPassword',
    component: () => import('@/views/public/auth/ForgotPassword.vue'),
    meta: { requiresAuth: false, title: '忘记密码' }
  }
]

// 公共内容路由 - 需要 MainLayout（显示导航栏）
export const publicContentRoutes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/public/home/Index.vue'),
    meta: { requiresAuth: false, title: '首页' }
  },
  {
    path: '/courses',
    name: 'CourseCenter',
    component: () => import('@/views/public/course/Center.vue'),
    meta: { requiresAuth: false, title: '课程中心' }
  },
  {
    path: '/courses/:id',
    name: 'CourseDetail',
    component: () => import('@/views/public/course/Detail.vue'),
    meta: { requiresAuth: false, title: '课程详情' }
  },
  {
    path: '/enrollment',
    name: 'CourseEnrollment',
    component: () => import('@/views/public/course/ClassEnrollment.vue'),
    meta: { requiresAuth: true, title: '课程报名' }
  }
]

// 默认导出认证路由（向后兼容）
export default authRoutes
