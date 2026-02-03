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
          <div class="user-avatar">{{ thread.author ? thread.author[0] : 'U' }}</div>
          <div class="user-details">
            <div class="user-name-row">
              <span class="user-name">{{ thread.author }}</span>
              <span v-if="thread.authorRole === 'teacher'" class="role-badge">老师</span>
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
            {{ thread.views }} 次浏览
          </span>
          <button 
            :class="['like-btn', { liked: thread.isLiked }]"
            @click="toggleThreadLike"
          >
            <i class="icon">{{ thread.isLiked ? '❤️' : '🤍' }}</i>
            {{ thread.likeCount }}
          </button>
        </div>
        <div v-if="canEditPost() || canDeletePost()" class="post-actions">
          <a v-if="canEditPost()" class="action-link edit" @click="editPost">编辑</a>
          <a v-if="canDeletePost()" class="action-link delete" @click="deletePost">删除</a>
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
              <div class="reply-avatar">{{ reply.author[0] }}</div>
              <div class="reply-user-details">
                <span class="reply-user-name">
                  {{ reply.author }}
                  <span v-if="reply.authorRole === 'teacher'" class="role-badge">老师</span>
                </span>
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
                  <div class="reply-avatar">{{ subReply.author[0] }}</div>
                  <div class="reply-user-details">
                    <span class="reply-user-name">
                      {{ subReply.author }}
                      <span v-if="subReply.authorRole === 'teacher'" class="role-badge">老师</span>
                    </span>
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
  name: 'StudentThreadDetail',
  data() {
    return {
      courseId: this.$route.params.courseId,
      threadId: this.$route.params.threadId,
      thread: {},
      replies: [],
      newReplyContent: '',
      replyingTo: null,
      currentUserId: 1, // 当前学生用户ID
      currentUserRole: 'student' // 当前用户角色
    }
  },
  computed: {
    organizedReplies() {
      // 将回复组织成层级结构
      const topLevel = this.replies.filter(r => !r.parentId)
      
      return topLevel.map(reply => {
        // 找到所有属于这个顶层评论的子回复
        // 包括直接回复和对子回复的回复
        const directChildren = this.replies.filter(r => r.parentId === reply.id)
        const childrenIds = directChildren.map(c => c.id)
        const nestedChildren = this.replies.filter(r => childrenIds.includes(r.parentId))
        
        return {
          ...reply,
          children: [...directChildren, ...nestedChildren]
        }
      })
    }
  },
  created() {
    this.loadThreadData()
  },
  methods: {
    goBack() {
      this.$router.push({
        path: `/student/courses/${this.courseId}`,
        query: { tab: 'discussion' }
      })
    },

    loadThreadData() {
      this.thread = {
        id: this.threadId,
        title: '关于HTML语义化标签的疑问',
        author: '张同学',
        authorId: 1, // 作者ID
        authorRole: 'student',
        createTime: '2024-01-20 10:30',
        views: 45,
        replyCount: 3,
        likeCount: 5,
        isLiked: false,
        content: '老师您好，我在学习HTML语义化标签时遇到了一些疑问。比如article和section标签的使用场景有什么区别？什么时候应该使用article，什么时候使用section？希望老师能够详细解答一下，谢谢！'
      }

      this.replies = [
        {
          id: 1,
          author: '李老师',
          authorRole: 'teacher',
          createTime: '2024-01-20 11:15',
          content: '这是个很好的问题！article标签用于独立的、完整的内容，比如一篇文章、一条评论等。而section标签用于文档中的节，通常包含一个主题。简单来说，article更强调内容的独立性，section更强调内容的组织结构。',
          likeCount: 3,
          isLiked: false,
          parentId: null,
          replyToId: null,
          replyTo: null
        },
        {
          id: 2,
          author: '王同学',
          createTime: '2024-01-20 14:20',
          content: '我也有同样的疑问，老师讲解得很清楚，感谢！',
          replyTo: '李老师',
          replyToId: 1,
          parentId: 1,
          likeCount: 1,
          isLiked: false
        },
        {
          id: 3,
          author: '张同学',
          createTime: '2024-01-20 15:30',
          content: '明白了，谢谢老师的详细解答！',
          replyTo: '李老师',
          replyToId: 1,
          parentId: 1,
          likeCount: 0,
          isLiked: false
        }
      ]
    },

    submitReply() {
      if (!this.newReplyContent.trim()) {
        this.$message.warning('请输入回复内容')
        return
      }

      const newReply = {
        id: Date.now(),
        authorId: this.currentUserId,
        author: '我',
        avatar: 'https://via.placeholder.com/40?text=Me',
        createTime: new Date().toLocaleString(),
        content: this.newReplyContent,
        replyTo: this.replyingTo ? this.replyingTo.author : null,
        replyToId: this.replyingTo ? this.replyingTo.authorId : null,
        parentId: this.replyingTo ? this.replyingTo.replyId : null,
        likeCount: 0,
        isLiked: false
      }

      this.replies.push(newReply)
      this.thread.replyCount++
      this.$message.success('回复成功')
      this.newReplyContent = ''
      this.replyingTo = null
    },

    replyToUser(reply) {
      this.replyingTo = {
        replyId: reply.id,
        authorId: reply.authorId,
        author: reply.author
      }
      this.$nextTick(() => {
        document.querySelector('.reply-textarea').focus()
      })
    },

    cancelReply() {
      this.replyingTo = null
    },

    toggleThreadLike() {
      this.thread.isLiked = !this.thread.isLiked
      this.thread.likeCount += this.thread.isLiked ? 1 : -1
      this.$message.success(this.thread.isLiked ? '已点赞' : '已取消点赞')
    },

    toggleReplyLike(reply) {
      reply.isLiked = !reply.isLiked
      reply.likeCount += reply.isLiked ? 1 : -1
    },
    
    // 权限判断
    canEditPost() {
      // 只能编辑自己的帖子
      return this.thread.authorId === this.currentUserId
    },
    
    canDeletePost() {
      // 学生只能删除自己的帖子
      return this.thread.authorId === this.currentUserId
    },
    
    // 编辑帖子
    editPost() {
      this.$message.info('编辑功能待实现')
      // TODO: 跳转到编辑页面
    },
    
    // 删除帖子
    deletePost() {
      this.$confirm('确定删除这个话题吗？删除后将无法恢复。', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.$message.success('话题已删除')
        // TODO: 调用API删除话题
        this.goBack()
      }).catch(() => {})
    }
  }
}
</script>

<style scoped>
.thread-detail-page {
  min-height: 100vh;
  background: #f9fafb;
  padding-bottom: 2rem;
}

.thread-detail-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1.5rem;
}

.top-bar {
  display: flex;
  align-items: center;
  padding: 1rem 1.5rem;
  background: white;
  border-bottom: 1px solid #e5e7eb;
  margin-bottom: 1rem;
}

.back-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: white;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  color: #374151;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.2s;
}

.back-btn:hover {
  background: #f3f4f6;
  border-color: #9ca3af;
}

.main-post-card {
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  padding: 1.5rem;
  margin: 0 0 1rem 0;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.user-info-row {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #f3f4f6;
}

.user-info {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.user-avatar {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.25rem;
  font-weight: 600;
  flex-shrink: 0;
}

.user-details {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.user-name-row {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.user-name {
  color: #111827;
  font-size: 1rem;
  font-weight: 600;
}

.role-badge {
  padding: 0.25rem 0.75rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  font-size: 0.75rem;
  font-weight: 600;
  border-radius: 12px;
}

.publish-time {
  color: #9ca3af;
  font-size: 0.875rem;
}

.post-content-area {
  margin-bottom: 1.5rem;
}

.post-title {
  margin: 0 0 1rem 0;
  color: #111827;
  font-size: 1.75rem;
  font-weight: 700;
  line-height: 1.4;
}

.post-content {
  color: #374151;
  font-size: 1rem;
  line-height: 1.8;
  white-space: pre-wrap;
}

.post-meta-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 1rem;
  border-top: 1px solid #f3f4f6;
}

.view-stats {
  display: flex;
  gap: 1.5rem;
}

.post-actions {
  display: flex;
  gap: 1rem;
}

.action-link {
  color: #667eea;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  text-decoration: none;
  transition: color 0.2s;
}

.action-link:hover {
  color: #764ba2;
  text-decoration: underline;
}

.action-link.delete {
  color: #ef4444;
}

.action-link.delete:hover {
  color: #dc2626;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #6b7280;
  font-size: 0.875rem;
}

.icon {
  font-style: normal;
}

.like-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 20px;
  color: #6b7280;
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.2s;
}

.like-btn:hover {
  background: #fef3c7;
  border-color: #fbbf24;
}

.like-btn.liked {
  background: #fee2e2;
  border-color: #fca5a5;
  color: #991b1b;
}

.replies-section {
  margin: 0 0 120px 0;
}

.replies-header {
  background: #f3f4f6;
  padding: 0.75rem 1.5rem;
  border-radius: 8px 8px 0 0;
  border: 1px solid #e5e7eb;
  border-bottom: none;
}

.replies-count {
  color: #6b7280;
  font-size: 0.9rem;
  font-weight: 500;
}

.replies-list {
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 0 0 8px 8px;
}

.reply-card {
  padding: 1.25rem;
  border-bottom: 1px solid #f3f4f6;
}

.reply-card:last-child {
  border-bottom: none;
}

.reply-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.75rem;
}

.reply-user-info {
  display: flex;
  gap: 0.75rem;
  align-items: center;
}

.reply-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1rem;
  font-weight: 600;
  flex-shrink: 0;
}

.reply-user-details {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.reply-user-name {
  color: #374151;
  font-size: 0.9rem;
  font-weight: 600;
}

.reply-time {
  color: #9ca3af;
  font-size: 0.8rem;
}

.reply-meta {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.reply-to-link {
  color: #667eea;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  text-decoration: none;
  transition: color 0.2s;
}

.reply-to-link:hover {
  color: #764ba2;
  text-decoration: underline;
}

.reply-content {
  color: #374151;
  font-size: 0.95rem;
  line-height: 1.6;
  white-space: pre-wrap;
  margin-bottom: 0.75rem;
}

.reply-to-tag {
  color: #667eea;
  font-weight: 600;
  margin-right: 0.5rem;
}

.reply-actions-row {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.like-btn-small {
  display: flex;
  align-items: center;
  gap: 0.35rem;
  padding: 0.35rem 0.75rem;
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 16px;
  color: #6b7280;
  font-size: 0.8rem;
  cursor: pointer;
  transition: all 0.2s;
}

.like-btn-small:hover {
  background: #fef3c7;
  border-color: #fbbf24;
}

.like-btn-small.liked {
  background: #fee2e2;
  border-color: #fca5a5;
  color: #991b1b;
}

/* 子回复区域 */
.sub-replies {
  margin-top: 1rem;
  margin-left: 2.5rem;
  padding-left: 1rem;
  border-left: 2px solid #e5e7eb;
}

.sub-reply-card {
  padding: 1rem 0;
  border-bottom: 1px solid #f3f4f6;
}

.sub-reply-card:last-child {
  border-bottom: none;
}

.no-replies {
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 0 0 8px 8px;
  padding: 3rem;
  text-align: center;
}

.no-replies p {
  margin: 0;
  color: #9ca3af;
  font-size: 0.95rem;
}

.reply-input-section {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: white;
  border-top: 2px solid #e5e7eb;
  box-shadow: 0 -4px 12px rgba(0, 0, 0, 0.08);
  z-index: 40;
  padding: 1rem 1.5rem;
}

.reply-input-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1.5rem;
}

.replying-to-banner {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem 0.75rem;
  background: #eff6ff;
  border: 1px solid #dbeafe;
  border-radius: 6px 6px 0 0;
  color: #1e40af;
  font-size: 0.875rem;
  margin-bottom: -1px;
}

.cancel-reply-btn {
  background: transparent;
  border: none;
  color: #6b7280;
  font-size: 1.25rem;
  cursor: pointer;
  padding: 0;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 4px;
  transition: all 0.2s;
}

.cancel-reply-btn:hover {
  background: #e5e7eb;
  color: #111827;
}

.reply-textarea {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  font-size: 0.9375rem;
  font-family: inherit;
  line-height: 1.5;
  resize: vertical;
  transition: border-color 0.2s;
  box-sizing: border-box;
}

.reply-textarea:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.submit-reply-btn {
  margin-top: 0.75rem;
  padding: 0.6rem 1.5rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 0.9375rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.submit-reply-btn:hover {
  opacity: 0.9;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}
</style>
