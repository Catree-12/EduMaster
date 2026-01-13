<template>
  <div class="course-center">
    <div class="course-header">
      <h1>课程中心</h1>
      <div class="search-bar">
        <input 
          v-model="searchQuery" 
          type="text" 
          placeholder="搜索课程..."
          @input="handleSearch"
        >
      </div>
    </div>

    <div class="course-layout">
      <!-- 侧边栏：筛选 -->
      <aside class="filter-sidebar">
        <h3>分类筛选</h3>
        <div class="filter-group">
          <label>
            <input 
              type="checkbox" 
              value="all"
              v-model="filters.category"
            >
            全部分类
          </label>
        </div>
        <div class="filter-group">
          <label v-for="cat in categories" :key="cat">
            <input 
              type="checkbox" 
              :value="cat"
              v-model="filters.category"
            >
            {{ cat }}
          </label>
        </div>

        <h3 style="margin-top: 2rem;">难度等级</h3>
        <div class="filter-group">
          <label v-for="level in levels" :key="level">
            <input 
              type="checkbox" 
              :value="level"
              v-model="filters.level"
            >
            {{ level }}
          </label>
        </div>

        <button @click="resetFilters" class="reset-btn">重置筛选</button>
      </aside>

      <!-- 主内容：课程列表 -->
      <main class="course-main">
        <div v-if="filteredCourses.length > 0" class="course-grid">
          <div v-for="course in filteredCourses" :key="course.id" class="course-card">
            <div class="course-image">{{ course.category[0] }}</div>
            <div class="course-content">
              <h3>{{ course.name }}</h3>
              <p class="instructor">👨‍🏫 {{ course.instructor }}</p>
              <p class="description">{{ course.description }}</p>
              <div class="course-footer">
                <span class="category">{{ course.category }}</span>
                <span class="level">{{ course.level }}</span>
              </div>
              <div class="course-meta">
                <span>👥 {{ course.studentCount }}</span>
                <span>⭐ {{ course.rating }}</span>
              </div>
              <router-link :to="`/course/${course.id}`" class="course-btn">查看详情</router-link>
            </div>
          </div>
        </div>
        <div v-else class="no-courses">
          <p>未找到符合条件的课程</p>
        </div>
      </main>
    </div>
  </div>
</template>

<script>
export default {
  name: 'CourseCenter',
  data() {
    return {
      searchQuery: '',
      filters: {
        category: ['all'],
        level: []
      },
      categories: ['前端开发', '后端开发', '数据科学', '移动开发', '人工智能'],
      levels: ['初级', '中级', '高级'],
      courses: [
        {
          id: 1,
          name: 'Vue.js 从入门到精通',
          instructor: '张三',
          description: '学习现代化前端框架Vue.js的开发技能',
          category: '前端开发',
          level: '初级',
          studentCount: 1250,
          rating: 4.8
        },
        {
          id: 2,
          name: 'Python 数据科学',
          instructor: '李四',
          description: '掌握数据分析和机器学习的基础知识',
          category: '数据科学',
          level: '中级',
          studentCount: 980,
          rating: 4.7
        },
        {
          id: 3,
          name: 'Web 全栈开发',
          instructor: '王五',
          description: '前后端完整的Web开发课程',
          category: '后端开发',
          level: '高级',
          studentCount: 750,
          rating: 4.9
        },
        // ...更多课程
      ]
    }
  },
  computed: {
    filteredCourses() {
      return this.courses.filter(course => {
        const matchSearch = course.name.includes(this.searchQuery) || 
                           course.instructor.includes(this.searchQuery)
        const matchCategory = this.filters.category.includes('all') || 
                             this.filters.category.includes(course.category)
        const matchLevel = this.filters.level.length === 0 || 
                          this.filters.level.includes(course.level)
        return matchSearch && matchCategory && matchLevel
      })
    }
  },
  methods: {
    handleSearch() {
      // 搜索功能已在计算属性中实现
    },
    resetFilters() {
      this.searchQuery = ''
      this.filters.category = ['all']
      this.filters.level = []
    }
  }
}
</script>

<style scoped>
.course-center {
  width: 100%;
}

.course-header {
  margin-bottom: 2rem;
}

.course-header h1 {
  margin: 0 0 1rem 0;
  color: #2c3e50;
}

.search-bar {
  margin-bottom: 1.5rem;
}

.search-bar input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #bdc3c7;
  border-radius: 4px;
  font-size: 1rem;
  box-sizing: border-box;
}

.search-bar input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.course-layout {
  display: grid;
  grid-template-columns: 200px 1fr;
  gap: 2rem;
}

.filter-sidebar {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  height: fit-content;
  position: sticky;
  top: 100px;
}

.filter-sidebar h3 {
  margin: 0 0 1rem 0;
  color: #2c3e50;
  font-size: 1rem;
}

.filter-group {
  margin-bottom: 1rem;
}

.filter-group label {
  display: flex;
  align-items: center;
  cursor: pointer;
  margin-bottom: 0.5rem;
  color: #7f8c8d;
}

.filter-group input {
  margin-right: 0.5rem;
}

.reset-btn {
  width: 100%;
  padding: 0.5rem;
  background-color: #e74c3c;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.reset-btn:hover {
  background-color: #c0392b;
}

.course-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 1.5rem;
}

.course-card {
  background: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s, box-shadow 0.3s;
  display: flex;
  flex-direction: column;
}

.course-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
}

.course-image {
  height: 150px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2.5rem;
  font-weight: bold;
}

.course-content {
  padding: 1rem;
  flex: 1;
  display: flex;
  flex-direction: column;
}

.course-card h3 {
  margin: 0 0 0.5rem 0;
  color: #2c3e50;
  font-size: 1.1rem;
}

.course-card .instructor {
  margin: 0 0 0.5rem 0;
  color: #7f8c8d;
  font-size: 0.875rem;
}

.course-card .description {
  margin: 0 0 1rem 0;
  color: #95a5a6;
  font-size: 0.875rem;
  flex: 1;
}

.course-footer {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
}

.course-footer span {
  font-size: 0.75rem;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
}

.category {
  background-color: #ecf0f1;
  color: #2c3e50;
}

.level {
  background-color: #e8daef;
  color: #8e44ad;
}

.course-meta {
  display: flex;
  justify-content: space-between;
  font-size: 0.875rem;
  color: #7f8c8d;
  margin-bottom: 1rem;
}

.course-btn {
  display: block;
  padding: 0.6rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  text-decoration: none;
  text-align: center;
  border-radius: 4px;
  transition: opacity 0.3s;
}

.course-btn:hover {
  opacity: 0.9;
}

.no-courses {
  text-align: center;
  padding: 3rem;
  color: #7f8c8d;
}

@media (max-width: 768px) {
  .course-layout {
    grid-template-columns: 1fr;
  }

  .filter-sidebar {
    position: static;
  }
}
</style>
