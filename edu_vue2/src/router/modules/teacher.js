/**
 * 教师路由 - 需要教师角色权限
 */

export default [
  // ==================== 教师主页重定向 ====================
  {
    path: '/teacher',
    redirect: '/teacher/courses',
    meta: { requiresAuth: true, roles: ['teacher'] }
  },

  // ==================== 课程管理 ====================
  {
    path: '/teacher/courses',
    name: 'TeacherCourseList',
    component: () => import('@/views/teacher/course/List.vue'),
    meta: { requiresAuth: true, roles: ['teacher'], title: '我教的课程' }
  },
  {
    path: '/teacher/courses/create',
    name: 'TeacherCourseCreate',
    component: () => import('@/views/teacher/course/Create.vue'),
    meta: { requiresAuth: true, roles: ['teacher'], title: '创建课程' }
  },
  {
    path: '/teacher/courses/:courseId',
    name: 'TeacherCourseDetail',
    component: () => import('@/views/teacher/course/Detail.vue'),
    meta: { requiresAuth: true, roles: ['teacher'], title: '课程管理' }
  },
  {
    path: '/teacher/courses/:courseId/edit',
    name: 'TeacherCourseEdit',
    component: () => import('@/views/teacher/course/Edit.vue'),
    meta: { requiresAuth: true, roles: ['teacher'], title: '编辑课程' }
  },
  {
    path: '/teacher/courses/:courseId/chapters',
    name: 'TeacherCourseChapterEdit',
    component: () => import('@/views/teacher/course/ChapterEdit.vue'),
    meta: { requiresAuth: true, roles: ['teacher'], title: '章节编辑' }
  },
  {
    path: '/teacher/courses/:courseId/preview',
    name: 'TeacherCoursePreview',
    component: () => import('@/views/teacher/course/Preview.vue'),
    meta: { requiresAuth: true, roles: ['teacher'], title: '预览课程' }
  },
  {
    path: '/teacher/courses/:courseId/lessons/:lessonId',
    name: 'TeacherLessonPlayer',
    component: () => import('@/views/teacher/course/LessonPlayer.vue'),
    meta: { requiresAuth: true, roles: ['teacher'], title: '课时预览' }
  },

  // ==================== 作业管理 ====================
  {
    path: '/teacher/homework',
    name: 'TeacherHomeworkLibrary',
    component: () => import('@/views/teacher/homework/Library.vue'),
    meta: { requiresAuth: true, roles: ['teacher'], title: '作业库' }
  },
  {
    path: '/teacher/homework/create',
    name: 'TeacherHomeworkCreate',
    component: () => import('@/views/teacher/homework/Create.vue'),
    meta: { requiresAuth: true, roles: ['teacher'], title: '创建作业' }
  },
  {
    path: '/teacher/homework/:id',
    name: 'TeacherHomeworkDetail',
    component: () => import('@/views/teacher/homework/Detail.vue'),
    meta: { requiresAuth: true, roles: ['teacher'], title: '作业详情' }
  },
  {
    path: '/teacher/homework/:id/edit',
    name: 'TeacherHomeworkEdit',
    component: () => import('@/views/teacher/homework/Edit.vue'),
    meta: { requiresAuth: true, roles: ['teacher'], title: '编辑作业' }
  },
  {
    path: '/teacher/homework/:id/settings',
    name: 'TeacherHomeworkSettings',
    component: () => import('@/views/teacher/homework/Settings.vue'),
    meta: { requiresAuth: true, roles: ['teacher'], title: '作业设置' }
  },
  {
    path: '/teacher/homework/:id/publish',
    name: 'TeacherHomeworkPublish',
    component: () => import('@/views/teacher/homework/Publish.vue'),
    meta: { requiresAuth: true, roles: ['teacher'], title: '发布作业' }
  },
  {
    path: '/teacher/homework/:id/grading',
    name: 'TeacherHomeworkGradingList',
    component: () => import('@/views/teacher/homework/GradingList.vue'),
    meta: { requiresAuth: true, roles: ['teacher'], title: '批阅列表' }
  },
  {
    path: '/teacher/homework/:id/grading/:studentId',
    name: 'TeacherHomeworkGradingDetail',
    component: () => import('@/views/teacher/homework/GradingDetail.vue'),
    meta: { requiresAuth: true, roles: ['teacher'], title: '批阅详情' }
  },

  // ==================== 考试管理 ====================
  {
    path: '/teacher/exams',
    name: 'TeacherExamLibrary',
    component: () => import('@/views/teacher/exam/Library.vue'),
    meta: { requiresAuth: true, roles: ['teacher'], title: '试卷库' }
  },
  {
    path: '/teacher/exams/create',
    name: 'TeacherExamCreateSelection',
    component: () => import('@/views/teacher/exam/CreateSelection.vue'),
    meta: { requiresAuth: true, roles: ['teacher'], title: '选择组卷方式' }
  },
  {
    path: '/teacher/exams/create/manual',
    name: 'TeacherExamCreateManual',
    component: () => import('@/views/teacher/exam/CreateManual.vue'),
    meta: { requiresAuth: true, roles: ['teacher'], title: '手动组卷' }
  },
  {
    path: '/teacher/exams/create/intelligent',
    name: 'TeacherExamCreateIntelligent',
    component: () => import('@/views/teacher/exam/CreateIntelligent.vue'),
    meta: { requiresAuth: true, roles: ['teacher'], title: '智能组卷' }
  },
  {
    path: '/teacher/exams/:id',
    name: 'TeacherExamDetail',
    component: () => import('@/views/teacher/exam/Detail.vue'),
    meta: { requiresAuth: true, roles: ['teacher'], title: '试卷详情' }
  },
  {
    path: '/teacher/exams/:id/settings',
    name: 'TeacherExamSettings',
    component: () => import('@/views/teacher/exam/Settings.vue'),
    meta: { requiresAuth: true, roles: ['teacher'], title: '考试设置' }
  },
  {
    path: '/teacher/exams/:id/publish',
    name: 'TeacherExamPublish',
    component: () => import('@/views/teacher/exam/Publish.vue'),
    meta: { requiresAuth: true, roles: ['teacher'], title: '发布试卷' }
  },
  {
    path: '/teacher/exams/:id/grading',
    name: 'TeacherExamGradingList',
    component: () => import('@/views/teacher/exam/GradingList.vue'),
    meta: { requiresAuth: true, roles: ['teacher'], title: '批阅列表' }
  },
  {
    path: '/teacher/exams/:id/grading/:studentId',
    name: 'TeacherExamGradingDetail',
    component: () => import('@/views/teacher/exam/GradingDetail.vue'),
    meta: { requiresAuth: true, roles: ['teacher'], title: '批阅详情' }
  },

  // ==================== 课程社区管理 ====================
  {
    path: '/teacher/courses/:courseId/community/posts/create',
    name: 'TeacherCommunityPostCreate',
    component: () => import('@/views/teacher/community/PostCreate.vue'),
    meta: { requiresAuth: true, roles: ['teacher'], title: '发布公告' }
  },
  {
    path: '/teacher/courses/:courseId/community/posts/:postId',
    name: 'TeacherCommunityPostDetail',
    component: () => import('@/views/teacher/community/PostDetail.vue'),
    meta: { requiresAuth: true, roles: ['teacher'], title: '话题详情' }
  },
  {
    path: '/teacher/courses/:courseId/community/posts/:postId/edit',
    name: 'TeacherCommunityPostEdit',
    component: () => import('@/views/teacher/community/PostEdit.vue'),
    meta: { requiresAuth: true, roles: ['teacher'], title: '编辑话题' }
  },

  // ==================== 班级管理 ====================
  {
    path: '/teacher/classes',
    name: 'TeacherClassList',
    component: () => import('@/views/teacher/class/List.vue'),
    meta: { requiresAuth: true, roles: ['teacher'], title: '班级管理' }
  },
  {
    path: '/teacher/terms',
    name: 'TeacherTermManage',
    component: () => import('@/views/teacher/class/TermManage.vue'),
    meta: { requiresAuth: true, roles: ['teacher'], title: '学期管理' }
  }
]
