<template>
  <div class="course-community">
    <div class="community-header">
      <router-link :to="`/course/${courseId}`" class="back-link">← 返回课程</router-link>
      <h1>{{ courseName }} - 课程讨论</h1>
    </div>

    <div class="community-container">
      <button @click="showReplyModal = true" class="post-btn">
        📝 提问或讨论
      </button>

      <div class="tabs">
        <button 
          v-for="tab in ['全部', '未解答', '精华']" 
          :key="tab"
          :class="{ active: activeTab === tab }"
          @click="activeTab = tab"
          class="tab-btn"
        >
          {{ tab }}
        </button>
      </div>

      <div v-if="threads.length > 0" class="threads-list">
        <div v-for="thread in threads" :key="thread.id" class="thread-card">
          <div class="thread-header">
            <h3>{{ thread.title }}</h3>
            <span v-if="thread.solved" class="solved-badge">✓ 已解答</span>
          </div>

          <p class="thread-preview">{{ thread.content }}</p>

          <div class="thread-meta">
            <span>👤 {{ thread.author }}</span>
            <span>💬 {{ thread.replyCount }} 回复</span>
            <span v-if="thread.bestReply">⭐ 最佳答案</span>
          </div>

          <button @click="viewThread(thread.id)" class="view-btn">
            查看讨论 →
          </button>
        </div>
      </div>

      <div v-else class="no-threads">
        <p>暂无讨论，快来<button @click="showReplyModal = true" class="link-btn">提出第一个问题</button></p>
      </div>
    </div>

    <!-- 提问模态框 -->
    <div v-if="showReplyModal" class="modal-overlay" @click="showReplyModal = false">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h2>在课程中提问</h2>
          <button @click="showReplyModal = false" class="close-btn">✕</button>
        </div>

        <form @submit.prevent="submitQuestion" class="question-form">
          <div class="form-group">
            <label for="title">问题标题</label>
            <input 
              v-model="newQuestion.title" 
              type="text" 
              id="title"
              placeholder="请输入问题标题"
              required
            >
          </div>

          <div class="form-group">
            <label for="content">问题描述</label>
            <textarea 
              v-model="newQuestion.content" 
              id="content"
              placeholder="请详细描述你的问题"
              rows="6"
              required
            ></textarea>
          </div>

          <div class="form-actions">
            <button type="submit" class="submit-btn" :disabled="submitting">
              {{ submitting ? '提交中...' : '提交问题' }}
            </button>
            <button type="button" @click="showReplyModal = false" class="cancel-btn">
              取消
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'UserCourseCommunity',
  data() {
    return {
      courseId: this.$route.params.id,
      courseName: 'Vue.js 从入门到精通',
      activeTab: '全部',
      showReplyModal: false,
      submitting: false,
      newQuestion: {
        title: '',
        content: ''
      },
      threads: [
        {
          id: 1,
          title: 'v-if 和 v-show 的区别是什么？',
          content: '在学习 Vue 指令时，经常看到 v-if 和 v-show，想了解它们之间的区别和使用场景...',
          author: '小王',
          replyCount: 5,
          solved: true,
          bestReply: true
        },
        {
          id: 2,
          title: '如何优化 Vue 组件的渲染性能？',
          content: '在项目中遇到了性能问题，想知道有哪些优化 Vue 组件渲染的方法...',
          author: '李明',
          replyCount: 8,
          solved: true,
          bestReply: false
        },
        {
          id: 3,
          title: 'computed 和 methods 有什么区别？',
          content: '这两个都可以实现功能，但不太明白什么时候用哪个...',
          author: '张三',
          replyCount: 3,
          solved: false,
          bestReply: false
        }
      ]
    }
  },
  methods: {
    viewThread(threadId) {
      this.$router.push(`/course/${this.courseId}/community/thread/${threadId}`)
    },
    async submitQuestion() {
      if (!this.newQuestion.title || !this.newQuestion.content) {
        this.$message.error('请填写问题标题和描述')
        return
      }

      this.submitting = true
      try {
        // TODO: 调用提交问题 API
        this.$message.success('问题已提交')
        this.showReplyModal = false
        this.newQuestion = { title: '', content: '' }
      } catch (error) {
        this.$message.error('提交失败：' + error.message)
      } finally {
        this.submitting = false
      }
    }
  }
}
</script>

<style scoped>
.course-community {
  width: 100%;
}

.community-header {
  margin-bottom: 2rem;
}

.back-link {
  display: inline-block;
  color: #667eea;
  text-decoration: none;
  margin-bottom: 1rem;
  transition: color 0.3s;
}

.back-link:hover {
  color: #764ba2;
}

.community-header h1 {
  color: #2c3e50;
  margin: 0;
  font-size: 1.75rem;
}

.community-container {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.post-btn {
  width: 100%;
  padding: 0.75rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 600;
  margin-bottom: 1.5rem;
  transition: opacity 0.3s;
}

.post-btn:hover {
  opacity: 0.9;
}

.tabs {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
  border-bottom: 1px solid #ecf0f1;
}

.tab-btn {
  padding: 0.75rem 1.5rem;
  background: none;
  border: none;
  color: #7f8c8d;
  cursor: pointer;
  border-bottom: 3px solid transparent;
  transition: all 0.3s;
}

.tab-btn.active {
  color: #667eea;
  border-bottom-color: #667eea;
}

.threads-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.thread-card {
  padding: 1.5rem;
  border: 1px solid #ecf0f1;
  border-radius: 8px;
  transition: all 0.3s;
}

.thread-card:hover {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.thread-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 0.75rem;
}

.thread-header h3 {
  margin: 0;
  color: #2c3e50;
  flex: 1;
}

.solved-badge {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  background-color: #d5f4e6;
  color: #27ae60;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 600;
  white-space: nowrap;
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

.thread-meta {
  display: flex;
  gap: 1.5rem;
  font-size: 0.875rem;
  color: #95a5a6;
  margin-bottom: 1rem;
}

.view-btn {
  padding: 0.5rem 1rem;
  background-color: #ecf0f1;
  color: #2c3e50;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s;
}

.view-btn:hover {
  background-color: #d5dbdb;
}

.no-threads {
  text-align: center;
  padding: 3rem;
  color: #7f8c8d;
}

.link-btn {
  background: none;
  border: none;
  color: #667eea;
  cursor: pointer;
  font-weight: 600;
}

.link-btn:hover {
  text-decoration: underline;
}

/* 模态框样式 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 8px;
  max-width: 600px;
  width: 90%;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid #ecf0f1;
}

.modal-header h2 {
  margin: 0;
  color: #2c3e50;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #7f8c8d;
}

.question-form {
  padding: 1.5rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  color: #2c3e50;
  font-weight: 500;
}

.form-group input,
.form-group textarea {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #bdc3c7;
  border-radius: 4px;
  font-size: 1rem;
  font-family: inherit;
  box-sizing: border-box;
}

.form-group input:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.form-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
}

.submit-btn,
.cancel-btn {
  padding: 0.75rem 1.5rem;
  border-radius: 4px;
  border: none;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s;
}

.submit-btn {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.submit-btn:hover:not(:disabled) {
  opacity: 0.9;
}

.submit-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.cancel-btn {
  background-color: #ecf0f1;
  color: #2c3e50;
}

.cancel-btn:hover {
  background-color: #d5dbdb;
}
</style>
