<template>
  <div class="community-container">
    <div class="community-header">
      <h1>社区</h1>
      <router-link to="/community/new-post" class="btn-new-post">+ 发表话题</router-link>
    </div>

    <div class="community-layout">
      <div class="sidebar">
        <div class="categories">
          <h3>分类</h3>
          <button 
            v-for="cat in categories" 
            :key="cat"
            :class="{ active: activeCategory === cat }"
            @click="activeCategory = cat"
            class="category-btn"
          >
            {{ cat }}
          </button>
        </div>
      </div>

      <div class="main-content">
        <div class="filters">
          <select v-model="sortBy" class="sort-select">
            <option value="latest">最新</option>
            <option value="popular">热门</option>
            <option value="trending">趋势</option>
          </select>
        </div>

        <div class="posts-list">
          <div v-for="post in posts" :key="post.id" class="post-item">
            <div class="post-avatar">
              <img :src="post.author.avatar" :alt="post.author.name">
            </div>
            <div class="post-content">
              <div class="post-header">
                <h2 class="post-title">{{ post.title }}</h2>
                <span class="post-category">{{ post.category }}</span>
              </div>
              <p class="post-excerpt">{{ post.excerpt }}</p>
              <div class="post-meta">
                <span class="author">{{ post.author.name }}</span>
                <span class="time">{{ post.time }}</span>
                <span class="replies">💬 {{ post.replies }} 条回复</span>
                <span class="views">👁 {{ post.views }} 次浏览</span>
              </div>
            </div>
            <router-link :to="`/community/${post.id}`" class="btn-read">查看</router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'CommunityHub',
  data() {
    return {
      activeCategory: '全部',
      sortBy: 'latest',
      categories: ['全部', '公共问答', '技术分享', '学习心得', '平台公告', '资源共享'],
      posts: [
        {
          id: 1,
          title: 'Vue 3 Composition API 最佳实践',
          excerpt: '在这篇文章中，我将分享我在使用 Vue 3 Composition API 时的一些最佳实践和常见陷阱...',
          category: '分享',
          author: {
            name: '李四',
            avatar: 'https://via.placeholder.com/40?text=User1'
          },
          time: '2小时前',
          replies: 12,
          views: 342
        },
        {
          id: 2,
          title: '如何优化大型 Vue 项目的性能？',
          excerpt: '我的项目最近遇到性能问题，有没有人可以分享一些优化经验？特别是在大列表渲染方面...',
          category: '问答',
          author: {
            name: '王五',
            avatar: 'https://via.placeholder.com/40?text=User2'
          },
          time: '5小时前',
          replies: 8,
          views: 256
        },
        {
          id: 3,
          title: '关于学习路径的一些思考',
          excerpt: '作为一个从零开始学习前端的学生，我想和大家分享一下我认为比较高效的学习路径和资源...',
          category: '分享',
          author: {
            name: '赵六',
            avatar: 'https://via.placeholder.com/40?text=User3'
          },
          time: '1天前',
          replies: 24,
          views: 1203
        },
        {
          id: 4,
          title: '【建议】增加更多的实战项目课程',
          excerpt: '我觉得平台现有的课程理论居多，能否增加更多的实战项目课程来帮助学生快速成长？...',
          category: '建议',
          author: {
            name: '周七',
            avatar: 'https://via.placeholder.com/40?text=User4'
          },
          time: '1天前',
          replies: 6,
          views: 189
        }
      ]
    }
  }
}
</script>

<style scoped>
.community-container {
  padding: 30px;
  background: #f5f5f5;
  min-height: 100vh;
}

.community-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

.community-header h1 {
  font-size: 28px;
  color: #333;
}

.btn-new-post {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 12px 24px;
  border-radius: 4px;
  text-decoration: none;
  font-weight: 600;
  transition: opacity 0.3s;
}

.btn-new-post:hover {
  opacity: 0.9;
}

.community-layout {
  display: grid;
  grid-template-columns: 200px 1fr;
  gap: 30px;
}

.sidebar {
  background: white;
  padding: 20px;
  border-radius: 8px;
  height: fit-content;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.categories h3 {
  margin-bottom: 15px;
  color: #333;
}

.category-btn {
  display: block;
  width: 100%;
  padding: 10px 15px;
  margin-bottom: 8px;
  background: none;
  border: 1px solid transparent;
  border-radius: 4px;
  cursor: pointer;
  text-align: left;
  color: #666;
  transition: all 0.3s;
}

.category-btn:hover {
  background: #f5f5f5;
}

.category-btn.active {
  background: #667eea;
  color: white;
  border-color: #667eea;
}

.main-content {
  flex: 1;
}

.filters {
  margin-bottom: 20px;
}

.sort-select {
  padding: 10px 15px;
  border: 1px solid #ddd;
  border-radius: 4px;
  background: white;
  cursor: pointer;
  font-size: 14px;
}

.posts-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.post-item {
  display: flex;
  gap: 20px;
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: all 0.3s;
}

.post-item:hover {
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
  transform: translateY(-2px);
}

.post-avatar {
  flex-shrink: 0;
}

.post-avatar img {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  object-fit: cover;
}

.post-content {
  flex: 1;
}

.post-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 10px;
}

.post-title {
  font-size: 18px;
  margin: 0;
  color: #333;
  cursor: pointer;
  transition: color 0.3s;
}

.post-title:hover {
  color: #667eea;
}

.post-category {
  display: inline-block;
  background: #f0f0f0;
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 12px;
  color: #667eea;
  font-weight: 600;
}

.post-excerpt {
  color: #666;
  font-size: 14px;
  line-height: 1.6;
  margin-bottom: 12px;
}

.post-meta {
  display: flex;
  gap: 20px;
  font-size: 12px;
  color: #999;
}

.btn-read {
  flex-shrink: 0;
  align-self: center;
  padding: 8px 16px;
  background: #f0f0f0;
  color: #667eea;
  border: none;
  border-radius: 4px;
  text-decoration: none;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-read:hover {
  background: #667eea;
  color: white;
}

@media (max-width: 768px) {
  .community-layout {
    grid-template-columns: 1fr;
  }

  .sidebar {
    display: none;
  }

  .post-item {
    flex-direction: column;
  }
}
</style>
