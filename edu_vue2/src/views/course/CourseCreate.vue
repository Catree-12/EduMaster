<template>
  <div class="course-create-container">
    <div class="page-header">
      <el-button icon="el-icon-arrow-left" circle @click="goBack"></el-button>
      <div class="header-content">
        <h1 class="page-title">创建新课程</h1>
        <p class="page-subtitle">填写课程基本信息，开启教学之旅</p>
      </div>
    </div>

    <div class="create-form-wrapper">
      <div class="form-layout">
        <!-- 左侧表单 -->
        <div class="form-card">
          <el-form
            ref="courseForm"
            :model="courseForm"
            :rules="rules"
            label-width="100px"
            size="medium"
          >
            <!-- 课程基本信息 -->
            <div class="form-section">
              <div class="section-header">
                <i class="el-icon-document section-icon"></i>
                <h3 class="section-title">基本信息</h3>
              </div>
              
              <el-form-item label="课程名称" prop="title">
                <el-input
                  v-model="courseForm.title"
                  placeholder="请输入课程名称"
                  maxlength="100"
                  show-word-limit
                />
              </el-form-item>

              <el-form-item label="课程分类" prop="categories">
                <el-select 
                  v-model="courseForm.categories" 
                  multiple 
                  placeholder="请选择分类（可多选）" 
                  style="width: 100%;"
                  collapse-tags
                >
                  <el-option label="计算机" value="计算机" />
                  <el-option label="经济学" value="经济学" />
                  <el-option label="农林园艺" value="农林园艺" />
                  <el-option label="医药卫生" value="医药卫生" />
                  <el-option label="理学" value="理学" />
                  <el-option label="历史" value="历史" />
                  <el-option label="哲学" value="哲学" />
                  <el-option label="法学" value="法学" />
                  <el-option label="文学文化" value="文学文化" />
                  <el-option label="艺术设计" value="艺术设计" />
                  <el-option label="外语" value="外语" />
                  <el-option label="教育教学" value="教育教学" />
                  <el-option label="管理学" value="管理学" />
                  <el-option label="工学" value="工学" />
                  <el-option label="其他" value="其他" />
                </el-select>
              </el-form-item>

              <el-form-item label="课程描述">
                <el-input
                  v-model="courseForm.description"
                  type="textarea"
                  rows="6"
                  placeholder="请输入课程描述（选填）"
                  maxlength="500"
                  show-word-limit
                />
              </el-form-item>

              <el-form-item label="课程封面">
                <el-upload
                  ref="coverUpload"
                  action="/api/upload/image"
                  :file-list="fileList"
                  :on-success="handleUploadSuccess"
                  :on-error="handleUploadError"
                  :show-file-list="false"
                  limit="1"
                  accept="image/*"
                >
                  <el-button size="small" icon="el-icon-upload">
                    {{ courseForm.coverImage ? '更换封面' : '上传封面' }}
                  </el-button>
                  <div slot="tip" class="el-upload__tip">
                    建议尺寸: 800x600px，支持jpg/png格式
                  </div>
                </el-upload>
              </el-form-item>
            </div>

            <!-- 提交按钮 -->
            <div class="form-actions">
              <el-button size="large" @click="goBack">
                取消
              </el-button>
              <el-button type="primary" size="large" :loading="submitting" @click="createCourse">
                {{ submitting ? '创建中...' : '创建课程' }}
              </el-button>
            </div>
          </el-form>
        </div>

        <!-- 右侧预览 -->
        <div class="preview-card">
          <div class="preview-header">
            <i class="el-icon-view"></i>
            <span>课程预览</span>
          </div>
          <div class="preview-content">
            <div class="preview-cover">
              <img v-if="courseForm.coverImage" :src="courseForm.coverImage" alt="课程封面" />
              <div v-else class="no-cover">
                <i class="el-icon-picture-outline"></i>
                <p>暂无封面</p>
              </div>
            </div>
            <div class="preview-info">
              <h3 class="preview-title">{{ courseForm.title || '课程名称' }}</h3>
              <div class="preview-categories">
                <el-tag 
                  v-for="(cat, index) in courseForm.categories" 
                  :key="index" 
                  size="small"
                  type="info"
                  style="margin-right: 8px; margin-bottom: 8px;"
                >
                  {{ cat }}
                </el-tag>
                <span v-if="courseForm.categories.length === 0" class="placeholder">未选择分类</span>
              </div>
              <p class="preview-desc">{{ courseForm.description || '暂无描述' }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'CourseCreate',
  data() {
    const validateTitle = (rule, value, callback) => {
      if (!value) {
        callback(new Error('请输入课程名称'))
      } else if (value.length < 3) {
        callback(new Error('课程名称至少3个字符'))
      } else if (value.length > 100) {
        callback(new Error('课程名称最多100个字符'))
      } else {
        callback()
      }
    }

    return {
      courseForm: {
        title: '',
        description: '',
        categories: [], // 改为多选数组
        price: 0,
        coverImage: '',
        capacity: 100,
        duration: '8',
        level: 'beginner',
        prerequisites: '',
        objectives: ''
      },
      rules: {
        title: [{ validator: validateTitle, trigger: 'blur' }],
        categories: [
          { required: true, message: '请至少选择一个课程分类', trigger: 'change', type: 'array' }
        ]
      },
      fileList: [],
      submitting: false
    }
  },
  methods: {
    // 上传成功
    handleUploadSuccess(response) {
      if (response.code === 0) {
        this.courseForm.coverImage = response.data.url
        this.$message.success('图片上传成功')
      } else {
        this.$message.error(response.message || '上传失败')
      }
    },

    // 上传失败
    handleUploadError() {
      this.$message.error('图片上传失败')
    },

    // 创建课程（仅保存为草稿，不发布）
    createCourse() {
      this.$refs.courseForm.validate(valid => {
        if (valid) {
          this.submitting = true
          const payload = {
            ...this.courseForm,
            status: 'draft' // 只创建草稿，不发布
          }

          // 临时使用 mock 数据，避免 API 不存在导致无限加载
          // 生产环境请替换为实际 API 调用
          const useMock = true // 设置为 false 使用真实 API

          if (useMock) {
            // Mock 成功响应
            setTimeout(() => {
              const mockCourseId = Date.now() // 使用时间戳作为临时 ID
              this.$message.success('课程创建成功')
              this.$router.push(`/mycourse/teacher/${mockCourseId}?tab=courseManagement`)
              this.submitting = false
            }, 800)
          } else {
            // 实际 API 调用
            this.$api.post('/courses', payload)
              .then(res => {
                this.$message.success('课程创建成功')
                this.$router.push(`/mycourse/teacher/${res.data.id}?tab=courseManagement`)
              })
              .catch(err => {
                console.error('课程创建失败:', err)
                this.$message.error(err.response?.data?.message || '创建失败，请稍后重试')
              })
              .finally(() => {
                this.submitting = false
              })
          }
        }
      })
    },

    // 返回
    goBack() {
      this.$router.back()
    }
  }
}
</script>

<style scoped lang="scss">
.course-create-container {
  padding: 20px;
  background: #f5f7fa;
  min-height: 100vh;
}

.page-header {
  margin-bottom: 24px;
  background: white;
  padding: 24px 32px;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  display: flex;
  align-items: center;
  gap: 16px;
  border-left: 4px solid #667eea;

  ::v-deep .el-button {
    background: #f5f7fa;
    color: #606266;
    border: 1px solid #dcdfe6;
    width: 40px;
    height: 40px;
    font-size: 18px;
    transition: all 0.3s;

    &:hover {
      background: #667eea;
      color: white;
      border-color: #667eea;
    }
  }

  .header-content {
    flex: 1;

    .page-title {
      margin: 0 0 4px 0;
      font-size: 24px;
      color: #303133;
      font-weight: 600;
    }

    .page-subtitle {
      margin: 0;
      font-size: 14px;
      color: #909399;
    }
  }
}

.create-form-wrapper {
  max-width: 1400px;
  margin: 0 auto;

  .form-layout {
    display: grid;
    grid-template-columns: 1fr 400px;
    gap: 24px;
    align-items: start;
  }

  .form-card {
    background: white;
    border-radius: 12px;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
    padding: 32px;
  }

  ::v-deep .el-form-item {
    margin-bottom: 22px;

    .el-form-item__label {
      color: #606266;
      font-weight: 500;
      font-size: 14px;
    }
    
    .el-input__inner,
    .el-textarea__inner {
      border-radius: 6px;
      border: 1px solid #dcdfe6;
      transition: all 0.3s ease;
      
      &:focus {
        border-color: #667eea;
      }
    }

    .el-select {
      width: 100%;
    }
  }

  .form-section {
    margin-bottom: 32px;

    .section-header {
      display: flex;
      align-items: center;
      gap: 10px;
      margin-bottom: 24px;
      padding-bottom: 12px;
      border-bottom: 2px solid #f0f0f0;

      .section-icon {
        font-size: 20px;
        color: #667eea;
      }

      .section-title {
        font-size: 18px;
        color: #303133;
        font-weight: 600;
        margin: 0;
      }
    }
  }

  .preview-card {
    background: white;
    border-radius: 12px;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
    padding: 24px;
    position: sticky;
    top: 20px;

    .preview-header {
      display: flex;
      align-items: center;
      gap: 8px;
      margin-bottom: 20px;
      padding-bottom: 12px;
      border-bottom: 2px solid #f0f0f0;
      font-size: 16px;
      font-weight: 600;
      color: #303133;

      i {
        font-size: 18px;
        color: #667eea;
      }
    }

    .preview-content {
      .preview-cover {
        width: 100%;
        height: 200px;
        border-radius: 8px;
        overflow: hidden;
        margin-bottom: 16px;
        background: #f5f7fa;

        img {
          width: 100%;
          height: 100%;
          object-fit: cover;
        }

        .no-cover {
          width: 100%;
          height: 100%;
          display: flex;
          flex-direction: column;
          align-items: center;
          justify-content: center;
          color: #c0c4cc;

          i {
            font-size: 48px;
            margin-bottom: 8px;
          }

          p {
            margin: 0;
            font-size: 14px;
          }
        }
      }

      .preview-info {
        .preview-title {
          font-size: 18px;
          font-weight: 600;
          color: #303133;
          margin: 0 0 12px 0;
          overflow: hidden;
          text-overflow: ellipsis;
          display: -webkit-box;
          -webkit-line-clamp: 2;
          line-clamp: 2;
          -webkit-box-orient: vertical;
        }

        .preview-categories {
          margin-bottom: 12px;
          min-height: 28px;

          .placeholder {
            color: #c0c4cc;
            font-size: 13px;
          }
        }

        .preview-desc {
          font-size: 13px;
          color: #606266;
          line-height: 1.6;
          margin: 0;
          overflow: hidden;
          text-overflow: ellipsis;
          display: -webkit-box;
          -webkit-line-clamp: 4;
          line-clamp: 4;
          -webkit-box-orient: vertical;
        }
      }
    }
  }

  ::v-deep .el-upload {
    .el-upload__tip {
      font-size: 12px;
      color: #909399;
      margin-top: 8px;
    }
  }

  .form-actions {
    display: flex;
    justify-content: flex-end;
    gap: 12px;
    margin-top: 32px;
    padding-top: 24px;
    border-top: 1px solid #f0f0f0;

    ::v-deep .el-button {
      min-width: 120px;
      height: 40px;
      
      &.el-button--primary {
        background: #667eea;
        border-color: #667eea;
        
        &:hover {
          background: #5568d3;
          border-color: #5568d3;
        }
      }
    }
  }

  @media (max-width: 1200px) {
    .form-layout {
      grid-template-columns: 1fr;
    }

    .preview-card {
      position: static;
    }
  }
}
</style>
