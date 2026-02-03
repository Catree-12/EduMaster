<template>
  <div class="course-detail">
    <div class="course-header">
      <button class="back-btn" @click="goBack">
        <i class="el-icon-arrow-left"></i> 返回
      </button>

      <div class="header-content">
        <h1>{{ course.name }}</h1>
        <p>讲师：{{ course.instructor }}</p>
      </div>

      <div class="header-decoration">
        <div class="decoration-circle circle-1"></div>
        <div class="decoration-circle circle-2"></div>
      </div>
    </div>

    <section class="course-intro">
      <div class="intro-content">
        <div class="intro-section">
          <h2>课程简介</h2>
          <p>{{ course.description }}</p>
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

    <section class="course-outline-section">
      <div class="outline-container">
        <h2 class="outline-title">📚 课程大纲</h2>
        <div v-if="course.sections && course.sections.length > 0" class="sections-list">
          <div v-for="(section, idx) in course.sections" :key="idx" class="section-item">
            <h3 class="section-title">{{ section.title }}</h3>
            <ul class="lessons-list">
              <li v-for="lesson in section.lessons" :key="lesson.id" class="lesson-item">
                <i class="el-icon-video-play"></i>
                {{ lesson.name }}
              </li>
            </ul>
          </div>
        </div>
        <div v-else class="no-outline">
          <i class="el-icon-document"></i>
          <p>暂无课程大纲</p>
        </div>
      </div>
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
    // 修改点 2：添加 goBack 方法
    goBack() {
      this.$router.push('/courses')
    },
    loadCourseDetail() {
      const coursesData = {
        1: {
          id: 1,
          name: 'Vue.js 从入门到精通',
          instructor: '张三',
          description: '这是一个完整的Vue.js课程，从基础到高级应用',
          rating: 4.8,
          studentCount: 1250,
          lessonCount: 48,
          sections: [
            {
              title: '第一章：Vue基础',
              lessons: [
                { id: 1, name: '认识Vue.js', type: 'video' },
                { id: 2, name: '环境搭建', type: 'video' }
              ]
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
        sections: []
      }
    },
    async joinCourse() {
      this.$router.push(`/enrollment?courseId=${this.courseId}`)
    }
  }
}
</script>

<style scoped>
.course-detail {
  width: 100%;
  font-family: -apple-system, sans-serif;
}

/* --- Header 样式：采用考试中心的绝对定位布局 --- */
.course-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 1.5rem 2rem;
  border-radius: 12px;
  margin-bottom: 2rem;
  position: relative; /* 必须设置，供返回按钮定位 */
  overflow: hidden;
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.25);
}

/* 返回按钮：绝对定位确保标题不受影响 */
.back-btn {
  position: absolute;
  left: 1.5rem;
  top: 50%;
  transform: translateY(-50%);
  background: rgba(255, 255, 255, 0.2);
  border: none;
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.9rem;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 0.3rem;
  transition: all 0.3s ease;
  z-index: 10;
}

.back-btn:hover {
  background: rgba(255, 255, 255, 0.3);
  transform: translateY(-50%) translateX(-2px);
}

.header-content {
  text-align: center; /* 标题绝对居中 */
}

.header-content h1 {
  margin: 0;
  font-size: 1.6rem;
  font-weight: 700;
}

.header-content p {
  margin: 0.4rem 0 0 0;
  opacity: 0.9;
  font-size: 0.9rem;
}

/* 修饰背景圆圈 */
.header-decoration {
  position: absolute;
  top: 0; right: 0; width: 100px; height: 100%; z-index: 1;
}
.decoration-circle {
  position: absolute;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.1);
}
.circle-1 { width: 40px; height: 40px; top: -10px; right: 10px; }
.circle-2 { width: 60px; height: 60px; bottom: -20px; right: 40px; }

/* --- 简介与侧边栏 --- */
.course-intro {
  display: grid;
  grid-template-columns: 1fr 300px;
  gap: 2rem;
}

.intro-content {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05);
}

.intro-section h2 {
  color: #2c3e50;
  margin-bottom: 1.2rem;
}

.intro-sidebar {
  height: fit-content;
  position: sticky;
  top: 20px;
}

.info-card {
  background: white;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
}

.info-item {
  display: flex;
  justify-content: space-between;
  padding: 0.8rem 0;
  border-bottom: 1px solid #f8f9fa;
  color: #606266;
  font-size: 0.95rem;
}

.info-item strong {
  color: #764ba2;
}

/* 按钮动画 */
.enroll-btn {
  width: 100%;
  padding: 0.9rem;
  margin-top: 1.5rem;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  font-weight: 600;
  transition: all 0.3s ease;
}

.enroll-btn:hover {
  filter: brightness(1.1);
  transform: translateY(-2px);
}

/* 课程大纲板块 */
.course-outline-section {
  margin-top: 2.5rem;
}

.outline-container {
  background: white;
  padding: 2.5rem;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05);
}

.section-item {
  padding: 1.5rem;
  border: 1px solid #ebeef5;
  border-radius: 10px;
  margin-bottom: 1.5rem;
  transition: all 0.3s ease;
}

.section-item:hover {
  box-shadow: 0 8px 24px rgba(102, 126, 234, 0.12);
  transform: translateY(-4px);
}

.lesson-item {
  padding: 0.8rem;
  border-radius: 6px;
  display: flex;
  align-items: center;
  gap: 10px;
  color: #606266;
  /* 应用你提供的 transition 简写属性 */
  transition: background 0.2s ease;
}

.lesson-item:hover {
  background-color: #f5f7fa;
  color: #667eea;
}

@media (max-width: 768px) {
  .course-intro { grid-template-columns: 1fr; }
  .back-btn { position: static; transform: none; margin-bottom: 1rem; width: fit-content; }
}
</style>