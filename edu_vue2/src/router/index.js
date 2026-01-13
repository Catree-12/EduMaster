import Vue from 'vue'
import VueRouter from 'vue-router'

// 认证相关
import Login from '@/views/auth/Login.vue'
import Register from '@/views/auth/Register.vue'
import ForgotPassword from '@/views/auth/ForgotPassword.vue'

// 主布局
import MainLayout from '@/layouts/MainLayout.vue'
import AdminLayout from '@/layouts/AdminLayout.vue'

// 首页和课程
import Home from '@/views/home/Home.vue'
import CourseCenter from '@/views/course/CourseCenter.vue'
import CourseDetail from '@/views/course/CourseDetail.vue'

// 个人中心
import MyProfile from '@/views/user/MyProfile.vue'

// 社区
import Community from '@/views/community/Community.vue'
import CourseCommunity from '@/views/community/CourseCommunity.vue'
import NewPost from '@/views/community/NewPost.vue'
import PostDetail from '@/views/community/PostDetail.vue'

// 考试相关
import ExamCenter from '@/views/exam/ExamCenter.vue'
import ExamAnswer from '@/views/exam/ExamAnswer.vue'

// 作业相关
import HomeworkCenter from '@/views/homework/HomeworkCenter.vue'

// 讲师相关
import TeacherCourseDetail from '@/views/teacher/TeacherCourseDetail.vue'
import ExamCreate from '@/views/teacher/ExamCreate.vue'
import ExamDetail from '@/views/teacher/ExamDetail.vue'
import ExamPublish from '@/views/teacher/ExamPublish.vue'
import ExamSettings from '@/views/teacher/ExamSettings.vue'
import ExamLibrary from '@/views/teacher/ExamLibrary.vue'
import GradingManage from '@/views/teacher/GradingManage.vue'
import CourseEdit from '@/views/teacher/CourseEdit.vue'
import TermManagement from '@/views/teacher/TermManagement.vue'
import ClassManagement from '@/views/teacher/ClassManagement.vue'
import HomeworkLibrary from '@/views/teacher/HomeworkLibrary.vue'
import HomeworkCreate from '@/views/teacher/HomeworkCreate.vue'
import HomeworkDetail from '@/views/teacher/HomeworkDetail.vue'
import HomeworkEdit from '@/views/teacher/HomeworkEdit.vue'
import HomeworkPublish from '@/views/teacher/HomeworkPublish.vue'
import HomeworkSettings from '@/views/teacher/HomeworkSettings.vue'
import HomeworkGrading from '@/views/teacher/HomeworkGrading.vue'
import HomeworkGradingDetail from '@/views/teacher/HomeworkGradingDetail.vue'
import ExamGrading from '@/views/teacher/ExamGrading.vue'
import ExamGradingDetail from '@/views/teacher/ExamGradingDetail.vue'
import ChapterEditor from '@/views/teacher/ChapterEditor.vue'

// 新课程页面（来自course目录）
import CourseCreate from '@/views/course/CourseCreate.vue'
import MyCoursesCourseView from '@/views/course/MyCourses.vue'
import StudentEnrollment from '@/views/course/StudentEnrollment.vue'
import StudentCourseDetail from '@/views/course/StudentCourseDetail.vue'
import LessonPlayer from '@/views/course/LessonPlayer.vue'

// 证书相关
import MyCertificates from '@/views/user/MyCertificates.vue'
import CertificateShareView from '@/views/certificate/ShareView.vue'

// 管理员相关
import AdminDashboard from '@/views/admin/AdminDashboard.vue'
import CourseAudit from '@/views/admin/CourseAudit.vue'
import UserManagement from '@/views/admin/UserManagement.vue'
import ContentReview from '@/views/admin/ContentReview.vue'
import CertificateManagement from '@/views/admin/CertificateManagement.vue'
import Analytics from '@/views/admin/AdminAnalytics.vue'
import SystemSettings from '@/views/admin/SystemSettings.vue'

Vue.use(VueRouter)

const routes = [
  // 认证路由（无布局）
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: { requiresAuth: false }
  },
  {
    path: '/register',
    name: 'Register',
    component: Register,
    meta: { requiresAuth: false }
  },
  {
    path: '/forgot-password',
    name: 'ForgotPassword',
    component: ForgotPassword,
    meta: { requiresAuth: false }
  },
  
  // 证书分享公开页面（不需要认证）
  {
    path: '/certificate/share/:shareCode',
    name: 'CertificateShareView',
    component: CertificateShareView,
    meta: { requiresAuth: false }
  },
  
  // 管理员路由（使用管理员布局）
  {
    path: '/admin',
    component: AdminLayout,
    meta: { requiresAuth: true, requiresRole: 'admin' },
    children: [
      {
        path: 'dashboard',
        name: 'AdminDashboard',
        component: AdminDashboard
      },
      {
        path: 'course-audit',
        name: 'CourseAudit',
        component: CourseAudit
      },
      {
        path: 'users',
        name: 'UserManagement',
        component: UserManagement
      },
      {
        path: 'content-review',
        name: 'ContentReview',
        component: ContentReview
      },
      {
        path: 'certificates',
        name: 'CertificateManagement',
        component: CertificateManagement
      },
      {
        path: 'analytics',
        name: 'Analytics',
        component: Analytics
      },
      {
        path: 'settings',
        name: 'SystemSettings',
        component: SystemSettings
      }
    ]
  },
  
  // 主应用路由（使用主布局）
  {
    path: '/',
    component: MainLayout,
    meta: { requiresAuth: true },
    children: [
      // 首页
      {
        path: '',
        name: 'Home',
        component: Home
      },
      
      // 课程相关
      {
        path: 'course',
        name: 'CourseCenter',
        component: CourseCenter
      },
      {
        path: 'course/create',
        name: 'CourseCreate',
        component: CourseCreate,
        meta: { requiresAuth: true }
      },
      {
        path: 'course/my-courses',
        name: 'MyCoursesList',
        component: MyCoursesCourseView
      },
      {
        path: 'course/enroll',
        name: 'StudentEnrollment',
        component: StudentEnrollment
      },
      {
        path: 'student/course/:id',
        name: 'StudentCourseDetail',
        component: StudentCourseDetail,
        meta: { requiresAuth: true }
      },
      {
        path: 'course/:id/lesson/:lessonId',
        name: 'LessonPlayer',
        component: LessonPlayer,
        meta: { requiresAuth: true }
      },
      {
        path: 'course/:id',
        name: 'CourseDetail',
        component: CourseDetail
      },
      
      // 用户中心
      {
        path: 'user-center/profile',
        name: 'MyProfile',
        component: MyProfile
      },
      {
        path: 'user-center/certificates',
        name: 'MyCertificates',
        component: MyCertificates
      },
      
      // 社区
      {
        path: 'community',
        name: 'Community',
        component: Community
      },
      {
        path: 'community/new-post',
        name: 'NewPost',
        component: NewPost
      },
      {
        path: 'community/post/:id',
        name: 'PostDetail',
        component: PostDetail
      },
      {
        path: 'course/:id/community',
        name: 'CourseCommunity',
        component: CourseCommunity
      },
      
      // 考试相关
      {
        path: 'exam-center',
        name: 'ExamCenter',
        component: ExamCenter
      },
      {
        path: 'exam/:id/answer',
        name: 'ExamAnswer',
        component: ExamAnswer
      },
      
      // 作业相关
      {
        path: 'homework-center',
        name: 'HomeworkCenter',
        component: HomeworkCenter
      },
      
      // 讲师相关（需要课程创建者权限，暂时不做全局限制）
      {
        path: 'teacher/course/:id',
        name: 'TeacherCourseDetail',
        component: TeacherCourseDetail,
        meta: { requiresAuth: true }
      },
      {
        path: 'teacher/course/:id/chapters/edit',
        name: 'ChapterEditor',
        component: ChapterEditor,
        meta: { requiresAuth: true }
      },
      {
        path: 'teacher/course/:id/edit',
        name: 'CourseEdit',
        component: CourseEdit,
        meta: { requiresAuth: true }
      },
      {
        path: 'teacher/exam-create',
        name: 'ExamCreate',
        component: ExamCreate,
        meta: { requiresAuth: true }
      },
      {
        path: 'teacher/exam/:id/detail',
        name: 'ExamDetail',
        component: ExamDetail,
        meta: { requiresAuth: true }
      },
      {
        path: 'teacher/exam/:id/publish',
        name: 'ExamPublish',
        component: ExamPublish,
        meta: { requiresAuth: true }
      },
      {
        path: 'teacher/exam/:id/settings',
        name: 'ExamSettings',
        component: ExamSettings,
        meta: { requiresAuth: true }
      },
      {
        path: 'teacher/exam-library',
        name: 'ExamLibrary',
        component: ExamLibrary,
        meta: { requiresAuth: true }
      },
      {
        path: 'teacher/grading',
        name: 'GradingManage',
        component: GradingManage,
        meta: { requiresAuth: true }
      },
      {
        path: 'teacher/term-management',
        name: 'TermManagement',
        component: TermManagement,
        meta: { requiresAuth: true }
      },
      {
        path: 'teacher/class-management',
        name: 'ClassManagement',
        component: ClassManagement,
        meta: { requiresAuth: true }
      },
      {
        path: 'teacher/homework/library',
        name: 'HomeworkLibrary',
        component: HomeworkLibrary,
        meta: { requiresAuth: true }
      },
      {
        path: 'teacher/homework/create',
        name: 'HomeworkCreate',
        component: HomeworkCreate,
        meta: { requiresAuth: true }
      },
      {
        path: 'teacher/homework/:id/detail',
        name: 'HomeworkDetail',
        component: HomeworkDetail,
        meta: { requiresAuth: true }
      },
      {
        path: 'teacher/homework/:id/edit',
        name: 'HomeworkEdit',
        component: HomeworkEdit,
        meta: { requiresAuth: true }
      },
      {
        path: 'teacher/homework/:id/publish',
        name: 'HomeworkPublish',
        component: HomeworkPublish,
        meta: { requiresAuth: true }
      },
      {
        path: 'teacher/homework/:id/settings',
        name: 'HomeworkSettings',
        component: HomeworkSettings,
        meta: { requiresAuth: true }
      },
      {
        path: 'teacher/homework/:id/grading',
        name: 'HomeworkGrading',
        component: HomeworkGrading,
        meta: { requiresAuth: true }
      },
      {
        path: 'teacher/homework/:id/grading-detail',
        name: 'HomeworkGradingDetail',
        component: HomeworkGradingDetail,
        meta: { requiresAuth: true }
      },
      {
        path: 'teacher/exam/:id/grading',
        name: 'ExamGrading',
        component: ExamGrading,
        meta: { requiresAuth: true }
      },
      {
        path: 'teacher/exam/:id/grading-detail',
        name: 'ExamGradingDetail',
        component: ExamGradingDetail,
        meta: { requiresAuth: true }
      },

      // 管理员相关
      {
        path: 'admin/course-audit',
        name: 'CourseAudit',
        component: CourseAudit,
        meta: { requiresAuth: true, requiresRole: 'admin' }
      }
    ]
  },
  
  // 重定向
  { path: '*', redirect: '/login' }
]

const router = new VueRouter({
  mode: 'history',
  routes
})

// 路由守卫：检查认证状态和角色权限
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  const userRole = localStorage.getItem('userRole') || 'user'
  const isAuthenticated = !!token
  
  // 需要认证的路由
  if (to.meta.requiresAuth && !isAuthenticated) {
    return next('/login')
  }
  
  // 已登录用户访问登录/注册页面，根据角色重定向
  if ((to.path === '/login' || to.path === '/register') && isAuthenticated) {
    if (userRole === 'admin') {
      return next('/admin/dashboard')
    }
    return next('/')
  }
  
  // 角色权限检查
  if (to.meta.requiresRole) {
    const requiredRoles = Array.isArray(to.meta.requiresRole) 
      ? to.meta.requiresRole 
      : [to.meta.requiresRole]
    
    if (!requiredRoles.includes(userRole)) {
      // 无权限，显示提示并重定向
      if (window.Vue && window.Vue.prototype.$message) {
        window.Vue.prototype.$message.error('您没有权限访问该页面')
      }
      return next('/')
    }
  }
  
  next()
})

export default router
