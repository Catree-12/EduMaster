<template>
  <div class="community-container">
    <!-- 固定顶部区域 -->
    <div class="community-header-fixed">
      <div class="community-header">
        <h1>社区</h1>
        <div class="search-box">
          <el-input
            v-model="searchQuery"
            placeholder="搜索话题..."
            prefix-icon="el-icon-search"
            clearable
            @input="handleSearch"
          ></el-input>
        </div>
        <router-link to="/community/new-post" class="btn-new-post">+ 发表话题</router-link>
      </div>
    </div>

    <!-- 可滚动内容区域 -->
    <div class="community-layout">
      <div class="sidebar">
        <div class="sort-options">
          <h3>排序</h3>
          <button 
            v-for="sort in sortOptions" 
            :key="sort.value"
            :class="{ active: sortBy === sort.value }"
            @click="sortBy = sort.value"
            class="sort-btn"
          >
            {{ sort.label }}
          </button>
        </div>
        
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

        <div class="posts-list">
          <div v-for="post in paginatedPosts" :key="post.id" class="thread-card" @click="viewPost(post.id)">
            <div class="thread-header">
              <h3>{{ post.title }}</h3>
            </div>
            <p class="thread-preview">{{ post.excerpt }}</p>
            <div class="thread-meta-row">
              <div class="thread-info">
                <span class="author-name">{{ post.author.name }}</span>
                <span class="separator">·</span>
                <span class="publish-time">{{ post.time }}</span>
              </div>
              <div class="thread-stats">
                <span class="stat-item">
                  <i class="icon-view">👁</i>
                  {{ post.views }}
                </span>
                <span class="stat-item">
                  <i class="icon-reply">💬</i>
                  {{ post.replies }}
                </span>
                <button 
                  :class="['like-btn-inline', { liked: post.isLiked }]" 
                  @click.stop="toggleLike(post)"
                >
                  {{ post.isLiked ? '❤️' : '🤍' }}
                  {{ post.likeCount }}
                </button>
                <div v-if="canEditPost(post)" class="thread-manage">
                  <a class="manage-link edit" @click.stop="editPost(post.id)">编辑</a>
                  <a class="manage-link delete" @click.stop="deletePost(post.id)">删除</a>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 分页组件 -->
        <div class="pagination-wrapper">
          <el-pagination
            @current-change="handlePageChange"
            :current-page="currentPage"
            :page-size="pageSize"
            layout="total, prev, pager, next, jumper"
            :total="filteredPosts.length">
          </el-pagination>
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
      currentUserId: 1, // 当前登录用户ID（实际应从store获取）
      searchQuery: '',
      activeCategory: '全部',
      sortBy: 'default',
      currentPage: 1,
      pageSize: 10,
      sortOptions: [
        { label: '默认', value: 'default' },
        { label: '最新', value: 'latest' },
        { label: '热门', value: 'popular' }
      ],
      categories: ['全部', '公共问答', '技术分享', '学习心得', '我的帖子'],
      posts: [
        {
          id: 1,
          title: 'Vue 3 Composition API 最佳实践',
          excerpt: '在这篇文章中，我将分享我在使用 Vue 3 Composition API 时的一些最佳实践和常见陷阱...',
          category: '技术分享',
          author: {
            id: 1,
            name: '李四',
            avatar: 'https://via.placeholder.com/40?text=User1'
          },
          time: '2024-01-24 10:30',
          replies: 12,
          views: 342,
          likeCount: 25,
          isLiked: false
        },
        {
          id: 2,
          title: '如何优化大型 Vue 项目的性能？',
          excerpt: '我的项目最近遇到性能问题，有没有人可以分享一些优化经验？特别是在大列表渲染方面...',
          category: '公共问答',
          author: {
            id: 2,
            name: '王五',
            avatar: 'https://via.placeholder.com/40?text=User2'
          },
          time: '2024-01-24 15:20',
          replies: 8,
          views: 256,
          likeCount: 15,
          isLiked: false
        },
        {
          id: 3,
          title: '关于学习路径的一些思考',
          excerpt: '作为一个从零开始学习前端的学生，我想和大家分享一下我认为比较高效的学习路径和资源...',
          category: '学习心得',
          author: {
            id: 3,
            name: '赵六',
            avatar: 'https://via.placeholder.com/40?text=User3'
          },
          time: '2024-01-23 09:15',
          replies: 24,
          views: 1203,
          likeCount: 48,
          isLiked: true
        },
        {
          id: 4,
          title: '【建议】增加更多的实战项目课程',
          excerpt: '我觉得平台现有的课程理论居多，能否增加更多的实战项目课程来帮助学生快速成长？...',
          category: '公共问答',
          author: {
            id: 4,
            name: '周七',
            avatar: 'https://via.placeholder.com/40?text=User4'
          },
          time: '2024-01-23 14:00',
          replies: 6,
          views: 189,
          likeCount: 10,
          isLiked: false
        },
        {
          id: 5,
          title: 'TypeScript 类型体操进阶技巧',
          excerpt: '深入探讨 TypeScript 中的高级类型技巧，包括条件类型、映射类型和模板字面量类型...',
          category: '技术分享',
          author: {
            id: 5,
            name: '陈八',
            avatar: 'https://via.placeholder.com/40?text=User5'
          },
          time: '2024-01-21 16:30',
          replies: 18,
          views: 876,
          likeCount: 32,
          isLiked: false
        },
        {
          id: 6,
          title: 'React Hooks 使用心得分享',
          excerpt: '最近一直在用 React Hooks，这里分享一些我踩过的坑和使用技巧...',
          category: '学习心得',
          author: {
            id: 6,
            name: '刘九',
            avatar: 'https://via.placeholder.com/40?text=User6'
          },
          time: '2024-01-19 11:00',
          replies: 15,
          views: 654,
          likeCount: 20,
          isLiked: false
        }
      ]
    }
  },
  computed: {
    filteredPosts() {
      let filtered = [...this.posts]
      
      // 分类筛选
      if (this.activeCategory !== '全部') {
        if (this.activeCategory === '我的帖子') {
          // TODO: 过滤当前用户的帖子
          filtered = filtered.filter(post => post.author.id === this.currentUserId)
        } else {
          filtered = filtered.filter(post => post.category === this.activeCategory)
        }
      }
      
      // 搜索筛选
      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase()
        filtered = filtered.filter(post => 
          post.title.toLowerCase().includes(query) ||
          post.excerpt.toLowerCase().includes(query) ||
          post.author.name.toLowerCase().includes(query)
        )
      }
      
      // 排序
      if (this.sortBy === 'default') {
        // 默认排序（按发布时间）
      } else if (this.sortBy === 'latest') {
        // 最新排序
      } else if (this.sortBy === 'popular') {
        // 热门排序（按回复数）
        filtered.sort((a, b) => b.replies - a.replies)
      }
      
      return filtered
    },
    paginatedPosts() {
      const start = (this.currentPage - 1) * this.pageSize
      const end = start + this.pageSize
      return this.filteredPosts.slice(start, end)
    }
  },
  methods: {
    handleSearch() {
      // 搜索逻辑已在 computed 中实现
      this.currentPage = 1 // 搜索后重置到第一页
    },
    handlePageChange(page) {
      this.currentPage = page
      // 滚动到列表顶部
      const mainContent = document.querySelector('.main-content')
      if (mainContent) {
        mainContent.scrollTop = 0
      }
    },
    viewPost(id) {
      this.$router.push(`/community/${id}`)
    },
    toggleLike(post) {
      post.isLiked = !post.isLiked
      post.likeCount += post.isLiked ? 1 : -1
      this.$message.success(post.isLiked ? '已点赞' : '已取消点赞')
    },
    canEditPost(post) {
      // 只有帖子作者才能编辑和删除
      return post.author.id === this.currentUserId
    },
    editPost(postId) {
      this.$router.push(`/community/edit/${postId}`)
    },
    deletePost(postId) {
      this.$confirm('确定要删除这个话题吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        const index = this.posts.findIndex(p => p.id === postId)
        if (index > -1) {
          this.posts.splice(index, 1)
          this.$message.success('话题已删除')
        }
      }).catch(() => {})
    }
  }
}
</script>

<style scoped lang="scss">
.community-container {
  background: #f8f9fb;
}

// 顶部区域
.community-header-fixed {
  background: #f8f9fb;
  padding: 2rem 8% 0;
}

.community-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1.5rem;
  padding-bottom: 2rem;

  h1 {
    font-size: 1.8rem;
    color: #2c3e50;
    white-space: nowrap;
  }

  .search-box {
    flex: 1;
    max-width: 500px;

    ::v-deep .el-input__inner {
      border-radius: 20px;
      height: 40px;
    }
  }

  .btn-new-post {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 0.65rem 1.5rem;
    border-radius: 20px;
    text-decoration: none;
    font-weight: 600;
    transition: all 0.3s;
    white-space: nowrap;
    box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);

    &:hover {
      transform: translateY(-2px);
      box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }
  }
}

.community-layout {
  display: grid;
  grid-template-columns: 200px 1fr;
  gap: 2rem;
  padding: 0 8% 0;
  height: calc(100vh - 180px);
  overflow: hidden;
}

.sidebar {
  height: 100%;
  overflow-y: auto;
  padding-right: 0.5rem;

  .sort-options {
    background: white;
    padding: 1.5rem;
    border-radius: 10px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
    margin-bottom: 1.5rem;

    h3 {
      margin-bottom: 1rem;
      color: #2c3e50;
      font-size: 1rem;
      font-weight: 600;
    }

    .sort-btn {
      display: block;
      width: 100%;
      padding: 0.65rem 1rem;
      margin-bottom: 0.5rem;
      background: none;
      border: 1px solid transparent;
      border-radius: 6px;
      cursor: pointer;
      text-align: left;
      color: #666;
      transition: all 0.3s;
      font-size: 0.9rem;

      &:hover {
        background: #f5f7fa;
        color: #667eea;
      }

      &.active {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-color: transparent;
        font-weight: 600;
      }
    }
  }

  .categories {
    background: white;
    padding: 1.5rem;
    border-radius: 10px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
    h3 {
      margin-bottom: 1rem;
      color: #2c3e50;
      font-size: 1rem;
      font-weight: 600;
    }

    .category-btn {
      display: block;
      width: 100%;
      padding: 0.65rem 1rem;
      margin-bottom: 0.5rem;
      background: none;
      border: 1px solid transparent;
      border-radius: 6px;
      cursor: pointer;
      text-align: left;
      color: #666;
      transition: all 0.3s;
      font-size: 0.9rem;

      &:hover {
        background: #f5f7fa;
        color: #667eea;
      }

      &.active {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-color: transparent;
        font-weight: 600;
      }
    }
  }
}

.main-content {
  flex: 1;
  min-width: 0;
  height: 100%;
  overflow-y: auto;
  padding-right: 0.5rem;
}

.posts-list {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

// 使用 CourseCommunity 的卡片风格
.thread-card {
  padding: 1.5rem;
  border: 1px solid #ecf0f1;
  border-radius: 8px;
  background: white;
  transition: all 0.3s;
  cursor: pointer;

  &:hover {
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    transform: translateY(-2px);
  }

  .thread-header {
    margin-bottom: 0.75rem;

    h3 {
      margin: 0;
      color: #2c3e50;
      font-size: 1.1rem;
      transition: color 0.3s;
    }
  }

  &:hover .thread-header h3 {
    color: #667eea;
  }

  .thread-preview {
    color: #7f8c8d;
    margin: 0.75rem 0;
    line-height: 1.5;
    overflow: hidden;
    text-overflow: ellipsis;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
  }

  .thread-meta-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-top: 0.75rem;
    border-top: 1px solid #f3f4f6;
  }

  .thread-info {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.875rem;
    color: #6b7280;
  }

  .author-name {
    font-weight: 500;
    color: #4b5563;
  }

  .separator {
    color: #d1d5db;
  }

  .publish-time {
    color: #9ca3af;
  }

  .thread-stats {
    display: flex;
    align-items: center;
    gap: 1.5rem;
  }

  .stat-item {
    display: flex;
    align-items: center;
    gap: 0.25rem;
    font-size: 0.875rem;
    color: #6b7280;
  }

  .icon-view,
  .icon-reply {
    font-size: 1rem;
  }

  .like-btn-inline {
    display: flex;
    align-items: center;
    gap: 0.25rem;
    padding: 0.25rem 0.75rem;
    border: 1px solid #e5e7eb;
    background: white;
    border-radius: 6px;
    cursor: pointer;
    transition: all 0.2s;
    font-size: 0.875rem;
    color: #6b7280;

    &:hover {
      border-color: #667eea;
      background: #f5f7ff;
    }

    &.liked {
      border-color: #ec4899;
      background: #fdf2f8;
      color: #ec4899;
    }
  }

  .thread-manage {
    display: flex;
    gap: 1rem;
  }

  .manage-link {
    font-size: 0.875rem;
    cursor: pointer;
    transition: color 0.2s;

    &.edit {
      color: #667eea;

      &:hover {
        color: #5568d3;
        text-decoration: underline;
      }
    }

    &.delete {
      color: #ef4444;

      &:hover {
        color: #dc2626;
        text-decoration: underline;
      }
    }
  }
}

.pagination-wrapper {
  display: flex;
  justify-content: center;
  padding: 2rem 0;
  margin-top: 2rem;
  border-top: 1px solid #e5e7eb;

  ::v-deep .el-pagination {
    .el-pager li {
      &.active {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
      }
    }

    button,
    .el-pager li {
      &:hover {
        color: #667eea;
      }
    }
  }
}

@media (max-width: 768px) {
  .community-container {
    padding: 1.5rem 5%;
  }

  .community-header {
    flex-direction: column;
    align-items: stretch;

    h1 {
      text-align: center;
    }

    .search-box {
      max-width: 100%;
    }

    .btn-new-post {
      text-align: center;
    }
  }

  .community-layout {
    grid-template-columns: 1fr;
  }

  .sidebar {
    position: static;

    .categories {
      .category-btn {
        display: inline-block;
        width: auto;
        margin-right: 0.5rem;
      }
    }
  }

  .thread-meta {
    font-size: 0.75rem;

    .meta-left,
    .meta-right {
      gap: 0.5rem;
    }
  }
}
</style>
