<template>
  <div class="course-create-container">
    <div class="page-header">
      <el-button icon="el-icon-arrow-left" type="text" @click="goBack">返回</el-button>
      <h1>创建新课程</h1>
    </div>

    <div class="create-form-wrapper">
      <el-card shadow="hover">
        <el-form
          ref="courseForm"
          :model="courseForm"
          :rules="rules"
          label-width="120px"
          size="medium"
        >
          <!-- 课程基本信息 -->
          <div class="form-section">
            <h3>基本信息</h3>
            
            <el-form-item label="课程名称" prop="title">
              <el-input
                v-model="courseForm.title"
                placeholder="请输入课程名称"
                maxlength="100"
                show-word-limit
              />
            </el-form-item>

            <el-form-item label="课程描述" prop="description">
              <el-input
                v-model="courseForm.description"
                type="textarea"
                rows="4"
                placeholder="请输入课程描述"
                maxlength="500"
                show-word-limit
              />
            </el-form-item>

            <el-form-item label="课程分类" prop="category">
              <el-select v-model="courseForm.category" placeholder="请选择分类">
                <el-option label="Web 前端" value="web" />
                <el-option label="后端开发" value="backend" />
                <el-option label="移动开发" value="mobile" />
                <el-option label="数据科学" value="data" />
                <el-option label="DevOps" value="devops" />
                <el-option label="其他" value="other" />
              </el-select>
            </el-form-item>

            <el-form-item label="课程价格" prop="price">
              <el-input-number
                v-model="courseForm.price"
                :min="0"
                :max="99999"
                placeholder="0"
                controls-position="right"
              />
              <span class="price-unit">元</span>
            </el-form-item>

            <el-form-item label="课程封面" prop="coverImage">
              <el-upload
                ref="coverUpload"
                action="/api/upload/image"
                :file-list="fileList"
                :on-success="handleUploadSuccess"
                :on-error="handleUploadError"
                limit="1"
                accept="image/*"
              >
                <el-button slot="trigger" type="primary" size="small">
                  选择图片
                </el-button>
                <span slot="tip" class="el-upload__tip">
                  请上传课程封面图片（建议尺寸: 800x600px）
                </span>
              </el-upload>
              <div v-if="courseForm.coverImage" class="preview">
                <img :src="courseForm.coverImage" alt="封面预览" />
              </div>
            </el-form-item>
          </div>

          <!-- 课程概览 -->
          <div class="form-section">
            <h3>课程概览</h3>

            <el-form-item label="学习人数" prop="capacity">
              <el-input-number
                v-model="courseForm.capacity"
                :min="1"
                :max="10000"
                placeholder="0"
                controls-position="right"
              />
              <span class="tip">预计学习人数</span>
            </el-form-item>

            <el-form-item label="学习周期" prop="duration">
              <el-select v-model="courseForm.duration" placeholder="请选择课程时长">
                <el-option label="4 周" value="4" />
                <el-option label="8 周" value="8" />
                <el-option label="12 周" value="12" />
                <el-option label="16 周" value="16" />
                <el-option label="自定进度" value="0" />
              </el-select>
            </el-form-item>

            <el-form-item label="难度级别" prop="level">
              <el-select v-model="courseForm.level" placeholder="请选择难度级别">
                <el-option label="入门" value="beginner" />
                <el-option label="中级" value="intermediate" />
                <el-option label="高级" value="advanced" />
                <el-option label="专家" value="expert" />
              </el-select>
            </el-form-item>

            <el-form-item label="前置要求" prop="prerequisites">
              <el-input
                v-model="courseForm.prerequisites"
                type="textarea"
                rows="3"
                placeholder="请输入学习本课程的前置要求（如有）"
                maxlength="200"
              />
            </el-form-item>
          </div>

          <!-- 课程目标 -->
          <div class="form-section">
            <h3>学习目标</h3>

            <el-form-item label="学习目标" prop="objectives">
              <el-input
                v-model="courseForm.objectives"
                type="textarea"
                rows="4"
                placeholder="请输入学生完成本课程后将学到什么（每行一个要点）"
                maxlength="500"
              />
              <span class="tip">提示：使用换行符分隔多个目标</span>
            </el-form-item>
          </div>

          <!-- 提交按钮 -->
          <div class="form-actions">
            <el-button @click="goBack">取消</el-button>
            <el-button type="primary" :loading="submitting" @click="saveDraft">
              保存为草稿
            </el-button>
            <el-button type="success" :loading="submitting" @click="createAndPublish">
              创建并发布
            </el-button>
          </div>
        </el-form>
      </el-card>
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
        category: '',
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
        description: [
          { required: true, message: '请输入课程描述', trigger: 'blur' },
          { min: 10, message: '课程描述至少10个字符', trigger: 'blur' }
        ],
        category: [
          { required: true, message: '请选择课程分类', trigger: 'change' }
        ],
        price: [
          { type: 'number', required: true, message: '请输入课程价格', trigger: 'blur' }
        ],
        coverImage: [
          { required: true, message: '请上传课程封面', trigger: 'change' }
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

    // 保存为草稿
    saveDraft() {
      this.$refs.courseForm.validate(valid => {
        if (valid) {
          this.submitCourse('draft')
        }
      })
    },

    // 创建并发布
    createAndPublish() {
      this.$refs.courseForm.validate(valid => {
        if (valid) {
          this.submitCourse('pending_review')
        }
      })
    },

    // 提交课程
    submitCourse(status) {
      this.submitting = true
      const payload = {
        ...this.courseForm,
        status
      }

      this.$api.post('/courses', payload)
        .then(res => {
          this.$message.success(
            status === 'draft' ? '课程已保存为草稿' : '课程已发布，请等待管理员审核'
          )
          this.$router.push(`/course/${res.data.id}`)
        })
        .catch(err => {
          this.$message.error(err.response?.data?.message || '创建失败')
        })
        .finally(() => {
          this.submitting = false
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
  margin-bottom: 30px;
  display: flex;
  align-items: center;
  gap: 20px;
}

.page-header h1 {
  margin: 0;
  font-size: 28px;
  color: #333;
}

.create-form-wrapper {
  max-width: 900px;

  /deep/ .el-card {
    border: none;
    border-radius: 4px;
  }

  /deep/ .el-form-item {
    margin-bottom: 22px;

    label {
      color: #333;
    }
  }

  .form-section {
    margin-bottom: 40px;

    h3 {
      font-size: 16px;
      color: #333;
      font-weight: bold;
      margin-bottom: 20px;
      padding-bottom: 10px;
      border-bottom: 2px solid #1890ff;
    }

    .form-section + .form-section h3 {
      margin-top: 0;
    }
  }

  .price-unit,
  .tip {
    margin-left: 10px;
    color: #999;
    font-size: 12px;
  }

  .preview {
    margin-top: 15px;

    img {
      max-width: 200px;
      max-height: 200px;
      border-radius: 4px;
      border: 1px solid #ddd;
    }
  }

  .form-actions {
    display: flex;
    justify-content: center;
    gap: 20px;
    margin-top: 40px;
    padding-top: 20px;
    border-top: 1px solid #f0f0f0;

    /deep/ .el-button {
      min-width: 120px;
    }
  }
}
