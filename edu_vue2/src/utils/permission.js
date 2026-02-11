/**
 * 权限判断工具函数
 * 使用 store getters 判断用户权限
 */
import store from '@/store'

export const permissionUtils = {
  // 检查用户是否是课程老师
  isCourseTeacher(courseId, userId, userCourses) {
    const course = userCourses.find(c => c.id === parseInt(courseId))
    return course && course.teacherId === userId
  },

  // 检查用户是否是管理员 (使用 Django 的 is_staff 或 is_superuser)
  isAdmin() {
    return store.getters['user/isAdmin']
  },

  // 检查用户是否有教师身份
  hasTeacherProfile() {
    return store.getters['user/hasTeacherProfile']
  },

  // 检查用户是否有学生身份
  hasStudentProfile() {
    return store.getters['user/hasStudentProfile']
  },

  // 检查用户是否选了该课程
  hasEnrolledCourse(courseId, userCourses) {
    return userCourses.some(c => c.id === parseInt(courseId))
  },

  // 检查是否可以操作考试 (教师身份且不是管理员)
  canEditExam() {
    return this.hasTeacherProfile() && !this.isAdmin()
  },

  // 检查教师是否已认证
  isTeacherVerified() {
    return store.getters['user/isTeacherVerified']
  }
}
