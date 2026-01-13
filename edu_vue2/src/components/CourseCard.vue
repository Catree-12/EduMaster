<template>
  <div class="course-card">
    <div class="course-image">
      <img :src="course.image" :alt="course.title">
      <span class="badge">{{ course.badge }}</span>
    </div>
    <div class="course-body">
      <h3>{{ course.title }}</h3>
      <p class="instructor">{{ course.instructor }}</p>
      <p class="description">{{ course.description }}</p>
      <div class="course-footer">
        <div class="stats">
          <span>⭐ {{ course.rating }}</span>
          <span>👥 {{ course.students }}</span>
        </div>
        <div class="price">¥{{ course.price }}</div>
      </div>
      <slot name="action">
        <router-link :to="`/course/${course.id}`" class="btn-view">
          查看详情
        </router-link>
      </slot>
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
  background: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: all 0.3s;
}

.course-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
}

.course-image {
  position: relative;
  width: 100%;
  height: 200px;
  overflow: hidden;
}

.course-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.badge {
  position: absolute;
  top: 10px;
  right: 10px;
  background: #667eea;
  color: white;
  padding: 6px 12px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 600;
}

.course-body {
  padding: 20px;
}

.course-body h3 {
  margin: 0 0 8px;
  color: #333;
  font-size: 16px;
}

.instructor {
  color: #999;
  font-size: 12px;
  margin: 0 0 10px;
}

.description {
  color: #666;
  font-size: 13px;
  margin: 0 0 15px;
  line-height: 1.5;
}

.course-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 15px;
  border-top: 1px solid #eee;
  margin-bottom: 15px;
}

.stats {
  display: flex;
  gap: 12px;
  font-size: 12px;
  color: #999;
}

.price {
  font-size: 18px;
  font-weight: 700;
  color: #667eea;
}

.btn-view {
  display: block;
  padding: 10px;
  background: #f0f0f0;
  color: #667eea;
  text-decoration: none;
  text-align: center;
  border-radius: 4px;
  font-weight: 600;
  transition: all 0.3s;
}

.btn-view:hover {
  background: #667eea;
  color: white;
}
</style>
