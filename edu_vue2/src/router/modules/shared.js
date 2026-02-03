/**
 * 共享路由 - 需要登录，但不限角色
 */

export default [
  // ==================== 社区广场 ====================
  {
    path: '/community',
    name: 'CommunityPlaza',
    component: () => import('@/views/shared/community/Plaza.vue'),
    meta: { requiresAuth: true, title: '社区广场' }
  },
  // 注意：create 必须放在 :id 之前，否则 create 会被当作 id 参数
  {
    path: '/community/posts/create',
    name: 'CommunityPostCreate',
    component: () => import('@/views/shared/community/PostCreate.vue'),
    meta: { requiresAuth: true, title: '发布话题' }
  },
  {
    path: '/community/posts/:id/edit',
    name: 'CommunityPostEdit',
    component: () => import('@/views/shared/community/PostEdit.vue'),
    meta: { requiresAuth: true, title: '编辑话题' }
  },
  {
    path: '/community/posts/:id',
    name: 'CommunityPostDetail',
    component: () => import('@/views/shared/community/PostDetail.vue'),
    meta: { requiresAuth: true, title: '话题详情' }
  },

  // ==================== 消息中心 ====================
  {
    path: '/messages',
    name: 'MessageCenter',
    component: () => import('@/views/shared/message/Center.vue'),
    meta: { requiresAuth: true, title: '消息中心' }
  }
]
