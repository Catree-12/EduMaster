<template>
  <div class="thread-detail-page">
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
        <div v-if="canManagePost" class="post-actions">
          <a class="action-link edit" @click="editPost">编辑</a>
          <a class="action-link delete" @click="deletePost">删除</a>
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
          v-for="reply in replies" 
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
            <div class="reply-meta">
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
</template>

<script>
export default {
  name: 'CommunityThreadDetail',
  data() {
    return {
      threadId: null,
      currentUserId: 1, // 模拟当前用户ID
      currentUserRole: 'teacher', // 当前用户角色
      newReplyContent: '',
      replyingTo: null, // 正在回复的用户对象
      thread: {
        id: 1,
        authorId: 1,
        author: '张三',
        authorRole: 'teacher',
        avatar: 'https://via.placeholder.com/50?text=Teacher1',
        title: '关于原型链的理解',
        content: '请问原型链和原型对象有什么区别？能否用代码示例说明？这是一个关于JavaScript基础的问题，希望老师能详细解答一下，最好能配合代码示例。\n\n我在学习过程中发现很多资料对这两个概念的解释都比较模糊，希望能得到更清晰的讲解。',
        createTime: '2024-01-20 14:30',
        viewCount: 120,
        likeCount: 15,
        isLiked: false
      },
      replies: [
        {
          id: 1,
          authorId: 2,
          author: '李老师',
          avatar: 'https://via.placeholder.com/40?text=Teacher2',
          content: '原型链是JavaScript实现继承的主要方式。简单来说，每个对象都有一个__proto__属性指向其原型对象，而原型对象也可能有自己的原型，这样一层层连接起来就形成了原型链。',
          createTime: '2024-01-20 15:10',
          replyTo: null,
          likeCount: 8,
          isLiked: false
        },
        {
          id: 2,
          authorId: 3,
          author: '王同学',
          avatar: 'https://via.placeholder.com/40?text=Student1',
          content: '谢谢李老师的解答！能否再举个具体的代码例子吗？',
          createTime: '2024-01-20 15:30',
          replyTo: '李老师',
          likeCount: 3,
          isLiked: false
        },
        {
          id: 3,
          authorId: 1,
          author: '张三',
          avatar: 'https://via.placeholder.com/40?text=Teacher1',
          content: '感谢李老师的解答，我现在理解了！',
          createTime: '2024-01-20 16:00',
          replyTo: '李老师',
          likeCount: 5,
          isLiked: false
        }
      ]
    }
  },
  computed: {
    canManagePost() {
      // 作者本人或老师可以管理主贴
      return this.thread.authorId === this.currentUserId || this.currentUserRole === 'teacher'
    }
  },
  mounted() {
    this.threadId = this.$route.params.id || this.$route.query.id
    // TODO: 根据threadId加载数据
    this.loadThreadDetail()
  },
  methods: {
    goBack() {
      this.$router.back()
    },
    loadThreadDetail() {
      // TODO: 从API加载话题详情和回复列表
      console.log('加载话题详情:', this.threadId)
    },
    canDeleteReply(reply) {
      // 回复作者本人或老师可以删除回复
      return reply.authorId === this.currentUserId || this.currentUserRole === 'teacher'
    },
    replyToUser(reply) {
      // 设置正在回复的用户
      this.replyingTo = {
        id: reply.authorId,
        author: reply.author
      }
      // 聚焦到输入框
      this.$nextTick(() => {
        const textarea = this.$el.querySelector('.reply-textarea')
        if (textarea) {
          textarea.focus()
          // 滚动到输入框位置
          textarea.scrollIntoView({ behavior: 'smooth', block: 'center' })
        }
      })
    },
    cancelReply() {
      this.replyingTo = null
    },
    editPost() {
      // 跳转到编辑页面
      this.$router.push({
        name: 'CommunityThreadEdit',
        params: {
          courseId: this.$route.params.courseId,
          id: this.threadId
        }
      })
    },
    deletePost() {
      if (confirm('确定删除这个话题吗？删除后将无法恢复。')) {
        this.$message.success('话题已删除')
        // TODO: 调用API删除话题
        this.$router.back()
      }
    },
    deleteReply(replyId) {
      if (confirm('确定删除这条回复吗？')) {
        this.replies = this.replies.filter(r => r.id !== replyId)
        this.$message.success('回复已删除')
        // TODO: 调用API删除回复
      }
    },
    // 切换帖子点赞状态
    toggleThreadLike() {
      this.thread.isLiked = !this.thread.isLiked
      if (this.thread.isLiked) {
        this.thread.likeCount++
        // TODO: 调用点赞API
        // this.$api.likeThread(this.thread.id)
      } else {
        this.thread.likeCount--
        // TODO: 调用取消点赞API
        // this.$api.unlikeThread(this.thread.id)
      }
    },
    // 切换评论点赞状态
    toggleReplyLike(reply) {
      reply.isLiked = !reply.isLiked
      if (reply.isLiked) {
        reply.likeCount++
        // TODO: 调用点赞API
        // this.$api.likeReply(reply.id)
      } else {
        reply.likeCount--
        // TODO: 调用取消点赞API
        // this.$api.unlikeReply(reply.id)
      }
    },
    submitReply() {
      if (!this.newReplyContent.trim()) {
        this.$message.error('请输入回复内容')
        return
      }

      const newReply = {
        id: Math.max(...this.replies.map(r => r.id), 0) + 1,
        authorId: this.currentUserId,
        author: '当前用户',
        avatar: 'https://via.placeholder.com/40?text=Me',
        content: this.newReplyContent,
        createTime: new Date().toLocaleString('zh-CN'),
        replyTo: this.replyingTo ? this.replyingTo.author : null
      }

      this.replies.push(newReply)
      this.newReplyContent = ''
      this.replyingTo = null
      this.$message.success('回复成功')
      
      // TODO: 调用API提交回复
    }
  }
}
</script>

<style scoped>
.thread-detail-page {
  min-height: 100vh;
  background: #f9fafb;
  padding-bottom: 2rem;
  margin-left: 220px;
  margin-top: 70px;
}

/* 1. 顶部返回层 */
.top-bar {
  display: flex;
  align-items: center;
  padding: 0.5rem 1rem;
  background: white;
  border-bottom: 1px solid #e5e7eb;
  position: sticky;
  top: 70px;
  z-index: 50;
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

/* 2. 楼主发帖区（主贴卡片） */
.main-post-card {
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  padding: 1.5rem;
  margin: 0.5rem 1rem 1rem 1rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

/* 用户信息行 */
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
  object-fit: cover;
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

/* 话题正文区 */
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

/* 互动统计与管理 */
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

/* 3. 回复统计与列表区 */
.replies-section {
  margin: 0 1rem 90px 1rem;
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
  object-fit: cover;
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

.delete-link {
  color: #ef4444;
  font-size: 0.875rem;
  cursor: pointer;
  text-decoration: none;
  transition: color 0.2s;
}

.delete-link:hover {
  color: #dc2626;
  text-decoration: underline;
}

.reply-content {
  color: #374151;
  font-size: 0.95rem;
  line-height: 1.6;
  white-space: pre-wrap;
}

.reply-to-tag {
  color: #667eea;
  font-weight: 600;
  margin-right: 0.5rem;
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

/* 4. 底部快捷回复区 */
.reply-input-section {
  position: fixed;
  bottom: 0;
  left: 220px;
  right: 0;
  background: white;
  border-top: 2px solid #e5e7eb;
  box-shadow: 0 -4px 12px rgba(0, 0, 0, 0.08);
  z-index: 40;
  padding: 0.5rem 1rem;
}

.reply-input-container {
  margin: 0;
  padding: 0 0.5rem;
}

.replying-to-banner {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.4rem 0.75rem;
  background: #eff6ff;
  border: 1px solid #dbeafe;
  border-radius: 6px 6px 0 0;
  color: #1e40af;
  font-size: 0.8rem;
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
  padding: 0.5rem 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  font-size: 0.875rem;
  font-family: inherit;
  line-height: 1.4;
  resize: vertical;
  transition: border-color 0.2s;
}

.reply-textarea:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.submit-reply-btn {
  margin-top: 0.5rem;
  padding: 0.4rem 1.25rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 0.85rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  float: right;
}

.submit-reply-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 16px rgba(102, 126, 234, 0.3);
}

.submit-reply-btn:active {
  transform: translateY(0);
}

/* 点赞按钮样式 */
.like-btn {
  background: transparent;
  border: 1px solid #e5e7eb;
  padding: 0.375rem 0.875rem;
  border-radius: 6px;
  font-size: 0.875rem;
  color: #6b7280;
  cursor: pointer;
  transition: all 0.2s;
  display: inline-flex;
  align-items: center;
  gap: 0.375rem;
}

.like-btn:hover {
  border-color: #ff6b6b;
  color: #ff6b6b;
  background: #fff5f5;
}

.like-btn.liked {
  border-color: #ff6b6b;
  color: #ff6b6b;
  background: #fff5f5;
}

.reply-actions-row {
  margin-top: 0.5rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.like-btn-small {
  background: transparent;
  border: 1px solid #e5e7eb;
  padding: 0.25rem 0.625rem;
  border-radius: 4px;
  font-size: 0.8125rem;
  color: #6b7280;
  cursor: pointer;
  transition: all 0.2s;
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
}

.like-btn-small:hover {
  border-color: #ff6b6b;
  color: #ff6b6b;
  background: #fff5f5;
}

.like-btn-small.liked {
  border-color: #ff6b6b;
  color: #ff6b6b;
  background: #fff5f5;
}

/* 响应式 */
@media (max-width: 768px) {
  .thread-detail-page {
    margin-left: 0;
  }

  .reply-input-section {
    left: 0;
    padding: 1rem;
  }

  .main-post-card,
  .replies-section {
    margin-left: 1rem;
    margin-right: 1rem;
  }

  .main-post-card,
  .reply-input-container {
    padding: 1.5rem;
  }

  .post-title {
    font-size: 1.5rem;
  }
}
</style>
