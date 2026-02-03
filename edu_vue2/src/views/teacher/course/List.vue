<template>
  <div class="my-courses-container">
    <div class="page-header">
      <h1>我的课程</h1>
      <p class="subtitle">管理你的课程和选修记录</p>
    </div>

    <!-- 标签切换 -->
    <el-tabs v-model="activeTab" type="card" class="tabs-container">
      <!-- 我教的课 -->
      <el-tab-pane label="我教的课" name="teaching">
        <div class="tab-content teaching-courses">
          <!-- 讲师工具栏 -->
          <div class="action-bar">
            <el-button type="primary" icon="el-icon-plus" @click="goToCreateCourse">
              创建课程
            </el-button>
          </div>

          <!-- 我教的课程列表 -->
          <div v-if="teachingCourses.length > 0" class="courses-grid">
            <div v-for="course in teachingCourses" :key="course.id" class="course-card teaching">
              <!-- 课程封面 -->
              <div class="course-cover">
                <img :src="course.coverImage" :alt="course.title" />
                <div class="status-badge" :class="course.status">
                  {{ getStatusText(course.status) }}
                </div>
              </div>

              <!-- 课程信息 -->
              <div class="course-info">
                <h3>{{ course.title }}</h3>
                <p class="description">{{ course.description | truncate(100) }}</p>
                
                <div class="course-meta">
                  <span class="category">{{ course.category }}</span>
                  <span class="price">¥{{ course.price }}</span>
                </div>

                <!-- 统计信息 -->
                <div class="statistics">
                  <div class="stat-item">
                    <span class="label">学生数</span>
                    <span class="value">{{ course.studentCount || 0 }}</span>
                  </div>
                  <div class="stat-item">
                    <span class="label">班期数</span>
                    <span class="value">{{ course.termCount || 0 }}</span>
                  </div>
                </div>

                <!-- 操作按钮 -->
                <div class="actions">
                  <el-button type="text" size="small" @click="viewTeachingCourse(course)">
                    查看
                  </el-button>
                  <el-button
                    v-if="course.status === 'draft'"
                    type="text"
                    size="small"
                    @click="publishCourse(course)"
                  >
                    发布
                  </el-button>
                  <el-button
                    v-if="course.status === 'published'"
                    type="text"
                    size="small"
                    @click="archiveCourse(course)"
                  >
                    下架
                  </el-button>
                  <el-button type="text" size="small" @click="deleteCourse(course)">
                    删除
                  </el-button>
                </div>
              </div>
            </div>
          </div>

          <!-- 空状态 -->
          <div v-else class="empty-state">
            <i class="el-icon-document" />
            <p>还没有创建任何课程</p>
            <el-button type="primary" @click="goToCreateCourse">
              立即创建
            </el-button>
          </div>
        </div>
      </el-tab-pane>

      <!-- 我学的课 -->
      <el-tab-pane label="我学的课" name="learning">
        <div class="tab-content learning-courses">
          <!-- 学生工具栏 -->
          <div class="action-bar">
            <el-button icon="el-icon-trophy" @click="goToExamCenter">
              考试中心
            </el-button>
            <el-button icon="el-icon-document-copy" @click="goToHomeworkCenter">
              作业中心
            </el-button>
          </div>

          <div v-if="learningCourses.length > 0" class="courses-grid">
            <div v-for="course in learningCourses" :key="course.id" class="course-card learning">
              <!-- 课程封面 -->
              <div class="course-cover">
                <img :src="course.coverImage" :alt="course.title" />
              </div>

              <!-- 课程信息 -->
              <div class="course-info">
                <h3>{{ course.title }}</h3>
                <p class="description">{{ course.description | truncate(100) }}</p>
                
                <div class="course-meta">
                  <span class="teacher">讲师: {{ course.instructorName }}</span>
                </div>

                <!-- 操作按钮 -->
                <div class="actions">
                  <el-button type="primary" size="small" @click="enterCourse(course)">
                    继续学习
                  </el-button>
                  <el-button type="text" size="small" @click="dropCourse(course)">
                    退课
                  </el-button>
                </div>
              </div>
            </div>
          </div>

          <!-- 空状态 -->
          <div v-else class="empty-state">
            <i class="el-icon-folder" />
            <p>还没有选修任何课程</p>
            <el-button type="primary" @click="goCourseCenter">
              去选课
            </el-button>
          </div>
        </div>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
export default {
  name: 'MyCourses',
  filters: {
    truncate(value, length) {
      if (!value) return ''
      value = value.toString()
      return value.length > length ? value.substring(0, length) + '...' : value
    }
  },
  data() {
    return {
      activeTab: 'teaching',
      teachingCourses: [
        {
          id: 't1',
          title: 'Vue.js 深度剖析与实战',
          description: '从源码级别深入理解 Vue.js，构建复杂、高性能的前端应用。',
          coverImage: 'https://via.placeholder.com/300x180/2c3e50/ffffff?text=Vue',
          status: 'published',
          category: '前端开发',
          price: 299,
          studentCount: 1250,
          termCount: 5
        },
        {
          id: 't2',
          title: 'Node.js 全栈开发工程师',
          description: '学习使用 Node.js、Express 和 MongoDB 构建完整的 Web 应用程序。',
          coverImage: 'https://via.placeholder.com/300x180/34495e/ffffff?text=Node.js',
          status: 'draft',
          category: '后端开发',
          price: 349,
          studentCount: 0,
          termCount: 1
        },
        {
          id: 't3',
          title: 'Python 数据分析与可视化',
          description: '掌握 Pandas、NumPy 和 Matplotlib，处理和可视化真实世界的数据集。',
          coverImage: 'https://via.placeholder.com/300x180/16a085/ffffff?text=Python',
          status: 'pending_review',
          category: '数据科学',
          price: 199,
          studentCount: 500,
          termCount: 2
        }
      ],
      learningCourses: [
        {
          id: 'l1',
          title: 'React 现代实战指南',
          description: '学习 React Hooks、Redux Toolkit 和 Next.js，构建现代化的 React 应用。',
          coverImage: 'https://via.placeholder.com/300x180/2980b9/ffffff?text=React',
          instructorName: '张三',
          progress: 75
        },
        {
          id: 'l2',
          title: 'UI/UX 设计原则与实践',
          description: '从用户研究到原型设计，掌握成为一名优秀设计师的核心技能。',
          coverImage: 'https://via.placeholder.com/300x180/8e44ad/ffffff?text=UI/UX',
          instructorName: '李四',
          progress: 30
        }
      ],
      loading: false
    }
  },
  computed: {
    userId() {
      return this.$store.state.user.id
    }
  },
  created() {
    // 暂时禁用 API 调用，使用静态示例数据进行测试
    // this.fetchMyCourses()
  },
  methods: {
    // 获取课程
    fetchMyCourses() {
      this.loading = true
      Promise.all([
        this.fetchTeachingCourses(),
        this.fetchLearningCourses()
      ])
        .then(() => {
          this.loading = false
        })
        .catch(() => {
          this.$message.error('加载课程失败')
          this.loading = false
        })
    },

    // 获取我教的课程
    fetchTeachingCourses() {
      return this.$api.get('/user/teaching-courses')
        .then(res => {
          this.teachingCourses = res.data || []
        })
    },

    // 获取我学的课程
    fetchLearningCourses() {
      return this.$api.get('/user/learning-courses')
        .then(res => {
          this.learningCourses = res.data || []
        })
    },

    // 状态文本
    getStatusText(status) {
      const statusMap = {
        draft: '草稿',
        pending_review: '待审核',
        published: '已发布',
        archived: '已下架'
      }
      return statusMap[status] || status
    },

    // 创建课程
    goToCreateCourse() {
      this.$router.push('/teacher/courses/create')
    },

    // 查看课程
    viewCourse(course) {
      this.$router.push(`/courses/${course.id}`)
    },

    // 查看课程（讲师视角）
    viewTeachingCourse(course) {
      this.$router.push(`/teacher/courses/${course.id}`)
    },

    // 发布课程
    publishCourse(course) {
      this.$confirm('确认发布此课程？发布后需要管理员审核。', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      })
        .then(() => {
          this.$api.put(`/courses/${course.id}/publish`)
            .then(() => {
              this.$message.success('课程发布成功，请等待审核')
              this.fetchMyCourses()
            })
            .catch(err => {
              this.$message.error(err.response?.data?.message || '发布失败')
            })
        })
        .catch(() => {})
    },

    // 下架课程
    archiveCourse(course) {
      this.$confirm('确认下架此课程？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      })
        .then(() => {
          this.$api.put(`/courses/${course.id}/archive`)
            .then(() => {
              this.$message.success('课程已下架')
              this.fetchMyCourses()
            })
            .catch(err => {
              this.$message.error(err.response?.data?.message || '操作失败')
            })
        })
        .catch(() => {})
    },

    // 删除课程
    deleteCourse(course) {
      this.$confirm('确认删除此课程？此操作不可撤销。', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      })
        .then(() => {
          this.$api.delete(`/courses/${course.id}`)
            .then(() => {
              this.$message.success('课程已删除')
              this.fetchMyCourses()
            })
            .catch(err => {
              this.$message.error(err.response?.data?.message || '删除失败')
            })
        })
        .catch(() => {})
    },

    // 进入课程学习（学生视角）
    enterCourse(course) {
      this.$router.push(`/student/courses/${course.id}`)
    },

    // 退课
    dropCourse(course) {
      this.$confirm('确认退课？退课后将无法继续学习该课程。', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      })
        .then(() => {
          this.$api.post(`/user/courses/${course.id}/drop`)
            .then(() => {
              this.$message.success('已退课')
              this.fetchLearningCourses()
            })
            .catch(err => {
              this.$message.error(err.response?.data?.message || '退课失败')
            })
        })
        .catch(() => {})
    },

    // 去选课
    goCourseCenter() {
      this.$router.push('/courses')
    },

    // 学生功能导航
    goToEnrollment() {
      this.$router.push('/courses')
    },

    goToExamCenter() {
      this.$router.push('/teacher/exams')
    },

    goToHomeworkCenter() {
      this.$router.push('/teacher/homework')
    }
  }
}
</script>

<style scoped lang="scss">
.my-courses-container {
  padding: 1.5rem;
  background: #f9fafb;
  min-height: 100vh;
}

.page-header {
  margin-bottom: 1rem;
  text-align: center;
  padding: 0.8rem 1rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 8px;
  color: white;
  box-shadow: 0 2px 6px rgba(102, 126, 234, 0.2);
}

.page-header h1 {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 700;
}

.subtitle {
  margin: 0.25rem 0 0 0;
  color: rgba(255, 255, 255, 0.9);
  font-size: 0.875rem;
}

.tabs-container {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  overflow: hidden;

  ::v-deep .el-tabs__header {
    margin: 0;
    background: #f8f9fa;
    padding: 0 1.5rem;
  }

  ::v-deep .el-tabs__nav {
    border: none;
  }

  ::v-deep .el-tabs__item {
    height: 3.5rem;
    line-height: 3.5rem;
    font-size: 1rem;
    font-weight: 600;
    border: none;
    color: #6b7280;
  }

  ::v-deep .el-tabs__item.is-active {
    color: #667eea;
    background: white;
  }

  ::v-deep .el-tabs__content {
    padding: 1.5rem;
  }
}

.tab-content .action-bar {
  margin-bottom: 1.5rem;
  display: flex;
  gap: 0.75rem;
  flex-wrap: wrap;
  padding: 1rem;
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  border-radius: 8px;
}

.action-bar .el-button {
  border-radius: 8px;
  font-weight: 600;
  transition: all 0.3s;
}

.action-bar .el-button--primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
}

.action-bar .el-button:not(.el-button--primary) {
  background: white;
  border: 2px solid #e5e7eb;
}

.action-bar .el-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.courses-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
}

.course-card {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  border: 1px solid #e5e7eb;
}

.course-card:hover {
  box-shadow: 0 8px 24px rgba(102, 126, 234, 0.2);
  transform: translateY(-4px);
  border-color: #667eea;
}

.course-cover {
  position: relative;
  width: 100%;
  height: 180px;
  overflow: hidden;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.course-cover img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s;
}

.course-card:hover .course-cover img {
  transform: scale(1.05);
}

.status-badge {
  position: absolute;
  top: 0.75rem;
  right: 0.75rem;
  padding: 0.375rem 0.75rem;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 600;
  color: white;
  backdrop-filter: blur(10px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

.status-badge.draft {
  background: rgba(144, 147, 153, 0.95);
}

.status-badge.pending_review {
  background: rgba(230, 162, 60, 0.95);
}

.status-badge.published {
  background: rgba(103, 194, 58, 0.95);
}

.status-badge.archived {
  background: rgba(144, 147, 153, 0.95);
}

.course-info {
  padding: 1.25rem;
}

.course-info h3 {
  margin: 0 0 0.75rem 0;
  font-size: 1.125rem;
  color: #1f2937;
  font-weight: 700;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.description {
  margin: 0.5rem 0;
  font-size: 0.875rem;
  color: #6b7280;
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  line-clamp: 2;
  overflow: hidden;
  min-height: 2.625rem;
}

.course-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin: 0.75rem 0;
  padding: 0.75rem 0;
  border-top: 1px solid #e5e7eb;
  border-bottom: 1px solid #e5e7eb;
  font-size: 0.875rem;
}

.category {
  color: #667eea;
  background: linear-gradient(135deg, #f0f4ff 0%, #e9ecff 100%);
  padding: 0.25rem 0.625rem;
  border-radius: 6px;
  font-weight: 600;
}

.price {
  color: #e74c3c;
  font-weight: 700;
  font-size: 1.125rem;
}

.teacher {
  color: #6b7280;
  font-weight: 500;
}

.statistics {
  display: flex;
  justify-content: space-around;
  margin: 0.75rem 0;
  padding: 0.75rem;
  background: #f9fafb;
  border-radius: 8px;
}

.stat-item {
  text-align: center;
}

.stat-item .label {
  display: block;
  font-size: 0.75rem;
  color: #9ca3af;
  margin-bottom: 0.25rem;
  font-weight: 500;
}

.stat-item .value {
  display: block;
  font-size: 1.25rem;
  font-weight: 700;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.progress-container {
  margin: 0.75rem 0;
  padding: 0.75rem 0;
}

.progress-container .label {
  display: block;
  font-size: 0.75rem;
  color: #9ca3af;
  margin-bottom: 0.5rem;
  font-weight: 500;
}

.actions {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
  margin-top: 1rem;
}

.actions .el-button {
  flex: 1;
  min-width: 60px;
  padding: 0.5rem 0.75rem;
  font-size: 0.875rem;
  border-radius: 6px;
  font-weight: 600;
  transition: all 0.3s;
}

.actions .el-button--primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
}

.actions .el-button--text {
  color: #6b7280;
}

.actions .el-button:hover {
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

.empty-state {
  text-align: center;
  padding: 4rem 1.5rem;
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  border-radius: 12px;
  margin: 1rem 0;
}

.empty-state i {
  font-size: 4rem;
  color: #cbd5e0;
  display: block;
  margin-bottom: 1.5rem;
}

.empty-state p {
  font-size: 1rem;
  color: #6b7280;
  margin-bottom: 1.5rem;
  font-weight: 500;
}

.empty-state .el-button {
  border-radius: 8px;
  padding: 0.75rem 2rem;
  font-weight: 600;
}
</style>
