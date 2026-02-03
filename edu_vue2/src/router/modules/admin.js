/**
 * 管理员路由 - 需要管理员角色权限
 */

export default [
  // ==================== 管理员主页重定向 ====================
  {
    path: '/admin',
    redirect: '/admin/dashboard',
    meta: { requiresAuth: true, roles: ['admin'] }
  },

  // ==================== 管理员功能 ====================
  {
    path: '/admin/dashboard',
    name: 'AdminDashboard',
    component: () => import('@/views/admin/AdminDashboard.vue'),
    meta: { requiresAuth: true, roles: ['admin'], title: '仪表盘' }
  },
  {
    path: '/admin/users',
    name: 'AdminUserManagement',
    component: () => import('@/views/admin/UserManagement.vue'),
    meta: { requiresAuth: true, roles: ['admin'], title: '用户管理' }
  },
  {
    path: '/admin/courses/audit',
    name: 'AdminCourseAudit',
    component: () => import('@/views/admin/CourseAudit.vue'),
    meta: { requiresAuth: true, roles: ['admin'], title: '课程审核' }
  },
  {
    path: '/admin/content/review',
    name: 'AdminContentReview',
    component: () => import('@/views/admin/ContentReview.vue'),
    meta: { requiresAuth: true, roles: ['admin'], title: '内容审查' }
  },
  {
    path: '/admin/certificates',
    name: 'AdminCertificateManagement',
    component: () => import('@/views/admin/CertificateManagement.vue'),
    meta: { requiresAuth: true, roles: ['admin'], title: '证书管理' }
  },
  {
    path: '/admin/analytics',
    name: 'AdminAnalytics',
    component: () => import('@/views/admin/AdminAnalytics.vue'),
    meta: { requiresAuth: true, roles: ['admin'], title: '数据分析' }
  },
  {
    path: '/admin/settings',
    name: 'AdminSystemSettings',
    component: () => import('@/views/admin/SystemSettings.vue'),
    meta: { requiresAuth: true, roles: ['admin'], title: '系统设置' }
  }
]
