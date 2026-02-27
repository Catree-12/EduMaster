<template>
  <div class="home">
    <!-- 大气 Banner 轮播图 -->
    <section class="banner-section">
      <el-carousel :interval="5000" height="420px" arrow="always">
        <el-carousel-item v-for="(banner, index) in banners" :key="index">
          <div class="banner-content" :style="{ background: banner.gradient }">
            <div class="banner-text">
              <h1>{{ banner.title }}</h1>
              <p>{{ banner.description }}</p>
              <div class="banner-actions">
                <el-button type="primary" size="large" @click="goToCourseCenter">
                  <i class="el-icon-video-play"></i> 开始学习
                </el-button>
                <el-button type="success" size="large" @click="goToMyCourses">
                  <i class="el-icon-upload2"></i> 发布课程
                </el-button>
              </div>
            </div>
            <div class="banner-illustration">
              <i :class="banner.icon"></i>
            </div>
          </div>
        </el-carousel-item>
      </el-carousel>
    </section>

    <!-- 平台核心数据展示 -->
    <section class="stats-bar">
      <div class="stat-item">
        <div class="stat-icon">👨‍🏫</div>
        <div class="stat-info">
          <div class="stat-number">{{ platformStats.teachers }}+</div>
          <div class="stat-label">入驻讲师</div>
        </div>
      </div>
      <div class="stat-item">
        <div class="stat-icon">📚</div>
        <div class="stat-info">
          <div class="stat-number">{{ platformStats.courses }}+</div>
          <div class="stat-label">累计课程</div>
        </div>
      </div>
      <div class="stat-item">
        <div class="stat-icon">👥</div>
        <div class="stat-info">
          <div class="stat-number">{{ platformStats.students }}+</div>
          <div class="stat-label">注册学员</div>
        </div>
      </div>
      <div class="stat-item">
        <div class="stat-icon">⭐</div>
        <div class="stat-info">
          <div class="stat-number">{{ platformStats.satisfaction }}%</div>
          <div class="stat-label">满意度</div>
        </div>
      </div>
    </section>

    <!-- 智慧功能特色区 -->->
    <section class="popular-courses-section">
      <div class="section-header">
        <h2>🔥 热门课程</h2>
        <p>最受欢迎的课程，万千学员的共同选择</p>
      </div>
      <div class="course-waterfall">
        <div v-for="course in popularCourses" :key="course.id" class="course-item">
          <div class="course-cover">
            <img :src="course.cover" :alt="course.name">
            <div class="enrollment-count">
              <i class="el-icon-user"></i>
              {{ course.enrollments }}人已学
            </div>
          </div>
          <div class="course-content">
            <h4>{{ course.name }}</h4>
            <div class="teacher-info">
              <span>{{ course.teacher }}</span>
            </div>
            <div class="course-bottom">
              <div class="rating">
                <i class="el-icon-star-on"></i>
                {{ course.rating }}
              </div>
              <div class="price" :class="{ free: course.price === 0 }">
                {{ course.price === 0 ? '免费' : `¥${course.price}` }}
              </div>
            </div>
            <el-button type="primary" size="small" class="view-detail-btn" @click="viewCourse(course.id)">
              查看详情
            </el-button>
          </div>
        </div>
      </div>
      <div class="view-more">
        <el-button type="primary" size="medium" @click="goToCourseCenter">
          查看更多课程 <i class="el-icon-arrow-right"></i>
        </el-button>
      </div>
    </section>

    <!-- 页脚 -->
    <footer class="footer">
      <div class="footer-content">
        <div class="footer-section">
          <h3>EduMaster</h3>
          <p>智慧教学平台，让教育更简单</p>
        </div>
        <div class="footer-section">
          <h4>关于我们</h4>
          <ul>
            <li><a href="#">平台介绍</a></li>
            <li><a href="#">联系我们</a></li>
            <li><a href="#">加入我们</a></li>
          </ul>
        </div>
        <div class="footer-section">
          <h4>帮助中心</h4>
          <ul>
            <li><a href="#">使用指南</a></li>
            <li><a href="#">常见问题</a></li>
            <li><a href="#">隐私政策</a></li>
          </ul>
        </div>
        <div class="footer-section">
          <h4>联系方式</h4>
          <ul>
            <li>📧 support@edumaster.com</li>
            <li>📞 400-123-4567</li>
            <li>📍 北京市海淀区中关村大街1号</li>
          </ul>
        </div>
      </div>
      <div class="footer-bottom">
        <p>&copy; 2026 EduMaster. All rights reserved.</p>
      </div>
    </footer>
  </div>
</template>

<script>
import { courseAPI } from '@/api'

export default {
  name: 'HomePage',
  data() {
    return {
      // Banner 数据
      banners: [
        {
          title: '智能组卷，让出题更高效',
          description: 'AI 算法自动生成试卷，支持知识点、难度、题型智能配比',
          gradient: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
          icon: 'el-icon-document'
        },
        {
          title: 'AI 辅助批改，提升教学质量',
          description: '运用自然语言处理技术，智能批改主观题，提供详细批注',
          gradient: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
          icon: 'el-icon-edit-outline'
        },
        {
          title: '个性化推荐，精准匹配课程',
          description: '基于协同过滤算法，为每位学员推荐最适合的学习内容',
          gradient: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
          icon: 'el-icon-magic-stick'
        }
      ],
      // 平台统计数据
      platformStats: {
        teachers: 1580,
        courses: 3200,
        students: 85000,
        satisfaction: 98
      },
      // 热门课程(从后端加载)
      popularCourses: [],
      loading: false
    }
  },
  created() {
    this.loadPopularCourses()
  },
  methods: {
    // 辅助方法：将相对路径转换为完整的后端URL
    getFullMediaUrl(relativeUrl) {
      if (!relativeUrl) return 'https://via.placeholder.com/300x200/667eea/ffffff?text=Course'
      if (relativeUrl.startsWith('http')) return relativeUrl
      
      const backendUrl = process.env.VUE_APP_API_URL?.replace('/api', '') || 'http://localhost:8000'
      return `${backendUrl}${relativeUrl}`
    },
    // 加载热门课程
    async loadPopularCourses() {
      this.loading = true
      try {
        const response = await courseAPI.getCourseList({
          page: 1,
          pageSize: 6
        })
        
        // 处理后端返回数据
        this.popularCourses = response.results.map(course => ({
          id: course.id,
          name: course.title,
          teacher: course.teacher.name,
          rating: 4.8, // 后端暂时没有评分字段,默认值
          price: course.price,
          enrollments: course.enrollment_count || 0,
          cover: this.getFullMediaUrl(course.cover)
        }))
      } catch (error) {
        console.error('加载热门课程失败:', error)
        this.$message.error('加载课程失败')
      } finally {
        this.loading = false
      }
    },
    
    goToCourseCenter() {
      if (this.$route.path !== '/courses') {
        this.$router.push('/courses')
      }
    },
    goToMyCourses() {
      if (this.$route.path !== '/courses/mycourses') {
        this.$router.push('/courses/mycourses')
      }
    },
    viewCourse(id) {
      const target = `/courses/${id}`
      if (this.$route.path !== target) {
        this.$router.push(target)
      }
    }
  }
}
</script>

<style scoped lang="scss">
.home {
  background: #f8f9fb;
}

// Banner 轮播图
.banner-section {
  margin-bottom: 0;

  .banner-content {
    height: 420px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 8%;
    color: white;
  }

  .banner-text {
    flex: 1;
    max-width: 550px;

    h1 {
      font-size: 2.5rem;
      font-weight: 700;
      margin-bottom: 1rem;
      line-height: 1.2;
    }

    p {
      font-size: 1.1rem;
      margin-bottom: 2rem;
      opacity: 0.95;
    }
  }

  .banner-actions {
    display: flex;
    gap: 1rem;

    .el-button {
      padding: 0.8rem 2rem;
      font-size: 0.95rem;
      font-weight: 600;
    }
  }

  .banner-illustration {
    font-size: 12rem;
    opacity: 0.2;
  }
}

// 统计条
.stats-bar {
  display: flex;
  justify-content: space-around;
  padding: 2rem 8%;
  background: white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);

  .stat-item {
    display: flex;
    align-items: center;
    gap: 0.8rem;
  }

  .stat-icon {
    font-size: 2.5rem;
  }

  .stat-number {
    font-size: 1.75rem;
    font-weight: 700;
    color: #667eea;
  }

  .stat-label {
    font-size: 0.85rem;
    color: #666;
  }
}

// 章节通用样式
section {
  padding: 2.5rem 8%;
}

.section-header {
  text-align: center;
  margin-bottom: 2rem;

  h2 {
    font-size: 1.75rem;
    font-weight: 700;
    color: #2c3e50;
    margin-bottom: 0.5rem;
  }

  p {
    font-size: 0.95rem;
    color: #7f8c8d;
  }
}

// 热门课程瀑布流
.popular-courses-section {
  background: white;

  .course-waterfall {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 1.5rem;
  }

  .course-item {
    background: white;
    border-radius: 10px;
    overflow: hidden;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
    transition: all 0.3s;
    cursor: pointer;

    &:hover {
      transform: translateY(-5px);
      box-shadow: 0 6px 16px rgba(0, 0, 0, 0.12);
    }

    .course-cover {
      position: relative;
      height: 170px;
      overflow: hidden;

      img {
        width: 100%;
        height: 100%;
        object-fit: cover;
      }

      .enrollment-count {
        position: absolute;
        bottom: 10px;
        left: 10px;
        background: rgba(0, 0, 0, 0.7);
        color: white;
        padding: 0.2rem 0.6rem;
        border-radius: 15px;
        font-size: 0.7rem;
        display: flex;
        align-items: center;
        gap: 0.25rem;
      }
    }

    .course-content {
      padding: 1rem;

      h4 {
        font-size: 0.95rem;
        margin-bottom: 0.5rem;
        color: #2c3e50;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
      }

      .teacher-info {
        font-size: 0.8rem;
        color: #7f8c8d;
        margin-bottom: 0.6rem;
      }

      .course-bottom {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.75rem;

        .rating {
          display: flex;
          align-items: center;
          gap: 0.25rem;
          color: #f39c12;
          font-weight: 600;
          font-size: 0.9rem;
        }

        .price {
          font-size: 1rem;
          font-weight: 700;
          color: #e74c3c;

          &.free {
            color: #27ae60;
          }
        }
      }

      .view-detail-btn {
        width: 100%;
      }
    }
  }

  .view-more {
    text-align: center;
    margin-top: 2rem;
  }
}

// 页脚
.footer {
  background: #2c3e50;
  color: white;
  padding: 2rem 8% 1rem;

  .footer-content {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1.5rem;
    margin-bottom: 1.5rem;
  }

  .footer-section {
    h3, h4 {
      margin-bottom: 0.75rem;
      color: white;
      font-size: 1rem;
    }

    p {
      color: rgba(255, 255, 255, 0.7);
      line-height: 1.6;
      font-size: 0.85rem;
    }

    ul {
      list-style: none;
      padding: 0;

      li {
        margin-bottom: 0.4rem;
        font-size: 0.85rem;

        a {
          color: rgba(255, 255, 255, 0.7);
          text-decoration: none;
          transition: color 0.3s;

          &:hover {
            color: white;
          }
        }
      }
    }
  }

  .footer-bottom {
    text-align: center;
    padding-top: 1.5rem;
    border-top: 1px solid rgba(255, 255, 255, 0.1);

    p {
      color: rgba(255, 255, 255, 0.5);
      font-size: 0.8rem;
    }
  }
}

// 响应式设计
@media (max-width: 1200px) {
  .features-grid {
    grid-template-columns: repeat(2, 1fr) !important;
  }
}

@media (max-width: 768px) {
  .banner-text h1 {
    font-size: 2rem !important;
  }

  .stats-bar {
    flex-wrap: wrap;
    gap: 2rem;
  }

  .features-grid {
    grid-template-columns: 1fr !important;
  }

  .footer-content {
    grid-template-columns: repeat(2, 1fr) !important;
  }
}
</style>
