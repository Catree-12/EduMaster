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

                <div class="course-teacher">

                  <i class="el-icon-user"></i>

                  {{ course.teacher }}

                </div>

                <div class="course-stats">

                  <span class="enrollments">

                    <i class="el-icon-user"></i>

                    {{ course.enrollments }}人报名

                  </span>

                  <span class="rating">

                    <i class="el-icon-star-on"></i>

                    {{ course.rating }}

                  </span>

                </div>

                <div class="course-footer">

                  <div class="price" :class="{ free: course.price === 0 }">

                    {{ course.price === 0 ? '免费' : `¥${course.price}` }}

                  </div>

                  <el-button type="primary" size="small" @click="viewCourse(course.id)">

                    查看详情

                  </el-button>

                </div>

              </div>

            </div>

          </div>

        </section>



        <!-- 课程列表 -->

        <section class="courses-list-section">

          <div class="section-header">

            <h2>全部课程</h2>

            <div class="result-count">共 {{ totalCourses }} 门课程</div>

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

                <div class="course-teacher">

                  <i class="el-icon-user"></i>

                  授课讲师:{{ course.teacher }}

                </div>

                <div class="course-meta">

                  <span class="enrollments">

                    <i class="el-icon-user"></i>

                    {{ course.enrollments }}人报名

                  </span>

                  <span class="rating">

                    <i class="el-icon-star-on"></i>

                    {{ course.rating }}

                  </span>

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

          <div v-if="filteredCourses.length > 0" class="pagination-wrapper">

            <el-pagination

              @current-change="handlePageChange"

              :current-page="currentPage"

              :page-size="pageSize"

              :total="filteredCourses.length"

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

export default {

  name: 'CourseCenterPage',

  data() {

    return {

      categoryOptions: [

        { label: '全部', value: 'all' },

        { label: '计算机', value: '计算机' },

        { label: '经济学', value: '经济学' },

        { label: '农林园艺', value: '农林园艺' },

        { label: '医药卫生', value: '医药卫生' },

        { label: '理学', value: '理学' },

        { label: '历史', value: '历史' },

        { label: '哲学', value: '哲学' },

        { label: '法学', value: '法学' },

        { label: '文学文化', value: '文学文化' },

        { label: '艺术设计', value: '艺术设计' },

        { label: '外语', value: '外语' },

        { label: '教育教学', value: '教育教学' },

        { label: '管理学', value: '管理学' },

        { label: '工学', value: '工学' }

      ],

      searchQuery: '',

      filters: {

        category: 'all',

        level: 'all',

        priceType: 'all'

      },

      currentPage: 1,

      pageSize: 12,

      // 推荐课程（协同过滤结果）

      recommendedCourses: [

        {

          id: 101,

          name: 'Vue.js 3.0 全家桶开发实战',

          teacher: '张三',

          rating: 4.9,

          price: 199,

          enrollments: 15680,

          cover: 'https://via.placeholder.com/300x180/667eea/ffffff?text=Vue.js'

        },

        {

          id: 102,

          name: 'Python 数据分析与可视化',

          teacher: '李四',

          rating: 4.8,

          price: 0,

          enrollments: 12340,

          cover: 'https://via.placeholder.com/300x180/f093fb/ffffff?text=Python'

        },

        {

          id: 103,

          name: 'React 现代化前端开发',

          teacher: '王五',

          rating: 4.7,

          price: 299,

          enrollments: 9850,

          cover: 'https://via.placeholder.com/300x180/4facfe/ffffff?text=React'

        },

        {

          id: 104,

          name: 'Node.js 后端开发进阶',

          teacher: '赵六',

          rating: 4.8,

          price: 249,

          enrollments: 8920,

          cover: 'https://via.placeholder.com/300x180/43e97b/ffffff?text=Node.js'

        }

      ],

      // 全部课程列表

      allCourses: [

        // 前端开发

        { id: 1, name: 'Vue.js 从入门到精通', teacher: '张三', category: '前端开发', level: '初级', rating: 4.8, price: 199, enrollments: 15680, isHot: true, cover: 'https://via.placeholder.com/300x200/667eea/ffffff?text=Vue' },

        { id: 2, name: 'React 现代化前端开发', teacher: '李四', category: '前端开发', level: '中级', rating: 4.7, price: 299, enrollments: 12340, isNew: true, cover: 'https://via.placeholder.com/300x200/61dafb/ffffff?text=React' },

        { id: 3, name: 'Angular 企业级应用开发', teacher: '王五', category: '前端开发', level: '高级', rating: 4.6, price: 399, enrollments: 8920, cover: 'https://via.placeholder.com/300x200/dd0031/ffffff?text=Angular' },

        { id: 4, name: 'TypeScript 完全指南', teacher: '赵六', category: '前端开发', level: '中级', rating: 4.9, price: 0, enrollments: 18750, isHot: true, cover: 'https://via.placeholder.com/300x200/3178c6/ffffff?text=TS' },

        { id: 5, name: 'Webpack 前端工程化', teacher: '孙七', category: '前端开发', level: '高级', rating: 4.5, price: 249, enrollments: 6540, cover: 'https://via.placeholder.com/300x200/8dd6f9/ffffff?text=Webpack' },

       

        // 后端开发

        { id: 6, name: 'Node.js 后端开发实战', teacher: '周八', category: '后端开发', level: '初级', rating: 4.8, price: 249, enrollments: 14230, isHot: true, cover: 'https://via.placeholder.com/300x200/43e97b/ffffff?text=Node' },

        { id: 7, name: 'Java Spring Boot 微服务', teacher: '吴九', category: '后端开发', level: '高级', rating: 4.9, price: 499, enrollments: 16890, isNew: true, cover: 'https://via.placeholder.com/300x200/6db33f/ffffff?text=Spring' },

        { id: 8, name: 'Python Django 全栈开发', teacher: '郑十', category: '后端开发', level: '中级', rating: 4.7, price: 0, enrollments: 11450, cover: 'https://via.placeholder.com/300x200/092e20/ffffff?text=Django' },

        { id: 9, name: 'Go 语言高并发编程', teacher: '陈一', category: '后端开发', level: '中级', rating: 4.6, price: 299, enrollments: 9320, cover: 'https://via.placeholder.com/300x200/00add8/ffffff?text=Go' },

       

        // 移动开发

        { id: 10, name: 'Flutter 跨平台开发', teacher: '刘二', category: '移动开发', level: '初级', rating: 4.8, price: 0, enrollments: 13670, isHot: true, cover: 'https://via.placeholder.com/300x200/02569b/ffffff?text=Flutter' },

        { id: 11, name: 'React Native 移动应用开发', teacher: '林三', category: '移动开发', level: '中级', rating: 4.7, price: 349, enrollments: 10240, cover: 'https://via.placeholder.com/300x200/61dafb/ffffff?text=RN' },

        { id: 12, name: 'Android Kotlin 开发', teacher: '黄四', category: '移动开发', level: '初级', rating: 4.6, price: 399, enrollments: 8930, isNew: true, cover: 'https://via.placeholder.com/300x200/0095d5/ffffff?text=Kotlin' },

       

        // 数据科学

        { id: 13, name: 'Python 数据分析与可视化', teacher: '何五', category: '数据科学', level: '初级', rating: 4.9, price: 0, enrollments: 19560, isHot: true, cover: 'https://via.placeholder.com/300x200/f093fb/ffffff?text=Data' },

        { id: 14, name: 'SQL 数据库查询优化', teacher: '梁六', category: '数据科学', level: '中级', rating: 4.7, price: 199, enrollments: 12340, cover: 'https://via.placeholder.com/300x200/00758f/ffffff?text=SQL' },

        { id: 15, name: 'Tableau 商业智能分析', teacher: '冯七', category: '数据科学', level: '初级', rating: 4.5, price: 299, enrollments: 7860, cover: 'https://via.placeholder.com/300x200/e97627/ffffff?text=Tableau' },

       

        // 人工智能

        { id: 16, name: '机器学习算法精讲', teacher: '许八', category: '人工智能', level: '高级', rating: 4.9, price: 599, enrollments: 15420, isNew: true, cover: 'https://via.placeholder.com/300x200/a8edea/ffffff?text=ML' },

        { id: 17, name: '深度学习与神经网络', teacher: '邓九', category: '人工智能', level: '高级', rating: 4.8, price: 699, enrollments: 11230, isHot: true, cover: 'https://via.placeholder.com/300x200/fed6e3/ffffff?text=DL' },

        { id: 18, name: 'PyTorch 实战项目', teacher: '潘十', category: '人工智能', level: '中级', rating: 4.7, price: 0, enrollments: 9840, cover: 'https://via.placeholder.com/300x200/ee4c2c/ffffff?text=PyTorch' }

      ]

    }

  },

  computed: {

    filteredCourses() {

      let courses = [...this.allCourses]

     

      // 搜索过滤

      if (this.searchQuery) {

        courses = courses.filter(course =>

          course.name.toLowerCase().includes(this.searchQuery.toLowerCase()) ||

          course.teacher.toLowerCase().includes(this.searchQuery.toLowerCase())

        )

      }

     

      // 分类过滤

      if (this.filters.category !== 'all') {

        courses = courses.filter(course => course.category === this.filters.category)

      }

     

      // 难度过滤

      if (this.filters.level !== 'all') {

        courses = courses.filter(course => course.level === this.filters.level)

      }

     

      // 价格类型过滤

      if (this.filters.priceType === 'free') {

        courses = courses.filter(course => course.price === 0)

      } else if (this.filters.priceType === 'paid') {

        courses = courses.filter(course => course.price > 0)

      }

     

      return courses

    },

    totalCourses() {

      return this.filteredCourses.length

    },

    paginatedCourses() {

      const start = (this.currentPage - 1) * this.pageSize

      const end = start + this.pageSize

      return this.filteredCourses.slice(start, end)

    }

  },

  methods: {

    selectCategory(value) {

      this.filters.category = value

      this.handleFilter()

    },

    handleSearch() {

      this.currentPage = 1

    },

    handleFilter() {

      this.currentPage = 1

    },

    handlePageChange(page) {

      this.currentPage = page

      // 滚动到课程列表顶部

      document.querySelector('.courses-list-section').scrollIntoView({ behavior: 'smooth' })

    },

    resetFilters() {

      this.searchQuery = ''

      this.filters = {

        category: 'all',

        level: 'all',

        priceType: 'all'

      }

      this.currentPage = 1

    },

    viewCourse(id) {
      this.$router.push(`/courses/${id}`)
    },

    getLevelTagType(level) {

      const types = {

        '初级': 'success',

        '中级': 'warning',

        '高级': 'danger'

      }

      return types[level] || 'info'

    }

  }

}

</script>



<style scoped lang="scss">

.course-center {

  background: #f8f9fb;

  min-height: 100vh;

}



// 搜索区域

.search-section {

  position: sticky;

  top: 64px;

  z-index: 100;

  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);

  padding: 1.2rem 8%;

  color: white;

  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);



  .search-container {

    max-width: 1400px;

    margin: 0 auto;



    .search-bar {

      ::v-deep .el-input__inner {

        height: 45px;

        font-size: 0.95rem;

        border-radius: 22px;

      }

    }

  }

}



// 主内容布局

.content-layout {

  display: flex;

  max-width: 1400px;

  margin: 0 auto;

  padding: 2rem 8%;

  gap: 2rem;

  align-items: flex-start;

}



// 左侧筛选栏

.filter-sidebar {

  width: 240px;

  flex-shrink: 0;

  position: sticky;

  top: 130px;

  background: white;

  padding: 1.5rem;

  border-radius: 10px;

  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);



  .filter-section {

    margin-bottom: 1.5rem;



    &:last-of-type {

      margin-bottom: 0;

    }



    h3 {

      font-size: 0.9rem;

      color: #2c3e50;

      margin-bottom: 0.75rem;

      font-weight: 600;

    }



    ::v-deep .el-radio-group {

      display: flex;

      flex-direction: column;

      gap: 0.5rem;



      .el-radio {

        margin: 0;

        white-space: nowrap;



        .el-radio__label {

          font-size: 0.85rem;

          padding-left: 0.5rem;

        }

      }

    }

  }

}



// 右侧课程区域

.courses-main {

  flex: 1;

  min-width: 0;

}



// 推荐区域

.recommendation-section {

  background: white;

  padding: 1.5rem;

  border-radius: 10px;

  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);

  margin-bottom: 2rem;



  .recommendation-header {

    text-align: center;

    margin-bottom: 1.5rem;



    h2 {

      font-size: 1.75rem;

      color: #2c3e50;

      margin-bottom: 0.4rem;

    }



    p {

      color: #7f8c8d;

      font-size: 0.9rem;

    }

  }



  .recommendation-grid {

    display: grid;

    grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));

    gap: 1.5rem;

  }



  .recommend-card {

    position: relative;

    background: white;

    border-radius: 10px;

    overflow: hidden;

    box-shadow: 0 3px 10px rgba(102, 126, 234, 0.15);

    border: 2px solid #667eea;

    transition: all 0.3s;



    &:hover {

      transform: translateY(-5px);

      box-shadow: 0 6px 18px rgba(102, 126, 234, 0.25);

    }



    .recommend-badge {

      position: absolute;

      top: 10px;

      left: 10px;

      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);

      color: white;

      padding: 0.2rem 0.6rem;

      border-radius: 15px;

      font-size: 0.7rem;

      font-weight: 600;

      z-index: 1;

    }



    .course-cover {

      height: 150px;

      overflow: hidden;



      img {

        width: 100%;

        height: 100%;

        object-fit: cover;

      }

    }



    .course-info {

      padding: 1rem;



      h3 {

        font-size: 0.95rem;

        margin-bottom: 0.6rem;

        color: #2c3e50;

        overflow: hidden;

        text-overflow: ellipsis;

        display: -webkit-box;

        -webkit-line-clamp: 2;

        -webkit-box-orient: vertical;

        min-height: 2.4em;

      }



      .course-teacher {

        font-size: 0.8rem;

        color: #7f8c8d;

        margin-bottom: 0.6rem;

        display: flex;

        align-items: center;

        gap: 0.25rem;

      }



      .course-stats {

        display: flex;

        justify-content: space-between;

        margin-bottom: 0.8rem;

        font-size: 0.8rem;



        .enrollments {

          color: #3498db;

        }



        .rating {

          color: #f39c12;

          font-weight: 600;

        }

      }



      .course-footer {

        display: flex;

        justify-content: space-between;

        align-items: center;



        .price {

          font-size: 1.1rem;

          font-weight: 700;

          color: #e74c3c;



          &.free {

            color: #27ae60;

          }

        }

      }

    }

  }

}



// 课程列表区域

.courses-list-section {

  background: white;

  padding: 1.5rem;

  border-radius: 10px;

  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);



  .section-header {

    display: flex;

    justify-content: space-between;

    align-items: center;

    margin-bottom: 1.5rem;



    h2 {

      font-size: 1.4rem;

      color: #2c3e50;

    }



    .result-count {

      color: #7f8c8d;

      font-size: 0.85rem;

    }

  }



  .course-grid {

    display: grid;

    grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));

    gap: 1.5rem;

    margin-bottom: 2rem;

  }



  .course-card {

    background: white;

    border-radius: 10px;

    overflow: hidden;

    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);

    transition: all 0.3s;



    &:hover {

      transform: translateY(-5px);

      box-shadow: 0 6px 16px rgba(0, 0, 0, 0.12);

    }



    .course-cover {

      position: relative;

      height: 160px;

      overflow: hidden;



      img {

        width: 100%;

        height: 100%;

        object-fit: cover;

      }



      .new-badge,

      .hot-badge {

        position: absolute;

        top: 10px;

        right: 10px;

        padding: 0.2rem 0.6rem;

        border-radius: 15px;

        font-size: 0.7rem;

        font-weight: 600;

        color: white;

      }



      .new-badge {

        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);

      }



      .hot-badge {

        background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);

      }

    }



    .course-body {

      padding: 1rem;



      h3 {

        font-size: 0.95rem;

        margin-bottom: 0.6rem;

        color: #2c3e50;

        overflow: hidden;

        text-overflow: ellipsis;

        display: -webkit-box;

        -webkit-line-clamp: 2;

        -webkit-box-orient: vertical;

        min-height: 2.4em;

      }



      .course-teacher {

        font-size: 0.8rem;

        color: #7f8c8d;

        margin-bottom: 0.6rem;

        display: flex;

        align-items: center;

        gap: 0.25rem;

      }



      .course-meta {

        display: flex;

        gap: 1rem;

        margin-bottom: 0.6rem;

        font-size: 0.8rem;



        .enrollments {

          color: #3498db;

        }



        .rating {

          color: #f39c12;

          font-weight: 600;

        }

      }



      .course-tags {

        margin-bottom: 0.8rem;

        display: flex;

        gap: 0.5rem;

      }



      .course-footer {

        display: flex;

        justify-content: space-between;

        align-items: center;



        .price-tag {

          font-size: 1.1rem;

          font-weight: 700;

          color: #e74c3c;



          &.free {

            color: #27ae60;

          }

        }

      }

    }

  }



  .no-result {

    text-align: center;

    padding: 3rem 2rem;



    i {

      font-size: 3rem;

      color: #dcdfe6;

      margin-bottom: 1rem;

    }



    p {

      font-size: 1rem;

      color: #7f8c8d;

      margin-bottom: 1.5rem;

    }

  }



  .pagination-wrapper {

    display: flex;

    justify-content: center;

    margin-top: 2rem;

  }

}



// 响应式设计

@media (max-width: 1200px) {

  .recommendation-grid {

    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)) !important;

  }

}



@media (max-width: 768px) {

  .content-layout {

    flex-direction: column;

  }



  .filter-sidebar {

    width: 100%;

    position: static;

  }

}

</style>