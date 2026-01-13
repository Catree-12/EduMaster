export const permissionUtils = {
  // 检查用户是否是课程老师
  isCourseTeacher(courseId, userId, userCourses) {
    const course = userCourses.find(c => c.id === parseInt(courseId))
    return course && course.teacherId === userId
  },

  // 检查用户是否是管理员
  isAdmin(userRole) {
    return userRole === 'admin'
  },

  // 检查用户是否选了该课程
  hasEnrolledCourse(courseId, userCourses) {
    return userCourses.some(c => c.id === parseInt(courseId))
  },

  // 检查是否可以操作考试
  canEditExam(userRole, isTeacher) {
    return userRole !== 'admin' && isTeacher
  }
}
