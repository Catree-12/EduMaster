<template>
  <div class="post-detail-container">
    <div class="breadcrumb">
      <el-breadcrumb separator="/">
        <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
        <el-breadcrumb-item :to="{ path: '/community' }">社区</el-breadcrumb-item>
        <el-breadcrumb-item>{{ post.title }}</el-breadcrumb-item>
      </el-breadcrumb>
    </div>

    <div class="post-detail-layout">
      <div class="post-main">
        <el-card class="post-article" shadow="hover">
          <header class="article-header">
            <div class="header-top">
              <el-tag size="small" effect="dark">{{ post.category }}</el-tag>
              <span class="time">{{ post.time }}</span>
            </div>
            <h1 class="article-title">{{ post.title }}</h1>
            
            <div class="author-info">
              <el-avatar :size="50" :src="post.author.avatar"></el-avatar>
              <div class="author-details">
                <p class="author-name">{{ post.author.name }}</p>
                <p class="author-bio">{{ post.author.bio }}</p>
              </div>
              <el-button type="primary" size="small" icon="el-icon-plus" plain>关注</el-button>
            </div>
          </header>

          <div class="article-content" v-html="formattedContent"></div>

          <div class="article-footer">
            <div class="actions">
              <el-button :type="liked ? 'danger' : 'default'" icon="el-icon-star-off" circle @click="toggleLike"></el-button>
              <span class="action-count">{{ post.likes }} 赞</span>
              
              <el-button icon="el-icon-chat-dot-round" circle style="margin-left: 20px;"></el-button>
              <span class="action-count">{{ post.replies.length }} 评论</span>
              
              <el-button icon="el-icon-share" circle style="margin-left: 20px;"></el-button>
              <span class="action-count">分享</span>
            </div>
            <div class="tags">
              <el-tag v-for="tag in post.tags" :key="tag" type="info" size="small" class="tag-item">{{ tag }}</el-tag>
            </div>
          </div>
        </el-card>

        <el-card class="comments-section" shadow="hover">
          <div slot="header" class="clearfix">
            <span>{{ post.replies.length }} 条评论</span>
          </div>
          
          <div class="comment-form">
            <el-input
              type="textarea"
              :rows="3"
              placeholder="分享你的想法..."
              v-model="newComment">
            </el-input>
            <div class="form-actions">
              <el-button type="primary" size="small" @click="handleAddComment">发送评论</el-button>
            </div>
          </div>

          <div class="comments-list">
            <div v-for="reply in post.replies" :key="reply.id" class="comment-item">
              <div class="comment-avatar">
                <el-avatar :size="40" :src="reply.author.avatar"></el-avatar>
              </div>
              <div class="comment-content">
                <div class="comment-header">
                  <span class="comment-author">{{ reply.author.name }}</span>
                  <span class="comment-time">{{ reply.time }}</span>
                </div>
                <p class="comment-text">{{ reply.text }}</p>
                <div class="comment-actions">
                  <el-button type="text" size="mini" icon="el-icon-chat-square">回复</el-button>
                  <el-button type="text" size="mini" icon="el-icon-thumb">点赞</el-button>
                </div>
              </div>
            </div>
          </div>
        </el-card>
      </div>

      <aside class="sidebar">
        <el-card class="stats-card" shadow="hover">
          <div class="stats-row">
            <div class="stat-item">
              <div class="stat-value">{{ post.views }}</div>
              <div class="stat-label">浏览</div>
            </div>
            <div class="stat-divider"></div>
            <div class="stat-item">
              <div class="stat-value">{{ post.likes }}</div>
              <div class="stat-label">获赞</div>
            </div>
            <div class="stat-divider"></div>
            <div class="stat-item">
              <div class="stat-value">{{ post.replies.length }}</div>
              <div class="stat-label">评论</div>
            </div>
          </div>
        </el-card>

        <el-card class="related-posts" shadow="hover">
          <div slot="header">
            <span>相关话题</span>
          </div>
          <div v-for="item in relatedPosts" :key="item.id" class="related-item">
            <router-link :to="`/community/${item.id}`" class="related-link">
              <i class="el-icon-document"></i> {{ item.title }}
            </router-link>
          </div>
        </el-card>
      </aside>
    </div>
  </div>
</template>

<script>
export default {
  name: 'PostDetail',
  data() {
    return {
      post: {
        id: 1,
        title: 'Vue 3 Composition API 最佳实践',
        category: '技术分享',
        time: '2小时前',
        views: 1205,
        likes: 45,
        content: `
          <p>Vue 3 的 Composition API 为代码组织提供了更大的灵活性。在这篇文章中，我将分享一些我在实际项目中的使用经验。</p>
          <h3>1. 逻辑复用</h3>
          <p>使用 Composition API 最主要的好处之一就是逻辑复用。我们可以将相关的逻辑提取到独立的 hook 函数中...</p>
          <h3>2. 代码组织</h3>
          <p>不再受限于 Options API 的 data, methods, computed 分割，我们可以按照功能特性来组织代码...</p>
          <p>（此处省略更多内容）</p>
        `,
        author: {
          name: '李四',
          avatar: 'https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png',
          bio: '资深前端开发工程师，热爱 Vue 和 React'
        },
        tags: ['Vue.js', 'Frontend', 'JavaScript'],
        replies: [
          {
            id: 101,
            author: {
              name: '张三',
              avatar: 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png'
            },
            time: '1小时前',
            text: '非常有用的分享，特别是关于逻辑复用的部分！'
          },
          {
            id: 102,
            author: {
              name: '王五',
              avatar: 'https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png'
            },
            time: '30分钟前',
            text: '请问有没有关于 TypeScript 配合使用的建议？'
          }
        ]
      },
      newComment: '',
      liked: false,
      relatedPosts: [
        { id: 2, title: '如何优化大型 Vue 项目的性能？' },
        { id: 3, title: 'TypeScript 在 Vue 3 中的应用' },
        { id: 4, title: '前端工程化实践指南' }
      ]
    }
  },
  computed: {
    formattedContent() {
      // 简单处理换行，实际项目中可能需要 Markdown 解析器
      return this.post.content
    }
  },
  methods: {
    toggleLike() {
      this.liked = !this.liked
      if (this.liked) {
        this.post.likes++
        this.$message.success('点赞成功')
      } else {
        this.post.likes--
      }
    },
    handleAddComment() {
      if (!this.newComment.trim()) {
        this.$message.warning('请输入评论内容')
        return
      }
      
      const newReply = {
        id: Date.now(),
        author: {
          name: '当前用户',
          avatar: 'https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png'
        },
        time: '刚刚',
        text: this.newComment
      }
      
      this.post.replies.unshift(newReply)
      this.newComment = ''
      this.$message.success('评论发表成功')
    }
  }
}
</script>

<style scoped lang="scss">
.post-detail-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.breadcrumb {
  margin-bottom: 20px;
}

.post-detail-layout {
  display: flex;
  gap: 20px;
}

.post-main {
  flex: 1;
  min-width: 0; /* 防止 flex 子项溢出 */
}

.sidebar {
  width: 300px;
  flex-shrink: 0;
}

.post-article {
  margin-bottom: 20px;
  
  .article-header {
    margin-bottom: 30px;
    border-bottom: 1px solid #ebeef5;
    padding-bottom: 20px;

    .header-top {
      display: flex;
      align-items: center;
      gap: 10px;
      margin-bottom: 15px;
      
      .time {
        color: #909399;
        font-size: 13px;
      }
    }

    .article-title {
      font-size: 28px;
      color: #303133;
      margin: 0 0 20px 0;
      line-height: 1.4;
    }

    .author-info {
      display: flex;
      align-items: center;
      gap: 15px;

      .author-details {
        flex: 1;
        
        .author-name {
          font-weight: bold;
          color: #303133;
          margin: 0 0 4px 0;
        }
        
        .author-bio {
          font-size: 12px;
          color: #909399;
          margin: 0;
        }
      }
    }
  }

  .article-content {
    font-size: 16px;
    line-height: 1.8;
    color: #303133;
    margin-bottom: 40px;
    min-height: 200px;
  }

  .article-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-top: 20px;
    border-top: 1px solid #ebeef5;

    .actions {
      display: flex;
      align-items: center;
      
      .action-count {
        margin-left: 8px;
        color: #606266;
        font-size: 14px;
      }
    }

    .tag-item {
      margin-left: 10px;
    }
  }
}

.comments-section {
  .comment-form {
    margin-bottom: 30px;
    
    .form-actions {
      margin-top: 10px;
      text-align: right;
    }
  }

  .comment-item {
    display: flex;
    gap: 15px;
    padding: 20px 0;
    border-bottom: 1px solid #ebeef5;

    &:last-child {
      border-bottom: none;
    }

    .comment-content {
      flex: 1;

      .comment-header {
        margin-bottom: 8px;
        
        .comment-author {
          font-weight: bold;
          color: #303133;
          margin-right: 10px;
        }
        
        .comment-time {
          font-size: 12px;
          color: #909399;
        }
      }

      .comment-text {
        color: #606266;
        line-height: 1.6;
        margin: 0 0 10px 0;
      }

      .comment-actions {
        .el-button {
          padding: 0;
          color: #909399;
          margin-right: 15px;
          
          &:hover {
            color: #409eff;
          }
        }
      }
    }
  }
}

.stats-card {
  margin-bottom: 20px;

  .stats-row {
    display: flex;
    justify-content: space-around;
    align-items: center;
    text-align: center;

    .stat-item {
      .stat-value {
        font-size: 20px;
        font-weight: bold;
        color: #303133;
      }
      .stat-label {
        font-size: 12px;
        color: #909399;
        margin-top: 4px;
      }
    }

    .stat-divider {
      width: 1px;
      height: 30px;
      background: #ebeef5;
    }
  }
}

.related-posts {
  .related-item {
    margin-bottom: 12px;
    
    &:last-child {
      margin-bottom: 0;
    }

    .related-link {
      color: #606266;
      text-decoration: none;
      font-size: 14px;
      display: block;
      line-height: 1.4;
      
      &:hover {
        color: #409eff;
      }

      i {
        margin-right: 5px;
        color: #909399;
      }
    }
  }
}
</style>
