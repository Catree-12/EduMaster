<template>
  <div class="enrollment-container">
    <div class="page-header">
      <h1>选课报名</h1>
      <p class="subtitle">选择课程和班期，立即报名学习</p>
    </div>

    <el-card shadow="hover" class="enrollment-wrapper">
      <el-steps :active="step" process-status="wait" align-center style="margin-bottom: 40px">
        <el-step title="选择课程" />
        <el-step title="选择班期" />
        <el-step title="选择班级" />
        <el-step title="确认报名" />
      </el-steps>

      <!-- 第一步：选择课程 -->
      <div v-if="step === 0" class="step-content">
        <h3>选择课程</h3>
        
        <!-- 搜索和筛选 -->
        <div class="filters">
          <el-input
            v-model="courseSearch"
            placeholder="搜索课程名称..."
            prefix-icon="el-icon-search"
            style="width: 250px"
          />
          <el-select
            v-model="selectedCategory"
            placeholder="课程分类"
            style="width: 150px; margin-left: 10px"
            clearable
          >
            <el-option label="Web 前端" value="web" />
            <el-option label="后端开发" value="backend" />
            <el-option label="移动开发" value="mobile" />
            <el-option label="数据科学" value="data" />
          </el-select>
        </div>

        <!-- 课程列表 -->
        <div class="courses-grid">
          <div
            v-for="course in filteredCourses"
            :key="course.id"
            class="course-item"
            :class="{ selected: formData.courseId === course.id }"
            @click="selectCourse(course)"
          >
            <div class="course-cover">
              <img :src="course.coverImage" :alt="course.title" />
            </div>
            <div class="course-info">
              <h4>{{ course.title }}</h4>
              <p class="category">{{ getCategoryText(course.category) }}</p>
              <p class="description">{{ course.description | truncate(100) }}</p>
              <div class="course-meta">
                <span>👥 {{ course.studentCount }} 人</span>
                <span>⭐ {{ course.rating }}</span>
                <span>¥{{ course.price }}</span>
              </div>
            </div>
            <div v-if="formData.courseId === course.id" class="check-mark">
              ✓
            </div>
          </div>
        </div>

        <div class="step-actions">
          <el-button @click="step = 0" disabled>上一步</el-button>
          <el-button
            type="primary"
            :disabled="!formData.courseId"
            @click="step = 1"
          >
            下一步
          </el-button>
        </div>
      </div>

      <!-- 第二步：选择班期 -->
      <div v-if="step === 1" class="step-content">
        <h3>选择班期</h3>
        <p class="tip">课程：<strong>{{ selectedCourseTitle }}</strong></p>

        <div v-if="availableTerms.length > 0" class="terms-grid">
          <div
            v-for="term in availableTerms"
            :key="term.id"
            class="term-item"
            :class="{ selected: formData.termId === term.id }"
            @click="selectTerm(term)"
          >
            <div class="term-header">
              <h4>{{ term.name }}</h4>
              <el-tag :type="getStatusType(term.status)">
                {{ getStatusText(term.status) }}
              </el-tag>
            </div>
            <div class="term-details">
              <p><strong>开始日期：</strong>{{ term.startDate }}</p>
              <p><strong>结束日期：</strong>{{ term.endDate }}</p>
              <p><strong>班级数：</strong>{{ term.classCount }}</p>
              <p><strong>已报名：</strong>{{ term.studentCount }} 人</p>
            </div>
            <div v-if="formData.termId === term.id" class="check-mark">
              ✓
            </div>
          </div>
        </div>

        <div v-else class="empty-state">
          <i class="el-icon-document-copy" />
          <p>暂无可用班期</p>
        </div>

        <div class="step-actions">
          <el-button @click="step = 0">上一步</el-button>
          <el-button
            type="primary"
            :disabled="!formData.termId"
            @click="step = 2"
          >
            下一步
          </el-button>
        </div>
      </div>

      <!-- 第三步：选择班级 -->
      <div v-if="step === 2" class="step-content">
        <h3>选择班级</h3>
        <p class="tip">班期：<strong>{{ selectedTermName }}</strong></p>

        <div v-if="availableClasses.length > 0" class="classes-grid">
          <div
            v-for="classItem in availableClasses"
            :key="classItem.id"
            class="class-item"
            :class="{ selected: formData.classId === classItem.id }"
            @click="selectClass(classItem)"
          >
            <div class="class-header">
              <h4>{{ classItem.name }}</h4>
              <span class="class-code">{{ classItem.code }}</span>
            </div>
            <div class="class-details">
              <p><strong>教师：</strong>{{ classItem.teacherName }}</p>
              <p><strong>已报名：</strong>{{ classItem.studentCount }}/{{ classItem.capacity }}</p>
              <el-progress
                :percentage="Math.round((classItem.studentCount / classItem.capacity) * 100)"
                :format="() => `${classItem.studentCount}/${classItem.capacity}`"
              />
            </div>
            <div v-if="classItem.studentCount >= classItem.capacity" class="full-mark">
              已满
            </div>
            <div v-if="formData.classId === classItem.id" class="check-mark">
              ✓
            </div>
          </div>
        </div>

        <div v-else class="empty-state">
          <i class="el-icon-document-copy" />
          <p>暂无可用班级</p>
        </div>

        <div class="step-actions">
          <el-button @click="step = 1">上一步</el-button>
          <el-button
            type="primary"
            :disabled="!formData.classId || isClassFull"
            @click="step = 3"
          >
            下一步
          </el-button>
        </div>
      </div>

      <!-- 第四步：确认报名 -->
      <div v-if="step === 3" class="step-content">
        <h3>确认报名信息</h3>

        <div class="confirm-info">
          <el-row :gutter="20">
            <el-col :span="12">
              <div class="info-box">
                <h4>课程信息</h4>
                <p><span class="label">课程名称：</span>{{ selectedCourseTitle }}</p>
                <p><span class="label">价格：</span>¥{{ selectedCoursePrice }}</p>
                <p><span class="label">分类：</span>{{ getCategoryText(selectedCourseCategory) }}</p>
              </div>
            </el-col>
            <el-col :span="12">
              <div class="info-box">
                <h4>班期信息</h4>
                <p><span class="label">班期名称：</span>{{ selectedTermName }}</p>
                <p><span class="label">开始日期：</span>{{ selectedTermStartDate }}</p>
                <p><span class="label">结束日期：</span>{{ selectedTermEndDate }}</p>
              </div>
            </el-col>
          </el-row>

          <el-row :gutter="20" style="margin-top: 20px">
            <el-col :span="24">
              <div class="info-box">
                <h4>班级信息</h4>
                <p><span class="label">班级名称：</span>{{ selectedClassName }}</p>
                <p><span class="label">班级代码：</span>{{ selectedClassCode }}</p>
                <p><span class="label">教师：</span>{{ selectedClassTeacher }}</p>
                <p><span class="label">班级人数：</span>{{ selectedClassStudentCount }}/{{ selectedClassCapacity }}</p>
              </div>
            </el-col>
          </el-row>
        </div>

        <div class="agreement">
          <el-checkbox v-model="agreeTerms">
            我已阅读并同意
            <a href="#">《课程学习协议》</a>
            和
            <a href="#">《隐私政策》</a>
          </el-checkbox>
        </div>

        <div class="step-actions">
          <el-button @click="step = 2">上一步</el-button>
          <el-button
            type="primary"
            :loading="submitting"
            :disabled="!agreeTerms"
            @click="confirmEnroll"
          >
            确认报名
          </el-button>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script>
export default {
  name: 'StudentEnrollment',
  filters: {
    truncate(text, length) {
      if (text && text.length > length) {
        return text.substring(0, length) + '...'
      }
      return text
    }
  },
  data() {
    return {
      step: 0,
      courseSearch: '',
      selectedCategory: '',
      submitting: false,
      agreeTerms: false,
      formData: {
        courseId: '',
        termId: '',
        classId: ''
      },
      courses: [
        {
          id: '1',
          title: 'Vue.js 全栈开发',
          description: '掌握 Vue.js 框架，学习现代前端开发技术',
          category: 'web',
          price: 599,
          rating: 4.8,
          studentCount: 1200,
          coverImage: 'https://via.placeholder.com/300x200?text=Vue.js',
          terms: [
            {
              id: 't1',
              name: '2024年秋季班',
              startDate: '2024-09-01',
              endDate: '2024-12-31',
              classCount: 3,
              studentCount: 85,
              status: 'active'
            },
            {
              id: 't2',
              name: '2025年春季班',
              startDate: '2025-03-01',
              endDate: '2025-06-30',
              classCount: 2,
              studentCount: 0,
              status: 'upcoming'
            }
          ]
        },
        {
          id: '2',
          title: 'Python 数据科学',
          description: '学习 Python 进行数据分析和机器学习',
          category: 'data',
          price: 799,
          rating: 4.9,
          studentCount: 980,
          coverImage: 'https://via.placeholder.com/300x200?text=Python',
          terms: [
            {
              id: 't3',
              name: '2024年秋季班',
              startDate: '2024-09-15',
              endDate: '2024-12-15',
              classCount: 2,
              studentCount: 65,
              status: 'active'
            }
          ]
        },
        {
          id: '3',
          title: 'React 开发实战',
          description: '深入学习 React，打造高性能前端应用',
          category: 'web',
          price: 699,
          rating: 4.7,
          studentCount: 850,
          coverImage: 'https://via.placeholder.com/300x200?text=React',
          terms: [
            {
              id: 't4',
              name: '2024年秋季班',
              startDate: '2024-09-10',
              endDate: '2024-12-20',
              classCount: 2,
              studentCount: 50,
              status: 'active'
            },
            {
              id: 't5',
              name: '2025年春季班',
              startDate: '2025-03-15',
              endDate: '2025-06-15',
              classCount: 1,
              studentCount: 0,
              status: 'upcoming'
            }
          ]
        }
      ],
      classes: [
        {
          id: 'c1',
          name: '班级A',
          code: 'CLASS001',
          teacherName: '张老师',
          studentCount: 25,
          capacity: 30,
          status: 'active',
          termId: 't1'
        },
        {
          id: 'c2',
          name: '班级B',
          code: 'CLASS002',
          teacherName: '李老师',
          studentCount: 28,
          capacity: 30,
          status: 'active',
          termId: 't1'
        },
        {
          id: 'c3',
          name: '班级C',
          code: 'CLASS003',
          teacherName: '王老师',
          studentCount: 32,
          capacity: 30,
          status: 'active',
          termId: 't1'
        },
        {
          id: 'c4',
          name: '班级D',
          code: 'CLASS004',
          teacherName: '周老师',
          studentCount: 0,
          capacity: 30,
          status: 'active',
          termId: 't2'
        },
        {
          id: 'c5',
          name: '班级A',
          code: 'CLASS005',
          teacherName: '陈老师',
          studentCount: 20,
          capacity: 30,
          status: 'active',
          termId: 't3'
        }
      ]
    }
  },
  computed: {
    filteredCourses() {
      return this.courses.filter(course => {
        const matchSearch = course.title.includes(this.courseSearch)
        const matchCategory = !this.selectedCategory || course.category === this.selectedCategory
        return matchSearch && matchCategory
      })
    },

    selectedCourseTitle() {
      const course = this.courses.find(c => c.id === this.formData.courseId)
      return course ? course.title : ''
    },

    selectedCoursePrice() {
      const course = this.courses.find(c => c.id === this.formData.courseId)
      return course ? course.price : 0
    },

    selectedCourseCategory() {
      const course = this.courses.find(c => c.id === this.formData.courseId)
      return course ? course.category : ''
    },

    availableTerms() {
      const course = this.courses.find(c => c.id === this.formData.courseId)
      return course ? course.terms : []
    },

    selectedTermName() {
      const term = this.availableTerms.find(t => t.id === this.formData.termId)
      return term ? term.name : ''
    },

    selectedTermStartDate() {
      const term = this.availableTerms.find(t => t.id === this.formData.termId)
      return term ? term.startDate : ''
    },

    selectedTermEndDate() {
      const term = this.availableTerms.find(t => t.id === this.formData.termId)
      return term ? term.endDate : ''
    },

    availableClasses() {
      return this.classes.filter(c => c.termId === this.formData.termId)
    },

    selectedClassName() {
      const classItem = this.classes.find(c => c.id === this.formData.classId)
      return classItem ? classItem.name : ''
    },

    selectedClassCode() {
      const classItem = this.classes.find(c => c.id === this.formData.classId)
      return classItem ? classItem.code : ''
    },

    selectedClassTeacher() {
      const classItem = this.classes.find(c => c.id === this.formData.classId)
      return classItem ? classItem.teacherName : ''
    },

    selectedClassStudentCount() {
      const classItem = this.classes.find(c => c.id === this.formData.classId)
      return classItem ? classItem.studentCount : 0
    },

    selectedClassCapacity() {
      const classItem = this.classes.find(c => c.id === this.formData.classId)
      return classItem ? classItem.capacity : 0
    },

    isClassFull() {
      const classItem = this.classes.find(c => c.id === this.formData.classId)
      return classItem && classItem.studentCount >= classItem.capacity
    }
  },

  methods: {
    selectCourse(course) {
      this.formData.courseId = course.id
    },

    selectTerm(term) {
      this.formData.termId = term.id
    },

    selectClass(classItem) {
      if (classItem.studentCount < classItem.capacity) {
        this.formData.classId = classItem.id
      } else {
        this.$message.warning('此班级已满，请选择其他班级')
      }
    },

    getCategoryText(category) {
      const texts = {
        'web': 'Web 前端',
        'backend': '后端开发',
        'mobile': '移动开发',
        'data': '数据科学',
        'devops': 'DevOps',
        'other': '其他'
      }
      return texts[category] || category
    },

    getStatusType(status) {
      const types = {
        'active': 'success',
        'upcoming': 'info',
        'finished': 'warning',
        'canceled': 'danger'
      }
      return types[status] || 'info'
    },

    getStatusText(status) {
      const texts = {
        'active': '进行中',
        'upcoming': '即将开始',
        'finished': '已结束',
        'canceled': '已取消'
      }
      return texts[status] || status
    },

    confirmEnroll() {
      if (!this.agreeTerms) {
        this.$message.warning('请先阅读并同意相关协议')
        return
      }

      this.submitting = true

      // 调用API提交报名
      this.$api.post('/enrollments', {
        courseId: this.formData.courseId,
        termId: this.formData.termId,
        classId: this.formData.classId
      })
        .then(() => {
          this.$message.success('报名成功，欢迎开始学习！')
          this.submitting = false
          setTimeout(() => {
            this.$router.push('/course/my-courses')
          }, 1500)
        })
        .catch(err => {
          this.$message.error(err.response?.data?.message || '报名失败，请重试')
          this.submitting = false
        })
    }
  }
}
</script>

<style scoped lang="scss">
.enrollment-container {
  padding: 20px;
  background: #f5f7fa;
  min-height: 100vh;
}

.page-header {
  margin-bottom: 30px;

  h1 {
    margin: 0 0 10px 0;
    font-size: 28px;
    color: #333;
  }

  .subtitle {
    margin: 0;
    font-size: 14px;
    color: #999;
  }
}

.enrollment-wrapper {
  max-width: 1000px;
  margin: 0 auto;
  background: white;

  .step-content {
    min-height: 400px;
    padding: 30px 0;

    h3 {
      font-size: 18px;
      color: #333;
      margin-bottom: 20px;
      font-weight: bold;
    }

    .tip {
      margin-bottom: 20px;
      color: #666;
      font-size: 14px;

      strong {
        color: #333;
      }
    }
  }

  .filters {
    display: flex;
    gap: 10px;
    margin-bottom: 20px;
    align-items: center;
  }

  .courses-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: 20px;
    margin-bottom: 30px;
  }

  .course-item {
    position: relative;
    border: 2px solid #f0f0f0;
    border-radius: 8px;
    overflow: hidden;
    cursor: pointer;
    transition: all 0.3s;
    display: flex;
    flex-direction: column;

    &:hover {
      border-color: #3498db;
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
      transform: translateY(-5px);
    }

    &.selected {
      border-color: #3498db;
      background: #f0f7ff;
    }

    .course-cover {
      width: 100%;
      height: 150px;
      background: #f0f0f0;
      overflow: hidden;

      img {
        width: 100%;
        height: 100%;
        object-fit: cover;
      }
    }

    .course-info {
      flex: 1;
      padding: 15px;
      display: flex;
      flex-direction: column;

      h4 {
        margin: 0 0 8px 0;
        font-size: 14px;
        color: #333;
        font-weight: bold;
      }

      .category {
        margin: 0 0 8px 0;
        font-size: 12px;
        color: #999;
      }

      .description {
        margin: 0 0 10px 0;
        font-size: 12px;
        color: #666;
        line-height: 1.4;
        flex: 1;
      }

      .course-meta {
        display: flex;
        gap: 10px;
        font-size: 12px;
        color: #999;
      }
    }

    .check-mark {
      position: absolute;
      top: 10px;
      right: 10px;
      width: 30px;
      height: 30px;
      background: #3498db;
      color: white;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: bold;
      font-size: 18px;
    }
  }

  .terms-grid,
  .classes-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 20px;
    margin-bottom: 30px;
  }

  .term-item,
  .class-item {
    position: relative;
    border: 2px solid #f0f0f0;
    border-radius: 8px;
    padding: 20px;
    cursor: pointer;
    transition: all 0.3s;

    &:hover {
      border-color: #3498db;
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
      transform: translateY(-5px);
    }

    &.selected {
      border-color: #3498db;
      background: #f0f7ff;
    }

    .term-header,
    .class-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 15px;

      h4 {
        margin: 0;
        font-size: 15px;
        color: #333;
        font-weight: bold;
      }
    }

    .term-details,
    .class-details {
      font-size: 13px;

      p {
        margin: 8px 0;
        color: #666;

        strong {
          color: #333;
        }
      }
    }

    .full-mark {
      position: absolute;
      top: 10px;
      right: 10px;
      background: #f56c6c;
      color: white;
      padding: 4px 12px;
      border-radius: 4px;
      font-size: 12px;
      font-weight: bold;
    }

    .check-mark {
      position: absolute;
      bottom: 10px;
      right: 10px;
      width: 30px;
      height: 30px;
      background: #3498db;
      color: white;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: bold;
      font-size: 18px;
    }
  }

  .empty-state {
    text-align: center;
    padding: 60px 20px;
    color: #999;

    i {
      font-size: 48px;
      display: block;
      margin-bottom: 15px;
      color: #bbb;
    }

    p {
      margin: 0;
      font-size: 16px;
    }
  }

  .confirm-info {
    margin-bottom: 30px;

    .info-box {
      border: 1px solid #f0f0f0;
      border-radius: 8px;
      padding: 20px;
      background: #fafafa;

      h4 {
        margin: 0 0 15px 0;
        font-size: 14px;
        color: #333;
        font-weight: bold;
        border-bottom: 2px solid #f0f0f0;
        padding-bottom: 10px;
      }

      p {
        margin: 8px 0;
        font-size: 13px;
        color: #666;

        .label {
          font-weight: bold;
          color: #333;
          margin-right: 10px;
        }
      }
    }
  }

  .agreement {
    margin-bottom: 30px;
    padding: 15px;
    background: #f9f9f9;
    border-radius: 4px;
    text-align: center;

    a {
      color: #3498db;
      text-decoration: none;

      &:hover {
        text-decoration: underline;
      }
    }
  }

  .step-actions {
    display: flex;
    justify-content: center;
    gap: 20px;
    padding-top: 20px;
    border-top: 1px solid #f0f0f0;

    .el-button {
      min-width: 120px;
    }
  }
}
</style>
