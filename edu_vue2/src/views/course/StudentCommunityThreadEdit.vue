<template>
  <div class="thread-edit-page">
    <!-- 顶部导航层 -->
    <div class="top-nav">
      <button class="back-btn" @click="goBack">
        <span class="back-icon">←</span>
      </button>
      <h1 class="page-title">编辑话题</h1>
    </div>

    <!-- 编辑主卡片 -->
    <div class="edit-card">
      <form @submit.prevent="saveChanges">
        <!-- 话题标题输入框 -->
        <div class="form-group">
          <label class="form-label">话题标题</label>
          <input 
            v-model="formData.title" 
            type="text" 
            class="title-input"
            placeholder="请输入话题标题"
            maxlength="100"
            required
          />
          <div class="char-count">{{ formData.title.length }}/100</div>
        </div>

        <!-- 话题内容编辑区 -->
        <div class="form-group">
          <label class="form-label">话题内容</label>
          <textarea 
            v-model="formData.content" 
            class="content-textarea"
            placeholder="请详细描述你的问题或想法..."
            rows="12"
            required
          ></textarea>
          <div class="char-count">{{ formData.content.length }} 字</div>
        </div>

        <!-- 底部操作栏 -->
        <div class="bottom-actions">
          <button type="button" class="cancel-btn" @click="goBack">
            取消
          </button>
          <button type="submit" class="save-btn">
            保存修改
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  name: 'StudentCommunityThreadEdit',
  data() {
    return {
      threadId: null,
      courseId: null,
      formData: {
        title: '',
        content: ''
      },
      originalData: null
    }
  },
  mounted() {
    this.threadId = this.$route.params.threadId || this.$route.query.threadId
    this.courseId = this.$route.params.courseId || this.$route.query.courseId
    this.loadThreadData()
  },
  methods: {
    loadThreadData() {
      // TODO: 从API加载话题数据
      console.log('加载话题数据:', this.threadId)
      
      // 模拟数据
      const mockData = {
        title: '关于CSS Grid布局的疑问',
        content: '在学习CSS Grid的时候遇到了一些问题，想请教一下大家...'
      }
      
      this.formData = { ...mockData }
      this.originalData = { ...mockData }
    },
    goBack() {
      if (this.hasChanges()) {
        if (confirm('你有未保存的修改，确定要放弃吗？')) {
          this.$router.back()
        }
      } else {
        this.$router.back()
      }
    },
    hasChanges() {
      if (!this.originalData) return false
      return this.formData.title !== this.originalData.title ||
             this.formData.content !== this.originalData.content
    },
    saveChanges() {
      if (!this.formData.title.trim()) {
        this.$message.error('请输入话题标题')
        return
      }
      if (!this.formData.content.trim()) {
        this.$message.error('请输入话题内容')
        return
      }

      // TODO: 调用API保存数据
      console.log('保存话题数据:', this.formData)
      this.$message.success('话题已更新')
      
      // 返回详情页
      this.$router.push({
        path: `/student/course/${this.courseId}/thread/${this.threadId}`
      })
    }
  }
}
</script>

<style scoped lang="scss">
.thread-edit-page {
  min-height: 100vh;
  background: #f9fafb;
  padding: 1rem 2rem 3rem;
}

/* ========== 顶部导航层 ========== */
.top-nav {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.back-btn {
  background: white;
  border: 1px solid #e5e7eb;
  width: 40px;
  height: 40px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s;
}

.back-btn:hover {
  border-color: #667eea;
  background: #f5f7ff;
}

.back-icon {
  font-size: 1.5rem;
  font-weight: 700;
  color: #374151;
}

.page-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #111827;
  margin: 0;
}

/* ========== 编辑主卡片 ========== */
.edit-card {
  max-width: 1100px;
  margin: 0 auto;
  background: white;
  border-radius: 12px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  padding: 2rem 2.5rem;
}

/* ========== 表单元素 ========== */
.form-group {
  margin-bottom: 1.75rem;
  position: relative;
}

.form-label {
  display: block;
  font-size: 0.9375rem;
  font-weight: 600;
  color: #374151;
  margin-bottom: 0.625rem;
}

.title-input {
  width: 100%;
  padding: 0.875rem 1rem;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  font-size: 1rem;
  color: #111827;
  transition: all 0.2s;
  font-family: inherit;
}

.title-input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.title-input::placeholder {
  color: #9ca3af;
}

.content-textarea {
  width: 100%;
  padding: 1rem;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  font-size: 0.9375rem;
  color: #111827;
  line-height: 1.6;
  resize: vertical;
  min-height: 300px;
  font-family: inherit;
  transition: all 0.2s;
}

.content-textarea:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.content-textarea::placeholder {
  color: #9ca3af;
}

.char-count {
  position: absolute;
  right: 0.5rem;
  bottom: -1.5rem;
  font-size: 0.8125rem;
  color: #9ca3af;
}

/* ========== 底部操作栏 ========== */
.bottom-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 2.5rem;
  padding-top: 2rem;
  border-top: 1px solid #e5e7eb;
}

.cancel-btn {
  padding: 0.75rem 2rem;
  background: white;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  font-size: 0.9375rem;
  font-weight: 600;
  color: #6b7280;
  cursor: pointer;
  transition: all 0.2s;
}

.cancel-btn:hover {
  border-color: #9ca3af;
  background: #f9fafb;
  color: #374151;
}

.save-btn {
  padding: 0.75rem 2.5rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  border-radius: 8px;
  font-size: 0.9375rem;
  font-weight: 600;
  color: white;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

.save-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
}

.save-btn:active {
  transform: translateY(0);
}

/* ========== 响应式设计 ========== */
@media (max-width: 768px) {
  .thread-edit-page {
    padding: 1rem;
  }

  .edit-card {
    padding: 1.5rem;
  }

  .page-title {
    font-size: 1.25rem;
  }

  .bottom-actions {
    flex-direction: column;
  }

  .cancel-btn,
  .save-btn {
    width: 100%;
  }
}
</style>
