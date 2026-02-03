/**
 * 用户路由 - 个人信息和证书管理
 * 不区分角色，所有登录用户都可以访问
 */

export default [
  // ==================== 个人中心 ====================
  {
    path: '/user/profile',
    name: 'UserProfile',
    component: () => import('@/views/user/Profile.vue'),
    meta: { requiresAuth: true, title: '个人中心' }
  },

  // ==================== 我的证书 ====================
  {
    path: '/user/certificates',
    name: 'UserCertificates',
    component: () => import('@/views/user/Certificates.vue'),
    meta: { requiresAuth: true, title: '我的证书' }
  }
]
