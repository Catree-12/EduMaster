<template>
  <div class="course-center">
     <!-- 顶部搜索 -->
    <section class="search-section">
      <div class="search-container">
        <div class="search-bar">
          <el-input
            v-model="searchQuery"
            placeholder="搜索你感兴趣的课程..."
            prefix-icon="el-icon-search"
            size="large"
            @input="handleSearch"
            clearable
          ></el-input>
        </div>
      </div>
    </section>
       <!-- 主内容区域 -->

    <div class="content-layout">

        <!-- 左侧筛选栏 -->

      <aside class="filter-sidebar">
        <div class="filter-section">
          <h3>课程方向</h3>
          <el-radio-group v-model="filters.category" size="small" @change="handleFilter">
            <el-radio v-for="cat in categoryOptions" :key="cat.value" :label="cat.value">
              {{ cat.label }}
            </el-radio>
          </el-radio-group>
        </div>

         
        <div class="filter-section">
          <h3>难度等级</h3>
          <el-radio-group v-model="filters.level" size="small" @change="handleFilter">
            <el-radio label="all">全部</el-radio>
            <el-radio label="初级">初级</el-radio>
            <el-radio label="中级">中级</el-radio>
            <el-radio label="高级">高级</el-radio>
          </el-radio-group>
        </div>

        <div class="filter-section">
          <h3>价格类型</h3>
          <el-radio-group v-model="filters.priceType" size="small" @change="handleFilter">
            <el-radio label="all">全部</el-radio>
            <el-radio label="free">免费</el-radio>
            <el-radio label="paid">付费</el-radio>
          </el-radio-group>
        </div>

        <el-button type="primary" size="small" @click="resetFilters" style="width: 100%; margin-top: 1rem;">
          重置筛选
        </el-button>
      </aside>

         <!-- 右侧课程列表 -->

      <main class="courses-main">

         <!-- 个性化推荐位 -->
        <section class="recommendation-section">
          <div class="recommendation-header">
            <h2>🎯 猜你喜欢</h2>
            <p>基于协同过滤算法，为你精准推荐</p>
          </div>
          <div class="recommendation-grid">
            <div v-for="course in recommendedCourses" :key="course.id" class="recommend-card">
              <div class="recommend-badge">为你推荐</div>
              <div class="course-cover">
                <img :src="course.cover" :alt="course.name">
              </div>
              <div class="course-info">
                <h3>{{ course.name }}</h3>
                <div class="course-teacher"><i class="el-icon-user"></i> {{ course.teacher }}</div>
                <div class="course-stats">
                  <span class="enrollments"><i class="el-icon-user"></i> {{ course.enrollments }}人报名</span>
                  <span class="rating"><i class="el-icon-star-on"></i> {{ course.rating }}</span>
                </div>
                <div class="course-footer">
                  <div class="price" :class="{ free: course.price === 0 }">
                    {{ course.price === 0 ? '免费' : `¥${course.price}` }}
                  </div>
                  <el-button type="primary" size="small" @click="viewCourse(course.id)">查看详情</el-button>
                </div>
              </div>
            </div>
          </div>
        </section>

         <!-- 课程列表 -->

        <section class="courses-list-section">
          <div class="section-header">
            <h2>全部课程</h2>
            <div class="result-count">共 {{ filteredCourses.length }} 门课程</div>
          </div>
          
          <div v-if="paginatedCourses.length > 0" class="course-grid">
            <div v-for="course in paginatedCourses" :key="course.id" class="course-card">
              <div class="course-cover">
                <img :src="course.cover" :alt="course.name">
                <div v-if="course.isNew" class="new-badge">NEW</div>
                <div v-if="course.isHot" class="hot-badge">HOT</div>
              </div>
              <div class="course-body">
                <h3>{{ course.name }}</h3>
                <div class="course-teacher"><i class="el-icon-user"></i> 授课讲师:{{ course.teacher }}</div>
                <div class="course-meta">
                  <span class="enrollments"><i class="el-icon-user"></i> {{ course.enrollments }}人报名</span>
                  <span class="rating"><i class="el-icon-star-on"></i> {{ course.rating }}</span>
                </div>
                <div class="course-tags">
                  <el-tag size="small" type="info">{{ course.category }}</el-tag>
                  <el-tag size="small" :type="getLevelTagType(course.level)">{{ course.level }}</el-tag>
                </div>
                <div class="course-footer">
                  <div class="price-tag" :class="{ free: course.price === 0 }">
                    {{ course.price === 0 ? '免费' : `¥${course.price}` }}
                  </div>
                  <el-button type="primary" size="small" @click="viewCourse(course.id)">
                    查看详情 <i class="el-icon-arrow-right"></i>
                  </el-button>
                </div>
              </div>
            </div>
          </div>

          <div v-else class="no-result">
            <i class="el-icon-search"></i>
            <p>未找到符合条件的课程</p>
            <el-button type="primary" @click="resetFilters">重置筛选</el-button>
          </div>

               <!-- 分页 -->
                
          <div v-if="paginatedCourses.length > 0" class="pagination-wrapper">
            <el-pagination
              @current-change="handlePageChange"
              :current-page="currentPage"
              :page-size="pageSize"
              :total="searchQuery || filters.level !== 'all' || filters.priceType !== 'all' ? filteredCourses.length : totalCourses"
              layout="prev, pager, next, jumper, total"
              background
            ></el-pagination>
          </div>
        </section>
      </main>
    </div>
  </div>
</template>

<script>
import { courseAPI } from '@/api'

export default {
  name: 'CourseCenterPage',
  data() {
    return {
      categoryOptions: [
        { label: '全部', value: 'all' }, { label: '计算机', value: '计算机' },
        { label: '经济学', value: '经济学' }, { label: '农林园艺', value: '农林园艺' },
        { label: '医药卫生', value: '医药卫生' }, { label: '理学', value: '理学' },
        { label: '历史', value: '历史' }, { label: '哲学', value: '哲学' },
        { label: '法学', value: '法学' }, { label: '文学文化', value: '文学文化' },
        { label: '艺术设计', value: '艺术设计' }, { label: '外语', value: '外语' },
        { label: '教育教学', value: '教育教学' }, { label: '管理学', value: '管理学' },
        { label: '工学', value: '工学' }
      ],
      searchQuery: '',
      filters: { category: 'all', level: 'all', priceType: 'all' },
      currentPage: 1,
      pageSize: 12,
      recommendedCourses: [
        { id: 101, name: 'Vue.js 3.0 全家桶开发实战', teacher: '张三', rating: 4.9, price: 199, enrollments: 15680, cover: 'https://via.placeholder.com/300x180/667eea/ffffff?text=Vue.js' },
        { id: 102, name: 'Python 数据分析与可视化', teacher: '李四', rating: 4.8, price: 0, enrollments: 12340, cover: 'https://via.placeholder.com/300x180/f093fb/ffffff?text=Python' },
        { id: 103, name: 'React 现代化前端开发', teacher: '王五', rating: 4.7, price: 299, enrollments: 9850, cover: 'https://via.placeholder.com/300x180/4facfe/ffffff?text=React' },
      ],
      allCourses: [],
      totalCourses: 0,
      totalPages: 0,
      loading: false
    }
  },
  computed: {
    filteredCourses() {
      let courses = [...this.allCourses];
      if (this.searchQuery) {
        const q = this.searchQuery.toLowerCase();
        courses = courses.filter(c => c.name.toLowerCase().includes(q) || c.teacher.toLowerCase().includes(q));
      }
      if (this.filters.level !== 'all') courses = courses.filter(c => c.level === this.filters.level);
      if (this.filters.priceType === 'free') courses = courses.filter(c => c.price === 0);
      else if (this.filters.priceType === 'paid') courses = courses.filter(c => c.price > 0);
      return courses;
    },
    paginatedCourses() {
      if (this.searchQuery || this.filters.level !== 'all' || this.filters.priceType !== 'all') {
        const start = (this.currentPage - 1) * this.pageSize;
        return this.filteredCourses.slice(start, start + this.pageSize);
      }
      return this.allCourses;
    }
  },
  created() { this.loadCourses(); },
  methods: {
    // 辅助方法：将相对路径转换为完整的后端URL
    getFullMediaUrl(relativeUrl) {
      if (!relativeUrl) return 'https://via.placeholder.com/300x200/667eea/ffffff?text=Course'
      if (relativeUrl.startsWith('http')) return relativeUrl
      
      const backendUrl = process.env.VUE_APP_API_URL?.replace('/api', '') || 'http://localhost:8000'
      return `${backendUrl}${relativeUrl}`
    },
    async loadCourses() {
      this.loading = true;
      try {
        const params = { page: this.currentPage, pageSize: this.pageSize };
        if (this.filters.category !== 'all') params.category = this.filters.category;
        const res = await courseAPI.getCourseList(params);
        this.allCourses = res.results.map(c => ({
          id: c.id, name: c.title, teacher: c.teacher.name, category: c.category,
          level: '初级', rating: 4.8, price: c.price, enrollments: c.enrollment_count || 0,
          isHot: c.enrollment_count > 1000,
          isNew: new Date(c.created_at) > new Date(Date.now() - 7 * 86400000),
          cover: this.getFullMediaUrl(c.cover)
        }));
        this.totalCourses = res.count;
        this.totalPages = res.totalPages;
      } catch (e) {
        this.$message.error('加载课程失败');
      } finally { this.loading = false; }
    },
    handleSearch() { this.currentPage = 1; },
    handleFilter() { this.currentPage = 1; this.loadCourses(); },
    handlePageChange(page) {
      this.currentPage = page;
      if (!this.searchQuery && this.filters.level === 'all' && this.filters.priceType === 'all') this.loadCourses();
      document.querySelector('.courses-list-section')?.scrollIntoView({ behavior: 'smooth' });
    },
    resetFilters() {
      this.searchQuery = '';
      this.filters = { category: 'all', level: 'all', priceType: 'all' };
      this.currentPage = 1;
      this.loadCourses();
    },
    viewCourse(id) { this.$router.push(`/courses/${id}`); },
    getLevelTagType(level) {
      return { '初级': 'success', '中级': 'warning', '高级': 'danger' }[level] || 'info';
    }
  }
}
</script>

<style scoped lang="scss">
.course-center { background: #f8f9fb; min-height: 100vh; }
.search-section {
  position: sticky; top: 64px; z-index: 100; padding: 1.2rem 8%; color: white;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  .search-container { max-width: 1400px; margin: 0 auto;
    .search-bar ::v-deep .el-input__inner { height: 45px; border-radius: 22px; }
  }
}
.content-layout { display: flex; max-width: 1400px; margin: 0 auto; padding: 2rem 8%; gap: 2rem; align-items: flex-start; }
.filter-sidebar {
  width: 240px; flex-shrink: 0; position: sticky; top: 130px; background: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  .filter-section { margin-bottom: 1.5rem;
    h3 { font-size: 0.9rem; color: #2c3e50; margin-bottom: 0.75rem; font-weight: 600; }
    ::v-deep .el-radio-group { display: flex; flex-direction: column; gap: 0.5rem;
      .el-radio { margin: 0; .el-radio__label { font-size: 0.85rem; padding-left: 0.5rem; } }
    }
  }
}
.courses-main { flex: 1; min-width: 0; }
.recommendation-section {
  background: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08); margin-bottom: 2rem;
  .recommendation-header { text-align: center; margin-bottom: 1.5rem;
    h2 { font-size: 1.75rem; color: #2c3e50; margin-bottom: 0.4rem; }
    p { color: #7f8c8d; font-size: 0.9rem; }
  }
  .recommendation-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(240px, 1fr)); gap: 1.5rem; }
  .recommend-card {
    position: relative; background: white; border-radius: 10px; overflow: hidden; border: 2px solid #667eea; transition: all 0.3s;
    &:hover { transform: translateY(-5px); box-shadow: 0 6px 18px rgba(102, 126, 234, 0.25); }
    .recommend-badge { position: absolute; top: 10px; left: 10px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 0.2rem 0.6rem; border-radius: 15px; font-size: 0.7rem; z-index: 1; }
    .course-cover { height: 150px; img { width: 100%; height: 100%; object-fit: cover; } }
    .course-info { padding: 1rem;
      h3 { font-size: 0.95rem; margin-bottom: 0.6rem; min-height: 2.4em; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }
      .course-teacher { font-size: 0.8rem; color: #7f8c8d; margin-bottom: 0.6rem; display: flex; align-items: center; gap: 0.25rem; }
      .course-stats { display: flex; justify-content: space-between; margin-bottom: 0.8rem; font-size: 0.8rem; .enrollments { color: #3498db; } .rating { color: #f39c12; } }
      .course-footer { display: flex; justify-content: space-between; align-items: center; .price { font-size: 1.1rem; font-weight: 700; color: #e74c3c; &.free { color: #27ae60; } } }
    }
  }
}
.courses-list-section {
  background: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  .section-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem; h2 { font-size: 1.4rem; color: #2c3e50; } .result-count { color: #7f8c8d; font-size: 0.85rem; } }
  .course-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 1.5rem; margin-bottom: 2rem; }
  .course-card {
    background: white; border-radius: 10px; overflow: hidden; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08); transition: 0.3s;
    &:hover { transform: translateY(-5px); box-shadow: 0 6px 16px rgba(0, 0, 0, 0.12); }
    .course-cover { position: relative; height: 160px; img { width: 100%; height: 100%; object-fit: cover; }
      .new-badge, .hot-badge { position: absolute; top: 10px; right: 10px; padding: 0.2rem 0.6rem; border-radius: 15px; font-size: 0.7rem; color: white; }
      .new-badge { background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); }
      .hot-badge { background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); }
    }
    .course-body { padding: 1rem;
      h3 { font-size: 0.95rem; margin-bottom: 0.6rem; min-height: 2.4em; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }
      .course-teacher { font-size: 0.8rem; color: #7f8c8d; margin-bottom: 0.6rem; display: flex; align-items: center; gap: 0.25rem; }
      .course-meta { display: flex; gap: 1rem; margin-bottom: 0.6rem; font-size: 0.8rem; .enrollments { color: #3498db; } .rating { color: #f39c12; } }
      .course-tags { margin-bottom: 0.8rem; display: flex; gap: 0.5rem; }
      .course-footer { display: flex; justify-content: space-between; align-items: center; .price-tag { font-size: 1.1rem; font-weight: 700; color: #e74c3c; &.free { color: #27ae60; } } }
    }
  }
  .no-result { text-align: center; padding: 3rem 2rem; i { font-size: 3rem; color: #dcdfe6; margin-bottom: 1rem; } p { color: #7f8c8d; margin-bottom: 1.5rem; } }
  .pagination-wrapper { display: flex; justify-content: center; margin-top: 2rem; }
}
@media (max-width: 1200px) { .recommendation-grid { grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)) !important; } }
@media (max-width: 768px) { .content-layout { flex-direction: column; } .filter-sidebar { width: 100%; position: static; } }
</style>