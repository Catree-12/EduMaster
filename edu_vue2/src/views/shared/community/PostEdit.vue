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
  name: 'CommunityPostEdit',
  data() {
    return {
      postId: null,
      formData: {
        title: '',
        content: ''
      },
      originalData: null
    }
  },
  mounted() {
    this.postId = this.$route.params.id
    this.loadPostData()
  },
  methods: {
    loadPostData() {
      // TODO: 从API加载话题数据
      console.log('加载话题数据:', this.postId)
      
      // 模拟数据
      const mockData = {
        title: '关于前端技术的讨论',
        content: '这是一个关于前端技术的讨论话题...'
      }
      
      this.formData = { ...mockData }
      this.originalData = { ...mockData }
    },
    goBack() {
      if (this.hasChanges()) {
        if (confirm('你有未保存的修改，确定要放弃吗？')) {
          this.$router.push(`/community/posts/${this.postId}`)
        }
      } else {
        this.$router.push(`/community/posts/${this.postId}`)
      }
    },
    hasChanges() {
      if (!this.originalData) return false
      return this.formData.title !== this.originalData.title ||
             this.formData.content !== this.originalData.content
    },
    async saveChanges() {
      if (!this.formData.title.trim()) {
        alert('请输入话题标题')
        return
      }
      if (!this.formData.content.trim()) {
        alert('请输入话题内容')
        return
      }

      try {
        // TODO: 调用API保存修改
        console.log('保存话题修改:', {
          postId: this.postId,
          ...this.formData
        })

        alert('保存成功！')
        this.$router.push(`/community/posts/${this.postId}`)
      } catch (error) {
        console.error('保存失败:', error)
        alert('保存失败，请重试')
      }
    }
  }
}
</script>

<style scoped>
.thread-edit-page {
  max-width: 900px;
  margin: 0 auto;
  padding: 20px;
}

.top-nav {
  display: flex;
  align-items: center;
  margin-bottom: 24px;
}

.back-btn {
  background: none;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  color: #606266;
  font-size: 16px;
  padding: 8px 12px;
  border-radius: 4px;
  transition: all 0.3s;
}

.back-btn:hover {
  background-color: #f5f7fa;
  color: #409eff;
}

.back-icon {
  font-size: 20px;
}

.page-title {
  margin: 0 0 0 16px;
  font-size: 24px;
  font-weight: 600;
  color: #303133;
}

.edit-card {
  background: white;
  border-radius: 8px;
  padding: 32px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
}

.form-group {
  margin-bottom: 24px;
  position: relative;
}

.form-label {
  display: block;
  margin-bottom: 8px;
  font-size: 14px;
  font-weight: 500;
  color: #303133;
}

.title-input {
  width: 100%;
  padding: 12px 16px;
  font-size: 16px;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  transition: border-color 0.3s;
  box-sizing: border-box;
}

.title-input:focus {
  outline: none;
  border-color: #409eff;
}

.content-textarea {
  width: 100%;
  padding: 12px 16px;
  font-size: 14px;
  line-height: 1.8;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  resize: vertical;
  font-family: inherit;
  transition: border-color 0.3s;
  box-sizing: border-box;
}

.content-textarea:focus {
  outline: none;
  border-color: #409eff;
}

.char-count {
  position: absolute;
  right: 12px;
  bottom: -20px;
  font-size: 12px;
  color: #909399;
}

.bottom-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 32px;
  padding-top: 24px;
  border-top: 1px solid #ebeef5;
}

.cancel-btn,
.save-btn {
  padding: 10px 24px;
  font-size: 14px;
  border-radius: 4px;
  cursor: pointer;
  border: none;
  transition: all 0.3s;
}

.cancel-btn {
  background-color: #f5f7fa;
  color: #606266;
}

.cancel-btn:hover {
  background-color: #e4e7ed;
}

.save-btn {
  background-color: #409eff;
  color: white;
}

.save-btn:hover {
  background-color: #66b1ff;
}

@media (max-width: 768px) {
  .thread-edit-page {
    padding: 12px;
  }

  .edit-card {
    padding: 20px;
  }

  .page-title {
    font-size: 20px;
  }
}
</style>
