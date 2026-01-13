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
                  <el-button type="text" size="small" @click="editCourse(course)">
                    编辑
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
            <el-button type="primary" icon="el-icon-circle-plus" @click="goToEnrollment">
              选课报名
            </el-button>
            <el-button icon="el-icon-trophy" @click="goToExamCenter">
              考试中心
            </el-button>
            <el-button icon="el-icon-document-copy" @click="goToHomeworkCenter">
              作业中心
            </el-button>
            <el-button icon="el-icon-award" @click="goToCertificates">
              我的证书
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

                <!-- 学习进度 -->
                <div class="progress-container">
                  <span class="label">学习进度</span>
                  <el-progress :percentage="course.progress" color="#1890ff" />
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
      this.$router.push('/course/create')
    },

    // 查看课程
    viewCourse(course) {
      this.$router.push(`/course/${course.id}`)
    },

    // 查看课程（讲师视角）
    viewTeachingCourse(course) {
      this.$router.push(`/teacher/course/${course.id}`)
    },

    // 编辑课程
    editCourse(course) {
      this.$router.push(`/teacher/course/${course.id}/edit`)
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
      this.$router.push(`/student/course/${course.id}`)
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
      this.$router.push('/course')
    },

    // 学生功能导航
    goToEnrollment() {
      this.$router.push('/course/enroll')
    },

    goToExamCenter() {
      this.$router.push('/exam-center')
    },

    goToHomeworkCenter() {
      this.$router.push('/homework-center')
    },

    goToCertificates() {
      this.$router.push('/user-center/certificates')
    }
  }
}
</script>

<style scoped lang="scss">
.my-courses-container {
  padding: 20px;
  background: #f5f7fa;
  min-height: 100vh;
}

.page-header {
  margin-bottom: 30px;
}

.page-header h1 {
  margin: 0;
  font-size: 28px;
  color: #333;
}

.subtitle {
  margin: 10px 0 0 0;
  color: #999;
  font-size: 14px;
}

.tabs-container {
  background: white;
  border-radius: 4px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);

  ::v-deep .el-tabs__content {
    padding: 20px;
  }
}

.tab-content .action-bar {
  margin-bottom: 20px;
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.courses-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
}

.course-card {
  background: white;
  border-radius: 4px;
  overflow: hidden;
  transition: all 0.3s ease;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.course-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  transform: translateY(-2px);
}

.course-cover {
  position: relative;
  width: 100%;
  height: 160px;
  overflow: hidden;
  background: #f0f0f0;
}

.course-cover img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.status-badge {
  position: absolute;
  top: 10px;
  right: 10px;
  padding: 4px 12px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: bold;
  color: white;
}

.status-badge.draft {
  background: #909399;
}

.status-badge.pending_review {
  background: #e6a23c;
}

.status-badge.published {
  background: #67c23a;
}

.status-badge.archived {
  background: #909399;
}

.course-info {
  padding: 15px;
}

.course-info h3 {
  margin: 0 0 10px 0;
  font-size: 16px;
  color: #333;
  font-weight: bold;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.description {
  margin: 8px 0;
  font-size: 13px;
  color: #666;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  line-clamp: 2;
  overflow: hidden;
}

.course-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin: 10px 0;
  padding: 10px 0;
  border-top: 1px solid #f0f0f0;
  border-bottom: 1px solid #f0f0f0;
  font-size: 13px;
}

.category {
  color: #1890ff;
  background: #e6f7ff;
  padding: 2px 8px;
  border-radius: 2px;
}

.price {
  color: #f56c6c;
  font-weight: bold;
}

.teacher {
  color: #666;
}

.statistics {
  display: flex;
  justify-content: space-around;
  margin: 10px 0;
  padding: 10px 0;
  border-top: 1px solid #f0f0f0;
}

.stat-item {
  text-align: center;
}

.stat-item .label {
  display: block;
  font-size: 12px;
  color: #999;
}

.stat-item .value {
  display: block;
  font-size: 16px;
  font-weight: bold;
  color: #333;
}

.progress-container {
  margin: 10px 0;
  padding: 10px 0;
}

.progress-container .label {
  display: block;
  font-size: 12px;
  color: #999;
  margin-bottom: 5px;
}

.actions {
  display: flex;
  gap: 5px;
  flex-wrap: wrap;
  margin-top: 10px;
}

.actions .el-button {
  flex: 1;
  min-width: 60px;
  padding: 6px 10px;
  font-size: 12px;
}

.empty-state {
  text-align: center;
  padding: 60px 20px;
}

.empty-state i {
  font-size: 64px;
  color: #ddd;
  display: block;
  margin-bottom: 20px;
}

.empty-state p {
  font-size: 14px;
  color: #999;
  margin-bottom: 20px;
}
</style>
