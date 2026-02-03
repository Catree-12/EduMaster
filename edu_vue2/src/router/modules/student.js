/**
 * 学生路由 - 需要学生角色权限
 */

export default [
  // ==================== 学生主页重定向 ====================
  {
    path: '/student',
    redirect: '/student/courses',
    meta: { requiresAuth: true, roles: ['student'] }
  },

  // ==================== 课程学习 ====================
  {
    path: '/student/courses',
    name: 'StudentCourseList',
    component: () => import('@/views/student/course/List.vue'),
    meta: { requiresAuth: true, roles: ['student'], title: '我学的课程' }
  },
  {
    path: '/student/courses/:courseId',
    name: 'StudentCourseDetail',
    component: () => import('@/views/student/course/Detail.vue'),
    meta: { requiresAuth: true, roles: ['student'], title: '课程学习' }
  },
  {
    path: '/student/courses/:courseId/lessons/:lessonId',
    name: 'StudentLessonPlayer',
    component: () => import('@/views/student/course/LessonPlayer.vue'),
    meta: { requiresAuth: true, roles: ['student'], title: '观看课时' }
  },

  // ==================== 作业 ====================
  {
    path: '/student/homework',
    name: 'StudentHomeworkList',
    component: () => import('@/views/student/homework/List.vue'),
    meta: { requiresAuth: true, roles: ['student'], title: '我的作业' }
  },
  {
    path: '/student/courses/:courseId/homework/:homeworkId',
    name: 'StudentHomeworkDetail',
    component: () => import('@/views/student/homework/Detail.vue'),
    meta: { requiresAuth: true, roles: ['student'], title: '作业详情' }
  },

  // ==================== 考试 ====================
  {
    path: '/student/exams',
    name: 'StudentExamList',
    component: () => import('@/views/student/exam/List.vue'),
    meta: { requiresAuth: true, roles: ['student'], title: '我的考试' }
  },
  {
    path: '/student/courses/:courseId/exams/:examId',
    name: 'StudentExamConfirm',
    component: () => import('@/views/student/exam/Confirm.vue'),
    meta: { requiresAuth: true, roles: ['student'], title: '考试确认' }
  },
  {
    path: '/student/courses/:courseId/exams/:examId/answer',
    name: 'StudentExamAnswer',
    component: () => import('@/views/student/exam/Answer.vue'),
    meta: { requiresAuth: true, roles: ['student'], title: '考试答题' }
  },

  // ==================== 课程社区 ====================
  {
    path: '/student/courses/:courseId/community/posts/create',
    name: 'StudentCommunityPostCreate',
    component: () => import('@/views/student/community/PostCreate.vue'),
    meta: { requiresAuth: true, roles: ['student'], title: '发布话题' }
  },
  {
    path: '/student/courses/:courseId/community/posts/:postId',
    name: 'StudentCommunityPostDetail',
    component: () => import('@/views/student/community/PostDetail.vue'),
    meta: { requiresAuth: true, roles: ['student'], title: '话题详情' }
  },
  {
    path: '/student/courses/:courseId/community/posts/:postId/edit',
    name: 'StudentCommunityPostEdit',
    component: () => import('@/views/student/community/PostEdit.vue'),
    meta: { requiresAuth: true, roles: ['student'], title: '编辑话题' }
  }
]
