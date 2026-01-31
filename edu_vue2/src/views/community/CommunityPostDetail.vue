<template>
  <div class="thread-detail-page">
    <div class="thread-detail-container">
      <!-- 1. 顶部返回层 -->
      <div class="top-bar">
        <button @click="goBack" class="back-btn">
          ← 返回
        </button>
      </div>

      <!-- 2. 楼主发帖区（主贴卡片） -->
      <div class="main-post-card">
        <!-- 用户信息行 -->
        <div class="user-info-row">
          <div class="user-info">
            <img :src="thread.avatar" :alt="thread.author" class="user-avatar">
            <div class="user-details">
              <div class="user-name-row">
                <span class="user-name">{{ thread.author }}</span>
                <span v-if="thread.authorRole === 'teacher'" class="role-badge">老师</span>
                <span v-else-if="thread.authorRole === 'admin'" class="role-badge admin">管理员</span>
              </div>
              <span class="publish-time">{{ thread.createTime }}</span>
            </div>
          </div>
        </div>

        <!-- 话题正文区 -->
        <div class="post-content-area">
          <h1 class="post-title">{{ thread.title }}</h1>
          <div class="post-content">
            {{ thread.content }}
          </div>
        </div>

        <!-- 互动统计与管理 -->
        <div class="post-meta-row">
          <div class="view-stats">
            <span class="stat-item">
              <i class="icon">👁</i>
              {{ thread.viewCount }} 次浏览
            </span>
            <button 
              :class="['like-btn', { liked: thread.isLiked }]"
              @click="toggleThreadLike"
            >
              <i class="icon">{{ thread.isLiked ? '❤️' : '🤍' }}</i>
              {{ thread.likeCount }}
            </button>
          </div>
          <div v-if="canEditPost || canDeletePost" class="post-actions">
            <a v-if="canEditPost" class="action-link edit" @click="editPost">编辑</a>
            <a v-if="canDeletePost" class="action-link delete" @click="deletePost">删除</a>
          </div>
        </div>
      </div>

      <!-- 3. 回复统计与列表区 -->
      <div class="replies-section">
        <!-- 回复总数行 -->
        <div class="replies-header">
          <span class="replies-count">共 {{ replies.length }} 条回复</span>
        </div>

        <!-- 回复卡片列表 -->
        <div v-if="replies.length > 0" class="replies-list">
          <div 
            v-for="reply in organizedReplies" 
            :key="reply.id" 
            class="reply-card"
          >
            <div class="reply-header">
              <div class="reply-user-info">
                <img :src="reply.avatar" :alt="reply.author" class="reply-avatar">
                <div class="reply-user-details">
                  <span class="reply-user-name">{{ reply.author }}</span>
                  <span class="reply-time">{{ reply.createTime }}</span>
                </div>
              </div>
            </div>
            <div class="reply-content">
              <span v-if="reply.replyTo" class="reply-to-tag">
                回复 @{{ reply.replyTo }}:
              </span>
              {{ reply.content }}
            </div>
            <div class="reply-actions-row">
              <button 
                :class="['like-btn-small', { liked: reply.isLiked }]"
                @click="toggleReplyLike(reply)"
              >
                <i class="icon">{{ reply.isLiked ? '❤️' : '🤍' }}</i>
                {{ reply.likeCount || 0 }}
              </button>
              <a class="reply-to-link" @click="replyToUser(reply)">
                回复
              </a>
              <a 
                v-if="canDeleteReply(reply)" 
                class="delete-link" 
                @click="deleteReply(reply.id)"
              >
                删除
              </a>
            </div>
            
            <!-- 子回复列表 -->
            <div v-if="reply.children && reply.children.length > 0" class="sub-replies">
              <div 
                v-for="subReply in reply.children" 
                :key="subReply.id" 
                class="sub-reply-card"
              >
                <div class="reply-header">
                  <div class="reply-user-info">
                    <img :src="subReply.avatar" :alt="subReply.author" class="reply-avatar">
                    <div class="reply-user-details">
                      <span class="reply-user-name">{{ subReply.author }}</span>
                      <span class="reply-time">{{ subReply.createTime }}</span>
                    </div>
                  </div>
                </div>
                <div class="reply-content">
                  <span v-if="subReply.replyTo" class="reply-to-tag">
                    回复 @{{ subReply.replyTo }}:
                  </span>
                  {{ subReply.content }}
                </div>
                <div class="reply-actions-row">
                  <button 
                    :class="['like-btn-small', { liked: subReply.isLiked }]"
                    @click="toggleReplyLike(subReply)"
                  >
                    <i class="icon">{{ subReply.isLiked ? '❤️' : '🤍' }}</i>
                    {{ subReply.likeCount || 0 }}
                  </button>
                  <a class="reply-to-link" @click="replyToUser(subReply)">
                    回复
                  </a>
                  <a 
                    v-if="canDeleteReply(subReply)" 
                    class="delete-link" 
                    @click="deleteReply(subReply.id)"
                  >
                    删除
                  </a>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div v-else class="no-replies">
          <p>还没有回复，快来抢沙发吧~</p>
        </div>
      </div>

      <!-- 4. 底部快捷回复区 -->
      <div class="reply-input-section">
        <div class="reply-input-container">
          <div v-if="replyingTo" class="replying-to-banner">
            <span>回复 @{{ replyingTo.author }}</span>
            <button @click="cancelReply" class="cancel-reply-btn">✕</button>
          </div>
          <textarea 
            v-model="newReplyContent"
            class="reply-textarea"
            :placeholder="replyingTo ? `回复 @${replyingTo.author}...` : '写下你的回复...'"
            rows="2"
          ></textarea>
          <button @click="submitReply" class="submit-reply-btn">
            发送回复
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'CommunityPostDetail',
  data() {
    return {
      threadId: this.$route.params.id,
      currentUserId: 1, // TODO: 从 Vuex 获取当前登录用户ID
      currentUserRole: 'student', // TODO: 从 Vuex 获取当前用户角色
      newReplyContent: '',
      replyingTo: null,
      thread: {
        id: 1,
        authorId: 1,
        author: '李四',
        authorRole: 'student',
        avatar: 'https://via.placeholder.com/50?text=User1',
        title: 'Vue 3 Composition API 最佳实践',
        content: '在这篇文章中，我将分享我在使用 Vue 3 Composition API 时的一些最佳实践和常见陷阱。\n\nComposition API 是 Vue 3 引入的一个重要特性，它提供了更灵活的代码组织方式。通过使用组合式函数，我们可以更好地复用逻辑代码。\n\n首先，我们来看看如何正确使用 ref 和 reactive。ref 主要用于基本类型数据，而 reactive 用于对象类型。在实际开发中，我发现合理选择这两者可以让代码更清晰。',
        createTime: '2小时前',
        viewCount: 342,
        likeCount: 15,
        isLiked: false
      },
      replies: [
        {
          id: 1,
          authorId: 2,
          author: '王五',
          avatar: 'https://via.placeholder.com/40?text=User2',
          content: '感谢分享！我最近也在学习 Composition API，你的经验很有帮助。',
          createTime: '1小时前',
          replyTo: null,
          replyToId: null,
          parentId: null,
          likeCount: 8,
          isLiked: false
        },
        {
          id: 2,
          authorId: 3,
          author: '赵六',
          avatar: 'https://via.placeholder.com/40?text=User3',
          content: '写得很好！我想问一下，在大型项目中，你是如何组织这些组合式函数的？',
          createTime: '45分钟前',
          replyTo: '李四',
          replyToId: null,
          parentId: null,
          likeCount: 3,
          isLiked: false
        },
        {
          id: 3,
          authorId: 1,
          author: '李四',
          avatar: 'https://via.placeholder.com/50?text=User1',
          content: '我一般会将可复用的逻辑放在 composables 文件夹中，每个功能一个文件。',
          createTime: '30分钟前',
          replyTo: '赵六',
          replyToId: 2,
          parentId: 2,
          likeCount: 5,
          isLiked: false
        }
      ]
    }
  },
  computed: {
    organizedReplies() {
      const topLevel = this.replies.filter(r => !r.parentId)
      
      return topLevel.map(reply => {
        const children = this.replies.filter(r => r.parentId === reply.id)
        return {
          ...reply,
          children
        }
      })
    },
    canEditPost() {
      // 只能编辑自己的帖子
      return this.thread.authorId === this.currentUserId
    },
    canDeletePost() {
      // 可以删除自己的帖子，或管理员可以删除任何帖子
      return this.thread.authorId === this.currentUserId || this.currentUserRole === 'admin'
    }
  },
  methods: {
    goBack() {
      this.$router.go(-1)
    },
    canDeleteReply(reply) {
      // 可以删除自己的回复，或管理员可以删除任何回复
      return reply.authorId === this.currentUserId || this.currentUserRole === 'admin'
    },
    toggleThreadLike() {
      this.thread.isLiked = !this.thread.isLiked
      this.thread.likeCount += this.thread.isLiked ? 1 : -1
      // TODO: 调用点赞API
    },
    toggleReplyLike(reply) {
      reply.isLiked = !reply.isLiked
      reply.likeCount = (reply.likeCount || 0) + (reply.isLiked ? 1 : -1)
      // TODO: 调用点赞API
    },
    replyToUser(reply) {
      this.replyingTo = reply
      this.$nextTick(() => {
        const textarea = document.querySelector('.reply-textarea')
        if (textarea) {
          textarea.focus()
        }
      })
    },
    cancelReply() {
      this.replyingTo = null
    },
    async submitReply() {
      if (!this.newReplyContent.trim()) {
        this.$message.error('请输入回复内容')
        return
      }

      try {
        // TODO: 调用提交回复API
        const newReply = {
          id: this.replies.length + 1,
          authorId: this.currentUserId,
          author: '当前用户',
          avatar: 'https://via.placeholder.com/40?text=Me',
          content: this.newReplyContent,
          createTime: '刚刚',
          replyTo: this.replyingTo ? this.replyingTo.author : null,
          replyToId: this.replyingTo ? this.replyingTo.id : null,
          parentId: this.replyingTo ? (this.replyingTo.parentId || this.replyingTo.id) : null,
          likeCount: 0,
          isLiked: false
        }
        
        this.replies.push(newReply)
        this.$message.success('回复成功')
        this.newReplyContent = ''
        this.replyingTo = null
      } catch (error) {
        this.$message.error('回复失败：' + error.message)
      }
    },
    editPost() {
      this.$router.push(`/community/edit/${this.threadId}`)
    },
    async deletePost() {
      try {
        await this.$confirm('确定要删除这个帖子吗？', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        })

        // TODO: 调用删除API
        this.$message.success('删除成功')
        this.$router.push('/community')
      } catch (error) {
        if (error !== 'cancel') {
          this.$message.error('删除失败：' + error.message)
        }
      }
    },
    async deleteReply(replyId) {
      try {
        await this.$confirm('确定要删除这条回复吗？', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        })

        // TODO: 调用删除API
        const index = this.replies.findIndex(r => r.id === replyId)
        if (index !== -1) {
          this.replies.splice(index, 1)
        }
        this.$message.success('删除成功')
      } catch (error) {
        if (error !== 'cancel') {
          this.$message.error('删除失败：' + error.message)
        }
      }
    }
  },
  mounted() {
    // TODO: 根据 threadId 加载帖子数据
    console.log('加载帖子ID:', this.threadId)
  }
}
</script>

<style scoped>
.thread-detail-page {
  width: 100%;
  background: #f5f7fa;
  min-height: 100vh;
}

.thread-detail-container {
  max-width: 900px;
  margin: 0 auto;
  padding: 2rem 1rem;
}

/* 1. 顶部返回栏 */
.top-bar {
  margin-bottom: 1.5rem;
}

.back-btn {
  background: none;
  border: none;
  color: #667eea;
  font-size: 1rem;
  cursor: pointer;
  padding: 0.5rem 0;
  transition: color 0.3s;
}

.back-btn:hover {
  color: #764ba2;
}

/* 2. 主贴卡片 */
.main-post-card {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  margin-bottom: 1.5rem;
}

.user-info-row {
  margin-bottom: 1.5rem;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.user-avatar {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  object-fit: cover;
}

.user-details {
  flex: 1;
}

.user-name-row {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.25rem;
}

.user-name {
  font-weight: 600;
  color: #2c3e50;
  font-size: 1rem;
}

.role-badge {
  display: inline-block;
  padding: 0.15rem 0.5rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 10px;
  font-size: 0.7rem;
  font-weight: 600;
}

.role-badge.admin {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
}

.publish-time {
  color: #95a5a6;
  font-size: 0.85rem;
}

.post-content-area {
  margin-bottom: 1.5rem;
}

.post-title {
  font-size: 1.75rem;
  color: #2c3e50;
  margin: 0 0 1rem 0;
  line-height: 1.4;
}

.post-content {
  color: #34495e;
  font-size: 1rem;
  line-height: 1.8;
  white-space: pre-line;
}

.post-meta-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 1rem;
  border-top: 1px solid #ecf0f1;
}

.view-stats {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.stat-item {
  color: #95a5a6;
  font-size: 0.875rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.like-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.4rem 1rem;
  background: white;
  border: 1px solid #ecf0f1;
  border-radius: 20px;
  color: #95a5a6;
  cursor: pointer;
  transition: all 0.3s;
  font-size: 0.875rem;
}

.like-btn:hover {
  border-color: #ff6b6b;
  color: #ff6b6b;
}

.like-btn.liked {
  border-color: #ff6b6b;
  color: #ff6b6b;
  background: #fff5f5;
}

.post-actions {
  display: flex;
  gap: 1rem;
}

.action-link {
  color: #667eea;
  cursor: pointer;
  font-size: 0.875rem;
  transition: color 0.3s;
}

.action-link:hover {
  color: #764ba2;
  text-decoration: underline;
}

.action-link.delete {
  color: #e74c3c;
}

.action-link.delete:hover {
  color: #c0392b;
}

/* 3. 回复区域 */
.replies-section {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  margin-bottom: 1.5rem;
}

.replies-header {
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #ecf0f1;
}

.replies-count {
  font-weight: 600;
  color: #2c3e50;
  font-size: 1.1rem;
}

.replies-list {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.reply-card {
  padding-bottom: 1.5rem;
  border-bottom: 1px solid #ecf0f1;
}

.reply-card:last-child {
  border-bottom: none;
  padding-bottom: 0;
}

.reply-header {
  margin-bottom: 0.75rem;
}

.reply-user-info {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.reply-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
}

.reply-user-name {
  font-weight: 600;
  color: #2c3e50;
  font-size: 0.95rem;
}

.reply-time {
  color: #95a5a6;
  font-size: 0.8rem;
  margin-left: 0.5rem;
}

.reply-content {
  color: #34495e;
  line-height: 1.6;
  margin-bottom: 0.75rem;
  font-size: 0.95rem;
}

.reply-to-tag {
  color: #667eea;
  margin-right: 0.5rem;
}

.reply-actions-row {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.like-btn-small {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  padding: 0.25rem 0.75rem;
  background: white;
  border: 1px solid #ecf0f1;
  border-radius: 15px;
  color: #95a5a6;
  cursor: pointer;
  transition: all 0.3s;
  font-size: 0.8rem;
}

.like-btn-small:hover {
  border-color: #ff6b6b;
  color: #ff6b6b;
}

.like-btn-small.liked {
  border-color: #ff6b6b;
  color: #ff6b6b;
  background: #fff5f5;
}

.reply-to-link,
.delete-link {
  color: #667eea;
  cursor: pointer;
  font-size: 0.85rem;
  transition: color 0.3s;
}

.reply-to-link:hover {
  color: #764ba2;
  text-decoration: underline;
}

.delete-link {
  color: #e74c3c;
}

.delete-link:hover {
  color: #c0392b;
  text-decoration: underline;
}

/* 子回复 */
.sub-replies {
  margin-top: 1rem;
  margin-left: 2rem;
  padding-left: 1rem;
  border-left: 2px solid #ecf0f1;
}

.sub-reply-card {
  padding-bottom: 1rem;
  margin-bottom: 1rem;
  border-bottom: 1px solid #f5f7fa;
}

.sub-reply-card:last-child {
  border-bottom: none;
  margin-bottom: 0;
  padding-bottom: 0;
}

.no-replies {
  text-align: center;
  padding: 3rem 2rem;
  color: #7f8c8d;
}

/* 4. 回复输入区 */
.reply-input-section {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  position: sticky;
  bottom: 1rem;
}

.replying-to-banner {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem 0.75rem;
  background: #f5f7fa;
  border-radius: 4px;
  margin-bottom: 0.75rem;
  font-size: 0.85rem;
  color: #667eea;
}

.cancel-reply-btn {
  background: none;
  border: none;
  color: #95a5a6;
  cursor: pointer;
  font-size: 1rem;
  padding: 0;
  width: 20px;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.cancel-reply-btn:hover {
  color: #e74c3c;
}

.reply-textarea {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #bdc3c7;
  border-radius: 4px;
  font-size: 0.95rem;
  font-family: inherit;
  resize: vertical;
  box-sizing: border-box;
  margin-bottom: 0.75rem;
}

.reply-textarea:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.submit-reply-btn {
  padding: 0.75rem 1.5rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 600;
  transition: opacity 0.3s;
  width: 100%;
}

.submit-reply-btn:hover {
  opacity: 0.9;
}

/* 响应式 */
@media (max-width: 768px) {
  .thread-detail-container {
    padding: 1rem 0.5rem;
  }

  .main-post-card,
  .replies-section,
  .reply-input-section {
    padding: 1.25rem;
  }

  .post-title {
    font-size: 1.4rem;
  }

  .sub-replies {
    margin-left: 1rem;
  }
}
</style>
