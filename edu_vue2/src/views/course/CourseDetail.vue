<template>
  <div class="course-detail">
    <div class="course-header">
      <h1>{{ course.name }}</h1>
      <p>讲师：{{ course.instructor }}</p>
    </div>

    <section class="course-intro">
      <div class="intro-content">
        <div class="intro-section">
          <h2>课程简介</h2>
          <p>{{ course.description }}</p>
        </div>
        <div class="intro-section">
          <h2>学习目标</h2>
          <ul>
            <li v-for="(goal, idx) in course.goals" :key="idx">{{ goal }}</li>
          </ul>
        </div>
        <div class="intro-section">
          <h2>课程大纲</h2>
          <div v-for="(section, idx) in course.sections" :key="idx" class="section">
            <h3>{{ section.title }}</h3>
            <ul>
              <li v-for="lesson in section.lessons" :key="lesson.id">
                {{ lesson.name }}
              </li>
            </ul>
          </div>
        </div>
      </div>

      <aside class="intro-sidebar">
        <div class="info-card">
          <h3>课程信息</h3>
          <div class="info-item">
            <span>👥 学生数</span>
            <strong>{{ course.studentCount }}</strong>
          </div>
          <div class="info-item">
            <span>⭐ 评分</span>
            <strong>{{ course.rating }}</strong>
          </div>
          <div class="info-item">
            <span>📚 课时数</span>
            <strong>{{ course.lessonCount }}</strong>
          </div>
          <button v-if="!isEnrolled" @click="joinCourse" class="enroll-btn">
            {{ enrollLoading ? '加入中...' : '加入课程' }}
          </button>
          <button v-else class="enrolled-btn" disabled>已加入</button>
        </div>
      </aside>
    </section>
  </div>
</template>

<script>
export default {
  name: 'CourseDetail',
  data() {
    return {
      courseId: this.$route.params.id,
      isEnrolled: false,
      enrollLoading: false,
      course: {}
    }
  },
  created() {
    this.loadCourseDetail()
  },
  watch: {
    '$route.params.id': function() {
      this.loadCourseDetail()
    }
  },
  methods: {
    loadCourseDetail() {
      // 根据 courseId 加载对应课程
      const coursesData = {
        1: {
          id: 1,
          name: 'Vue.js 从入门到精通',
          instructor: '张三',
          description: '这是一个完整的Vue.js课程，从基础到高级应用',
          rating: 4.8,
          studentCount: 1250,
          lessonCount: 48,
          goals: ['掌握Vue.js基础', '能够开发应用', '理解组件化', '使用Vuex'],
          sections: [
            {
              title: '第一章：Vue基础',
              lessons: [
                { id: 1, name: '认识Vue.js', type: 'video' },
                { id: 2, name: '环境搭建', type: 'video' }
              ]
            }
          ]
        },
        2: {
          id: 2,
          name: 'Python 数据科学',
          instructor: '李四',
          description: '掌握数据分析和机器学习的基础知识',
          rating: 4.7,
          studentCount: 980,
          lessonCount: 40,
          goals: ['学习Python', '掌握数据分析', '理解机器学习'],
          sections: [
            {
              title: '第一章：Python基础',
              lessons: [
                { id: 1, name: 'Python简介', type: 'video' }
              ]
            }
          ]
        },
        3: {
          id: 3,
          name: 'Web 全栈开发',
          instructor: '王五',
          description: '前后端完整的Web开发课程',
          rating: 4.9,
          studentCount: 750,
          lessonCount: 60,
          goals: ['学习前端', '学习后端', '理解架构'],
          sections: [
            {
              title: '第一章：前端基础',
              lessons: [
                { id: 1, name: 'HTML基础', type: 'video' }
              ]
            }
          ]
        },
        101: {
          id: 101,
          name: '高级JavaScript开发',
          instructor: '讲师',
          description: '深入学习JavaScript的高级特性',
          rating: 4.7,
          studentCount: 320,
          lessonCount: 24,
          goals: ['掌握JS高级特性'],
          sections: [
            {
              title: '第一章',
              lessons: [{ id: 1, name: '课程1', type: 'video' }]
            }
          ]
        }
      }
      
      this.course = coursesData[this.courseId] || {
        id: this.courseId,
        name: '课程 ' + this.courseId,
        instructor: '讲师',
        description: '课程描述',
        rating: 0,
        studentCount: 0,
        lessonCount: 0,
        goals: [],
        sections: []
      }
    },
    async joinCourse() {
      this.enrollLoading = true
      try {
        this.isEnrolled = true
        this.$message.success('已加入课程！')
        setTimeout(() => {
          this.$router.push('/user-center/my-courses')
        }, 500)
      } catch (error) {
        this.$message.error('加入失败：' + error.message)
      } finally {
        this.enrollLoading = false
      }
    }
  }
}
</script>

<style scoped>
.course-detail {
  width: 100%;
}

.course-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 2rem;
  border-radius: 8px;
  margin-bottom: 2rem;
}

.course-header h1 {
  margin: 0 0 0.5rem 0;
  font-size: 2rem;
}

.course-header p {
  margin: 0;
  opacity: 0.9;
}

.course-intro {
  display: grid;
  grid-template-columns: 1fr 300px;
  gap: 2rem;
}

.intro-content {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.intro-section {
  margin-bottom: 2rem;
}

.intro-section:last-child {
  margin-bottom: 0;
}

.intro-section h2 {
  color: #2c3e50;
  margin: 0 0 1rem 0;
  font-size: 1.3rem;
}

.intro-section h3 {
  color: #2c3e50;
  margin: 0 0 0.75rem 0;
  font-size: 1rem;
}

.intro-section p {
  color: #7f8c8d;
  line-height: 1.6;
  margin: 0;
}

.intro-section ul {
  padding-left: 1.5rem;
  margin: 0;
}

.intro-section li {
  color: #7f8c8d;
  margin-bottom: 0.5rem;
}

.section {
  margin-bottom: 1.5rem;
}

.intro-sidebar {
  height: fit-content;
  position: sticky;
  top: 100px;
}

.info-card {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.info-card h3 {
  margin: 0 0 1rem 0;
  color: #2c3e50;
  font-size: 1rem;
}

.info-item {
  display: flex;
  justify-content: space-between;
  padding: 0.75rem 0;
  border-bottom: 1px solid #ecf0f1;
  color: #7f8c8d;
  font-size: 0.9rem;
}

.info-item strong {
  color: #667eea;
  font-weight: 600;
}

.enroll-btn,
.enrolled-btn {
  width: 100%;
  padding: 0.75rem;
  margin-top: 1rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s;
}

.enroll-btn {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.enroll-btn:hover {
  opacity: 0.9;
}

.enrolled-btn {
  background-color: #95a5a6;
  color: white;
  cursor: not-allowed;
}

@media (max-width: 768px) {
  .course-intro {
    grid-template-columns: 1fr;
  }

  .intro-sidebar {
    position: static;
  }
}
</style>
