<template>
  <div class="new-post-container">
    <div class="back-bar">
      <button @click="$router.back()" class="back-btn">← 返回</button>
    </div>

    <div class="new-post-card">
      <h1>发表新话题</h1>
      
      <form @submit.prevent="handleSubmit">
        <div class="form-group">
          <label>话题分类 *</label>
          <select v-model="form.category" required>
            <option value="">请选择分类</option>
            <option value="question">问答</option>
            <option value="share">分享</option>
            <option value="suggestion">建议</option>
            <option value="announcement">公告</option>
          </select>
        </div>

        <div class="form-group">
          <label>话题标题 *</label>
          <input v-model="form.title" type="text" placeholder="输入话题标题" required>
        </div>

        <div class="form-group">
          <label>话题内容 *</label>
          <textarea v-model="form.content" placeholder="输入话题内容（支持 Markdown）" rows="10" required></textarea>
        </div>

        <div class="form-group">
          <label>标签</label>
          <input v-model="tagInput" type="text" placeholder="输入标签，按 Enter 添加">
          <div class="tags">
            <span v-for="(tag, index) in form.tags" :key="index" class="tag">
              {{ tag }}
              <button type="button" @click="removeTag(index)" class="btn-remove-tag">×</button>
            </span>
          </div>
        </div>

        <div class="form-actions">
          <button type="button" class="btn-cancel" @click="$router.back()">取消</button>
          <button type="button" class="btn-draft" @click="saveDraft">保存草稿</button>
          <button type="submit" class="btn-submit">发表话题</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  name: 'NewPostPage',
  data() {
    return {
      tagInput: '',
      form: {
        category: '',
        title: '',
        content: '',
        tags: []
      }
    }
  },
  methods: {
    handleKeyUp(event) {
      if (event.key === 'Enter' && this.tagInput.trim()) {
        this.form.tags.push(this.tagInput.trim())
        this.tagInput = ''
      }
    },
    removeTag(index) {
      this.form.tags.splice(index, 1)
    },
    saveDraft() {
      this.$message.success('话题已保存为草稿')
    },
    handleSubmit() {
      if (!this.form.category || !this.form.title || !this.form.content) {
        this.$message.error('请填写所有必填字段')
        return
      }
      this.$message.success('话题发表成功！')
      this.$router.push('/community')
    }
  },
  mounted() {
    const input = this.$el.querySelector('input[placeholder="输入标签"]')
    if (input) {
      input.addEventListener('keyup', this.handleKeyUp)
    }
  }
}
</script>

<style scoped>
.new-post-container {
  padding: 30px;
  background: #f5f5f5;
  max-width: 900px;
  margin: 0 auto;
}

.back-bar {
  margin-bottom: 20px;
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

.new-post-card {
  background: white;
  padding: 40px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

h1 {
  margin-top: 0;
  margin-bottom: 30px;
  font-size: 28px;
  color: #333;
}

.form-group {
  margin-bottom: 25px;
}

.form-group label {
  display: block;
  margin-bottom: 10px;
  color: #555;
  font-weight: 600;
}

.form-group input,
.form-group textarea,
.form-group select {
  width: 100%;
  padding: 12px 15px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 14px;
  font-family: inherit;
  transition: border-color 0.3s;
  box-sizing: border-box;
}

.form-group input:focus,
.form-group textarea:focus,
.form-group select:focus {
  outline: none;
  border-color: #667eea;
}

.tags {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 10px;
}

.tag {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: #f0f0f0;
  padding: 6px 12px;
  border-radius: 12px;
  font-size: 12px;
  color: #667eea;
  font-weight: 600;
}

.btn-remove-tag {
  background: none;
  border: none;
  color: #999;
  cursor: pointer;
  font-size: 16px;
  padding: 0;
  transition: color 0.3s;
}

.btn-remove-tag:hover {
  color: #667eea;
}

.form-actions {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
  margin-top: 30px;
  padding-top: 20px;
  border-top: 1px solid #eee;
}

.btn-cancel,
.btn-draft,
.btn-submit {
  padding: 12px 30px;
  border: none;
  border-radius: 6px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-cancel {
  background: #f0f0f0;
  color: #333;
}

.btn-cancel:hover {
  background: #e0e0e0;
}

.btn-draft {
  background: #f9f9f9;
  color: #667eea;
  border: 2px solid #667eea;
}

.btn-draft:hover {
  background: #f0f0f0;
}

.btn-submit {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.btn-submit:hover {
  opacity: 0.9;
}
</style>
