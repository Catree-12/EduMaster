<template>
  <div class="home">
    <!-- 英雄横幅 -->
    <section class="hero-banner">
      <div class="hero-content">
        <h1>欢迎来到 EduMaster</h1>
        <p>专业在线教育平台，汇聚优质课程与讲师</p>
        <div class="hero-actions">
          <router-link to="/course" class="cta-btn primary">浏览全部课程</router-link>
          <router-link to="/register" class="cta-btn secondary">立即注册</router-link>
        </div>
      </div>
      <div class="hero-illustration">
        <div class="illustration-item">📚</div>
      </div>
    </section>

    <!-- 特色课程 -->
    <section class="featured-section">
      <div class="section-header">
        <h2>热门课程推荐</h2>
        <p>精选优质课程，助力你的学习之旅</p>
      </div>
      
      <div class="course-grid">
        <div v-for="course in featuredCourses" :key="course.id" class="course-card">
          <div class="course-image">
            <span class="course-icon">{{ getCourseIcon(course.category) }}</span>
            <div class="course-badge">{{ course.category }}</div>
          </div>
          <div class="course-body">
            <h3>{{ course.name }}</h3>
            <p class="instructor">👨‍🏫 {{ course.instructor }}</p>
            <p class="description">{{ course.description }}</p>
            
            <div class="course-stats">
              <span class="stat">
                <span class="icon">👥</span>
                <span>{{ course.studentCount }}</span>
              </span>
              <span class="stat">
                <span class="icon">⭐</span>
                <span>{{ course.rating }}</span>
              </span>
            </div>
            
            <router-link :to="`/course/${course.id}`" class="view-btn">
              查看课程 →
            </router-link>
          </div>
        </div>
      </div>

      <div class="view-all">
        <router-link to="/course" class="view-all-btn">查看更多课程 →</router-link>
      </div>
    </section>

    <!-- 统计信息 -->
    <section class="stats-section">
      <div class="section-header">
        <h2>EduMaster 成绩</h2>
        <p>数字说话，见证我们的成长</p>
      </div>

      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-number">{{ totalCourses }}+</div>
          <div class="stat-label">优质课程</div>
          <div class="stat-description">覆盖多个领域</div>
        </div>
        <div class="stat-card">
          <div class="stat-number">{{ totalUsers }}+</div>
          <div class="stat-label">活跃学生</div>
          <div class="stat-description">全球学习者</div>
        </div>
        <div class="stat-card">
          <div class="stat-number">{{ totalLessons }}+</div>
          <div class="stat-label">优质课程</div>
          <div class="stat-description">专业教师讲授</div>
        </div>
        <div class="stat-card">
          <div class="stat-number">98%</div>
          <div class="stat-label">用户满意度</div>
          <div class="stat-description">获得高度认可</div>
        </div>
      </div>
    </section>

    <!-- 优势特性 -->
    <section class="features-section">
      <div class="section-header">
        <h2>为什么选择 EduMaster</h2>
        <p>提供最优质的在线教育服务</p>
      </div>

      <div class="features-grid">
        <div class="feature-card">
          <div class="feature-icon">🎯</div>
          <h3>针对性学习</h3>
          <p>个性化学习路径，根据你的进度调整内容</p>
        </div>
        <div class="feature-card">
          <div class="feature-icon">👨‍🏫</div>
          <h3>专业讲师</h3>
          <p>汇聚业界精英讲师，提供高质量教学</p>
        </div>
        <div class="feature-card">
          <div class="feature-icon">💻</div>
          <h3>灵活学习</h3>
          <p>随时随地学习，不受时间和地点限制</p>
        </div>
        <div class="feature-card">
          <div class="feature-icon">🏆</div>
          <h3>认证证书</h3>
          <p>完成课程获得认证，提升职业竞争力</p>
        </div>
        <div class="feature-card">
          <div class="feature-icon">💬</div>
          <h3>互动社区</h3>
          <p>与其他学习者交流分享，共同进步</p>
        </div>
        <div class="feature-card">
          <div class="feature-icon">🚀</div>
          <h3>持续更新</h3>
          <p>定期更新课程内容，追踪行业趋势</p>
        </div>
      </div>
    </section>

    <!-- 行动号召 -->
    <section class="cta-section">
      <h2>现在就开始学习</h2>
      <p>加入数千名学生，开启你的学习之旅</p>
      <router-link to="/register" class="cta-btn large">免费注册账号</router-link>
    </section>
  </div>
</template>

<script>
export default {
  name: 'HomePage',
  data() {
    return {
      featuredCourses: [
        {
          id: 1,
          name: 'Vue.js 从入门到精通',
          instructor: '张三',
          description: '学习现代化前端框架Vue.js的开发技能',
          category: '前端开发',
          studentCount: 1250,
          rating: 4.8
        },
        {
          id: 2,
          name: 'Python 数据科学',
          instructor: '李四',
          description: '掌握数据分析和机器学习的基础知识',
          category: '数据科学',
          studentCount: 980,
          rating: 4.7
        },
        {
          id: 3,
          name: 'Web 全栈开发',
          instructor: '王五',
          description: '前后端完整的Web开发课程',
          category: '后端开发',
          studentCount: 750,
          rating: 4.9
        }
      ],
      totalCourses: 150,
      totalUsers: 5000,
      totalLessons: 2500
    }
  },
  methods: {
    getCourseIcon(category) {
      const iconMap = {
        '前端开发': '🌐',
        '后端开发': '⚙️',
        '数据科学': '📊',
        '移动开发': '📱',
        '人工智能': '🤖'
      }
      return iconMap[category] || '📚'
    }
  }
}
</script>

<style scoped>
.home {
  width: 100%;
}

/* 英雄横幅 */
.hero-banner {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 3rem;
  align-items: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 16px;
  padding: 4rem;
  margin-bottom: 4rem;
  color: white;
}

.hero-content h1 {
  font-size: 3rem;
  font-weight: 800;
  margin: 0 0 1rem 0;
  line-height: 1.2;
}

.hero-content > p {
  font-size: 1.2rem;
  opacity: 0.95;
  margin: 0 0 2rem 0;
  font-weight: 300;
}

.hero-actions {
  display: flex;
  gap: 1.5rem;
  flex-wrap: wrap;
}

.cta-btn {
  display: inline-block;
  padding: 1rem 2rem;
  border-radius: 8px;
  text-decoration: none;
  font-weight: 700;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  border: 2px solid transparent;
}

.cta-btn.primary {
  background-color: white;
  color: #667eea;
}

.cta-btn.primary:hover {
  transform: translateY(-3px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.2);
}

.cta-btn.secondary {
  background-color: transparent;
  color: white;
  border-color: white;
}

.cta-btn.secondary:hover {
  background-color: rgba(255, 255, 255, 0.1);
  transform: translateY(-3px);
}

.hero-illustration {
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 8rem;
  opacity: 0.9;
}

/* 特色课程 */
.featured-section {
  margin-bottom: 5rem;
}

.section-header {
  text-align: center;
  margin-bottom: 3rem;
}

.section-header h2 {
  font-size: 2.2rem;
  color: #2c3e50;
  margin: 0 0 0.75rem 0;
  font-weight: 800;
}

.section-header p {
  font-size: 1.1rem;
  color: #95a5a6;
  margin: 0;
}

.course-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(340px, 1fr));
  gap: 2rem;
  margin-bottom: 2rem;
}

.course-card {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  display: flex;
  flex-direction: column;
  border: 1px solid #f0f0f0;
}

.course-card:hover {
  transform: translateY(-12px);
  box-shadow: 0 16px 32px rgba(0, 0, 0, 0.15);
}

.course-image {
  height: 180px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
}

.course-icon {
  font-size: 4rem;
  opacity: 0.8;
}

.course-badge {
  position: absolute;
  top: 1rem;
  right: 1rem;
  background: rgba(255, 255, 255, 0.9);
  color: #667eea;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 600;
}

.course-body {
  padding: 1.5rem;
  flex: 1;
  display: flex;
  flex-direction: column;
}

.course-card h3 {
  margin: 0 0 0.75rem 0;
  color: #2c3e50;
  font-size: 1.2rem;
  font-weight: 700;
}

.instructor {
  color: #7f8c8d;
  font-size: 0.9rem;
  margin: 0 0 0.75rem 0;
}

.description {
  color: #95a5a6;
  font-size: 0.95rem;
  margin: 0 0 1.5rem 0;
  line-height: 1.6;
  flex: 1;
}

.course-stats {
  display: flex;
  gap: 1.5rem;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #ecf0f1;
}

.stat {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.9rem;
  color: #7f8c8d;
}

.stat .icon {
  font-size: 1.1rem;
}

.view-btn {
  display: block;
  padding: 0.8rem 1.2rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  text-decoration: none;
  text-align: center;
  border-radius: 8px;
  font-weight: 600;
  transition: all 0.3s;
}

.view-btn:hover {
  opacity: 0.95;
  transform: translateX(2px);
}

.view-all {
  text-align: center;
}

.view-all-btn {
  display: inline-block;
  padding: 1rem 2rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  text-decoration: none;
  border-radius: 8px;
  font-weight: 600;
  transition: all 0.3s;
}

.view-all-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3);
}

/* 统计信息 */
.stats-section {
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.08) 0%, rgba(118, 75, 162, 0.08) 100%);
  padding: 4rem 2rem;
  border-radius: 16px;
  margin-bottom: 5rem;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
}

.stat-card {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  text-align: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  transition: all 0.3s;
}

.stat-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
}

.stat-number {
  font-size: 2.8rem;
  font-weight: 800;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 0.5rem;
}

.stat-label {
  font-size: 1.1rem;
  color: #2c3e50;
  font-weight: 700;
  margin-bottom: 0.5rem;
}

.stat-description {
  color: #95a5a6;
  font-size: 0.9rem;
}

/* 特性部分 */
.features-section {
  margin-bottom: 5rem;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
}

.feature-card {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  text-align: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  transition: all 0.3s;
  border-left: 4px solid transparent;
}

.feature-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.1);
  border-left-color: #667eea;
}

.feature-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
  display: block;
}

.feature-card h3 {
  color: #2c3e50;
  font-size: 1.2rem;
  margin: 0 0 0.75rem 0;
  font-weight: 700;
}

.feature-card p {
  color: #95a5a6;
  margin: 0;
  line-height: 1.6;
}

/* 行动号召 */
.cta-section {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 4rem 2rem;
  border-radius: 16px;
  text-align: center;
}

.cta-section h2 {
  font-size: 2.2rem;
  font-weight: 800;
  margin: 0 0 1rem 0;
}

.cta-section p {
  font-size: 1.1rem;
  opacity: 0.95;
  margin: 0 0 2rem 0;
}

.cta-btn.large {
  padding: 1.2rem 2.5rem;
  font-size: 1.1rem;
  background-color: white;
  color: #667eea;
}

.cta-btn.large:hover {
  transform: translateY(-4px);
  box-shadow: 0 16px 32px rgba(0, 0, 0, 0.2);
}

@media (max-width: 768px) {
  .hero-banner {
    grid-template-columns: 1fr;
    padding: 2rem;
  }

  .hero-content h1 {
    font-size: 2rem;
  }

  .hero-actions {
    flex-direction: column;
  }

  .hero-illustration {
    font-size: 5rem;
  }

  .course-grid {
    grid-template-columns: 1fr;
  }

  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .features-grid {
    grid-template-columns: 1fr;
  }
}
</style>
