<template>
  <div class="enrollment-container">
    <div class="page-header">
      <button class="back-btn" @click="goBack">
        <i class="el-icon-arrow-left"></i> 返回
      </button>
      <h1>🎓 课程报名</h1>
      <p class="subtitle">选择班期和班级，开启学习之旅</p>
    </div>

    <el-card shadow="hover" class="enrollment-wrapper">
      <el-steps :active="step" process-status="wait" align-center style="margin-bottom: 40px">
        <el-step title="选择班期" />
        <el-step title="选择班级" />
        <el-step title="确认报名" />
      </el-steps>

      <!-- 第一步：选择班期 -->
      <div v-if="step === 0" class="step-content">
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
            </div>
            <div class="term-details">
              <p><strong>开始日期：</strong>{{ term.start_date }}</p>
              <p><strong>结束日期：</strong>{{ term.end_date }}</p>
              <p><strong>已报名：</strong>{{ term.current_enrollment }} 人</p>
            </div>
            <div v-if="formData.termId === term.id" class="check-mark">
              ✓
            </div>
          </div>
        </div>

        <div v-else class="empty-state">
          <i class="el-icon-warning-outline" style="font-size: 64px; color: #909399;"></i>
          <p>该课程暂无可用班期</p>
          <p class="hint">请联系老师或稍后再试</p>
        </div>

        <div class="step-actions">
          <el-button
            type="primary"
            size="large"
            :disabled="!formData.termId"
            @click="step = 1"
          >
            下一步 <i class="el-icon-arrow-right"></i>
          </el-button>
        </div>
      </div>

      <!-- 第二步：选择班级 -->
      <div v-if="step === 1" class="step-content">
        <h3>选择班级</h3>
        <p class="tip">班期：<strong>{{ selectedTermName }}</strong></p>

        <div v-if="availableClasses.length > 0" class="classes-grid">
          <div
            v-for="classItem in availableClasses"
            :key="classItem.id"
            class="class-item"
            :class="{ selected: formData.classId === classItem.id, disabled: isClassFull }"
            @click="selectClass(classItem)"
          >
            <div class="class-header">
              <h4>{{ classItem.name }}</h4>
            </div>
            <div class="class-details">
              <p><strong>教师：</strong>{{ classItem.head_teacher?.name || '未分配' }}</p>
              <p><strong>已报名：</strong>{{ classItem.current_count }} 人</p>
            </div>
            <div v-if="formData.classId === classItem.id" class="check-mark">
              ✓
            </div>
          </div>
        </div>

        <div v-else class="empty-state">
          <i class="el-icon-warning-outline" style="font-size: 64px; color: #909399;"></i>
          <p>该班期暂无可用班级</p>
          <p class="hint">请选择其他班期或联系老师</p>
        </div>

        <div class="step-actions">
          <el-button @click="step = 0" size="large">
            <i class="el-icon-arrow-left"></i> 上一步
          </el-button>
          <el-button
            type="primary"
            size="large"
            :disabled="!formData.classId"
            @click="step = 2"
          >
            下一步<i class="el-icon-arrow-right"></i>
          </el-button>
        </div>
      </div>

      <!-- 第三步：确认报名 -->
      <div v-if="step === 2" class="step-content">
        <h3>确认报名信息</h3>

        <div class="confirm-info">
          <el-row :gutter="20">
            <el-col :span="12">
              <div class="info-box">
                <h4>📚 课程信息</h4>
                <p><span class="label">课程名称：</span>{{ selectedCourseTitle }}</p>
                <p><span class="label">课程价格：</span>{{ isFree ? '免费' : `¥${selectedCoursePrice}` }}</p>
              </div>
            </el-col>
            <el-col :span="12">
              <div class="info-box">
                <h4>📅 班期信息</h4>
                <p><span class="label">班期名称：</span>{{ selectedTermName }}</p>
                <p><span class="label">开始日期：</span>{{ selectedTermStartDate }}</p>
                <p><span class="label">结束日期：</span>{{ selectedTermEndDate }}</p>
              </div>
            </el-col>
          </el-row>

          <el-row :gutter="20" style="margin-top: 20px">
            <el-col :span="24">
              <div class="info-box">
                <h4>👥 班级信息</h4>
                <p><span class="label">班级名称：</span>{{ selectedClassName }}</p>
                <p><span class="label">班主任：</span>{{ selectedClassTeacher }}</p>
                <p><span class="label">已报名：</span>{{ selectedClassStudentCount }} 人</p>
              </div>
            </el-col>
          </el-row>
        </div>

        <div class="agreement">
          <el-checkbox v-model="agreeTerms">
            我已阅读并同意 <a href="javascript:void(0)">《课程学习协议》</a> 和 <a href="javascript:void(0)">《隐私政策》</a>
          </el-checkbox>
        </div>

        <div class="step-actions">
          <el-button @click="step = 1" size="large">
            <i class="el-icon-arrow-left"></i> 上一步
          </el-button>
          <el-button
            type="primary"
            size="large"
            :loading="submitting"
            :disabled="!agreeTerms"
            @click="confirmEnroll"
          >
            <i class="el-icon-check"></i> 确认报名
          </el-button>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script>
import { courseAPI } from '@/api'

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
      submitting: false,
      agreeTerms: false,
      loading: false,
      formData: {
        courseId: '',
        termId: '',
        classId: ''
      },
      // 后端返回的数据
      courseInfo: null,
      availableTerms: [],
      availableClasses: []
    }
  },

  async created() {
    // 从路由参数获取课程ID
    const courseId = this.$route.query.courseId
    if (courseId) {
      this.formData.courseId = String(courseId)
      // 加载课程班期班级信息
      await this.loadEnrollmentInfo()
    } else {
      this.$message.error('未指定课程')
      this.$router.push('/courses')
    }
  },

  computed: {
    selectedCourseTitle() {
      return this.courseInfo?.course_title || '加载中...'
    },

    selectedCoursePrice() {
      return this.courseInfo?.price || 0
    },

    isFree() {
      return this.courseInfo?.is_free || false
    },

    selectedTermName() {
      const term = this.availableTerms.find(t => t.id === this.formData.termId)
      return term ? term.name : ''
    },

    selectedTermStartDate() {
      const term = this.availableTerms.find(t => t.id === this.formData.termId)
      return term ? term.start_date : ''
    },

    selectedTermEndDate() {
      const term = this.availableTerms.find(t => t.id === this.formData.termId)
      return term ? term.end_date : ''
    },

    selectedClassName() {
      const classItem = this.availableClasses.find(c => c.id === this.formData.classId)
      return classItem ? classItem.name : ''
    },

    selectedClassTeacher() {
      const classItem = this.availableClasses.find(c => c.id === this.formData.classId)
      return classItem?.head_teacher?.name || '未分配'
    },

    selectedClassStudentCount() {
      const classItem = this.availableClasses.find(c => c.id === this.formData.classId)
      return classItem ? classItem.current_count : 0
    },

    isClassFull() {
      // 后端没有返回 capacity，暂时不做满员判断
      return false
    }
  },

  methods: {
    async loadEnrollmentInfo() {
      this.loading = true
      try {
        const response = await courseAPI.getEnrollmentInfo(this.formData.courseId)
        const data = response.data || response
        
        this.courseInfo = {
          course_id: data.course_id,
          course_title: data.course_title,
          price: data.price,
          is_free: data.is_free
        }
        
        // 映射班期数据
        this.availableTerms = (data.terms || []).map(term => ({
          id: term.id,
          name: term.name,
          start_date: term.start_date,
          end_date: term.end_date,
          enrollment_limit: term.enrollment_limit,
          current_enrollment: term.current_enrollment,
          is_full: term.is_full,
          classes: term.classes || []
        }))
        
      } catch (error) {
        console.error('加载课程信息失败:', error)
        this.$message.error('加载课程信息失败')
        this.$router.push('/courses')
      } finally {
        this.loading = false
      }
    },

    goBack() {
      if (this.formData.courseId) {
        this.$router.push(`/courses/${this.formData.courseId}`)
      } else {
        this.$router.go(-1)
      }
    },

    selectTerm(term) {
      this.formData.termId = term.id
      // 加载该班期下的班级
      this.availableClasses = term.classes.map(cls => ({
        id: cls.id,
        name: cls.name,
        head_teacher: cls.head_teacher,
        current_count: cls.current_count || 0
      }))
      // 重置班级选择
      this.formData.classId = ''
    },

    selectClass(classItem) {
      // 直接选择，不做满员判断
      this.formData.classId = classItem.id
    },

    async confirmEnroll() {
      if (!this.agreeTerms) {
        this.$message.warning('请先阅读并同意相关协议')
        return
      }

      this.submitting = true

      try {
        const enrollData = {
          term_id: this.formData.termId,
          class_id: this.formData.classId
        }
        
        const response = await courseAPI.enrollCourse(this.formData.courseId, enrollData)
        const data = response.data || response

        this.$message.success('选课成功！')
        
        if (data.is_free || !data.need_payment) {
          // 免费课程直接进入课程页面
          this.$message.success('正在进入课程...')
          setTimeout(() => {
            this.$router.push(`/student/courses/${this.formData.courseId}`)
          }, 1000)
        } else {
          // 付费课程显示缴费等待状态
          this.$alert(
            `选课成功！请完成支付（￥${data.price}）后方可学习课程。`,
            '等待支付',
            {
              confirmButtonText: '确定',
              type: 'warning',
              callback: () => {
                this.$router.push('/courses/mycourses')
              }
            }
          )
        }
      } catch (error) {
        console.error('选课失败:', error)
        this.$message.error(error.response?.data?.message || '选课失败，请稍后重试')
      } finally {
        this.submitting = false
      }
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
  margin-bottom: 20px;
  text-align: center;
  padding: 0.5rem 0; /* 稍微增加了内边距，让空间更充裕 */
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 12px;
  color: white;
  position: relative; /* 必须为 relative 才能让按钮绝对定位 */

  .back-btn {
    position: absolute;
    left: 1.5rem;
    top: 50%;
    transform: translateY(-50%);
    background: rgba(255, 255, 255, 0.2); /* 半透明毛玻璃效果 */
    border: none;
    color: white;
    padding: 0.6rem 1.2rem;
    border-radius: 8px;
    cursor: pointer;
    font-size: 0.9rem;
    font-weight: 600;
    display: flex;
    align-items: center;
    gap: 0.4rem;
    transition: all 0.3s;
    backdrop-filter: blur(4px); /* 背景模糊 */

    &:hover {
      background: rgba(255, 255, 255, 0.3);
      transform: translateY(-50%) translateX(-3px); /* 悬停微移 */
    }

    i {
      font-weight: bold;
    }
  }

  h1 {
    margin: 0 0 10px 0;
    font-size: 32px;
    font-weight: 700;
  }

  .subtitle {
    margin: 0;
    font-size: 16px;
    opacity: 0.9;
  }
}

.enrollment-wrapper {
  max-width: 1000px;
  margin: 0 auto;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.08);

  ::v-deep .el-steps {
    .el-step__title {
      font-size: 16px;
      font-weight: 600;
    }

    .el-step__head.is-process {
      color: #667eea;
      border-color: #667eea;
    }

    .el-step__head.is-finish {
      color: #67c23a;
      border-color: #67c23a;
    }
  }

  .step-content {
    min-height: 400px;
    padding: 30px 0;

    h3 {
      font-size: 22px;
      color: #2c3e50;
      margin-bottom: 20px;
      font-weight: 700;
      padding-bottom: 15px;
      border-bottom: 3px solid #667eea;
      display: inline-block;
    }

    .tip {
      margin-bottom: 25px;
      padding: 15px 20px;
      background: #f0f7ff;
      border-left: 4px solid #667eea;
      border-radius: 4px;
      color: #606266;
      font-size: 15px;

      strong {
        color: #667eea;
        font-weight: 600;
      }
    }

    .hint {
      font-size: 13px;
      color: #909399;
      margin-top: 8px;
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
    border: 2px solid #e4e7ed;
    border-radius: 12px;
    padding: 24px;
    cursor: pointer;
    transition: all 0.3s ease;
    background: white;

    &:hover {
      border-color: #667eea;
      box-shadow: 0 8px 16px rgba(102, 126, 234, 0.15);
      transform: translateY(-4px);
    }

    &.selected {
      border-color: #667eea;
      background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%);
      box-shadow: 0 4px 12px rgba(102, 126, 234, 0.2);
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
      bottom: 15px;
      right: 15px;
      width: 36px;
      height: 36px;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: white;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: bold;
      font-size: 20px;
      box-shadow: 0 2px 8px rgba(102, 126, 234, 0.4);
    }
  }

  .empty-state {
    text-align: center;
    padding: 80px 20px;
    color: #909399;

    i {
      font-size: 72px;
      display: block;
      margin-bottom: 20px;
      color: #c0c4cc;
    }

    p {
      margin: 10px 0;
      font-size: 16px;
      color: #606266;

      &.hint {
        font-size: 14px;
        color: #909399;
      }
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
    justify-content: space-between;
    gap: 20px;
    margin-top: 40px;
    padding-top: 30px;
    border-top: 2px solid #f0f0f0;

    .el-button {
      flex: 1;
      max-width: 200px;
      height: 48px;
      font-size: 16px;
      font-weight: 600;
      border-radius: 8px;
      transition: all 0.3s;

      &.el-button--primary {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border: none;

        &:hover:not(:disabled) {
          transform: translateY(-2px);
          box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
        }
      }

      i {
        font-weight: bold;
      }
    }

    &:has(.el-button:only-child) {
      justify-content: center;
    }
  }
}
</style>
