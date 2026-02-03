<!-- CourseCard 课程卡片组件 -->
<template>
  <div class="course-card">
    <div class="course-cover">
      <img :src="course.cover" :alt="course.title" />
    </div>
    <div class="course-info">
      <h3>{{ course.title }}</h3>
      <p class="course-desc">{{ course.description }}</p>
      <div class="course-meta">
        <span class="course-price">¥{{ course.price }}</span>
        <span class="course-students">{{ course.studentCount }} 人学习</span>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'CourseCard',
  props: {
    course: {
      type: Object,
      required: true
    }
  }
}
</script>

<style scoped>
.course-card {
  border: 1px solid #e4e7ed;
  border-radius: 8px;
  overflow: hidden;
  transition: all 0.3s;
  cursor: pointer;
}

.course-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transform: translateY(-4px);
}

.course-cover {
  width: 100%;
  height: 160px;
  overflow: hidden;
}

.course-cover img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.course-info {
  padding: 16px;
}

.course-info h3 {
  font-size: 16px;
  margin: 0 0 8px 0;
  color: #303133;
}

.course-desc {
  font-size: 14px;
  color: #606266;
  margin: 0 0 12px 0;
  line-height: 1.5;
}

.course-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.course-price {
  font-size: 18px;
  font-weight: bold;
  color: #f56c6c;
}

.course-students {
  font-size: 12px;
  color: #909399;
}
</style>
