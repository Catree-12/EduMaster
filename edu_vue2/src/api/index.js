// ================================================
// 统一的 API 导出文件
// 建议使用命名导出，例如:
// import { courseAPI, teacherAPI, studentAPI } from '@/api'
// ================================================

// 认证相关
export { authAPI } from './auth'

// 用户相关
export { userAPI } from './user'

// 课程相关
export { courseAPI } from './course'

// 学生功能
export * from './student'

// 教师功能
export * from './teacher'

// 作业相关
export { assignmentAPI } from './assignment'

// 考试相关
export { examAPI } from './exam'

// 社区相关
export { communityAPI } from './community'

// 管理员相关
export { adminAPI } from './admin'

// 默认导出 (简化，不使用 services.js)
import { authAPI } from './auth'
import { userAPI } from './user'
import { courseAPI } from './course'
import { communityAPI } from './community'
import { adminAPI } from './admin'
import { examAPI } from './exam'
import { assignmentAPI } from './assignment'

export default {
  auth: authAPI,
  user: userAPI,
  course: courseAPI,
  community: communityAPI,
  admin: adminAPI,
  exam: examAPI,
  homework: assignmentAPI
}
