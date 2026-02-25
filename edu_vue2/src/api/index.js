/**
 * ================================================
 * 统一的 API 导出文件
 * ================================================
 * 
 * 使用方式 1 - 命名导出（推荐）:
 * import { authAPI, userAPI, courseAPI } from '@/api'
 * authAPI.login(data)
 * userAPI.updateUserInfo(data)
 * 
 * 使用方式 2 - 默认导出:
 * import api from '@/api'
 * api.auth.login(data)
 * api.user.updateUserInfo(data)
 * 
 * 使用方式 3 - 导入具体方法（学生/教师模块）:
 * import { getStudentCourses, getTeacherCourses } from '@/api'
 * 
 * ================================================
 */

// ==================== 核心模块 ====================
// 认证相关
export { authAPI } from './auth'

// 用户相关
export { userAPI } from './user'

// 课程相关
export { courseAPI } from './course'

// 作业相关
export { assignmentAPI } from './assignment'

// 考试相关
export { examAPI } from './exam'

// 社区相关
export { communityAPI } from './community'

// 管理员相关
export { adminAPI } from './admin'

// ==================== 学生模块 ====================
// 导出所有学生相关方法
import * as studentAPIs from './student'
export const studentAPI = studentAPIs
export * from './student'

// ==================== 教师模块 ====================
// 导出所有教师相关方法
import * as teacherAPIs from './teacher'
export const teacherAPI = teacherAPIs
export * from './teacher'

// ==================== 知识点和标签模块 ====================

import * as knowledgeAPIs from './knowledge'
export const knowledgeAPI = knowledgeAPIs
export * from './knowledge'

// ==================== 默认导出 ====================
// 方便使用 api.xxx.method() 的方式调用
import { authAPI } from './auth'
import { userAPI } from './user'
import { courseAPI } from './course'
import { communityAPI } from './community'
import { adminAPI } from './admin'
import { examAPI } from './exam'
import { assignmentAPI } from './assignment'

export default {
  // 核心模块
  auth: authAPI,
  user: userAPI,
  course: courseAPI,
  community: communityAPI,
  admin: adminAPI,
  exam: examAPI,
  assignment: assignmentAPI,
  homework: assignmentAPI, // 别名
  
  // 知识点和标签模块
  knowledge: knowledgeAPI,
  
  // 角色模块
  student: studentAPIs,
  teacher: teacherAPIs
}
